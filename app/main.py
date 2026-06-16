import pandas as pd
import streamlit as st
from PIL import Image
from io import BytesIO

from app.groq_vlm import extract_receipt_groq

if "parsed_output" not in st.session_state:
    st.session_state.parsed_output = None

if "runtime" not in st.session_state:
    st.session_state.runtime = None

if "receipt_results" not in st.session_state:
    st.session_state.receipt_results = []

from vlm import extract_receipt
from parser import parse_json
from evaluator import benchmark

st.title("Smart Split Bill")
st.caption("Auto Receipt Reading | Visual Language Model")

model_choice = st.selectbox(
    "Choose Model",
    [
        "Gemini",
        "Groq"
    ]
)

uploaded_file = st.file_uploader(
    "Upload Receipt",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Receipt",
        use_container_width=True
    )

    st.write(
        "Filename:",
        uploaded_file.name
    )

    st.write(
        "File Size (KB):",
        round(uploaded_file.size / 1024, 2)
    )

    if st.button("Extract Receipt"):

        if model_choice == "Gemini":
            benchmark_result = benchmark(
                extract_receipt,
                image
            )
        else:
            benchmark_result = benchmark(
                extract_receipt_groq,
                image
            )

        raw_output = benchmark_result["result"]

        runtime = benchmark_result["runtime"]

        parsed_output = parse_json(raw_output)
        st.session_state.parsed_output = parsed_output
        st.session_state.runtime = runtime

        receipt_summary = {
            "model": model_choice,
            "store_name": parsed_output.get(
                "store_name",
                "-"
            ),
            "date": parsed_output.get(
                "date",
                "-"
            ),
            "total": parsed_output.get(
                "total",
                0
            ),
            "runtime": runtime
        }

        if receipt_summary not in st.session_state.receipt_results:
            st.session_state.receipt_results.append(
                receipt_summary
            )

    
    if st.session_state.parsed_output:

        parsed_output = st.session_state.parsed_output
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Store",
                parsed_output.get(
                    "store_name",
                    "-"
                )
            )

        with col2:
            st.metric(
                "Date",
                parsed_output.get(
                    "date",
                    "-"
                )
            )

        with col3:
            st.metric(
                "Total",
                parsed_output.get(
                    "total",
                    0
                )
            )
        st.metric(
            "Inference Time (sec)",
            st.session_state.runtime
        )

        with st.expander(
            "View Raw JSON"
        ):
            st.json(parsed_output)

        if "items" in parsed_output:

            st.subheader("Receipt Items")

            df = pd.DataFrame(
                parsed_output["items"]
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            st.divider()

            st.subheader("Split Bill")

            people_input = st.text_input(
                "Enter people names (comma separated)",
                placeholder="Person 1, Person 2, Person 3, etc."
            )

            if people_input:

                people = [
                    p.strip()
                    for p in people_input.split(",")
                    if p.strip()
                ]

                assignments = {}

                for idx, row in df.iterrows():

                    assignments[idx] = st.selectbox(
                        f"{row['item_name']} ({row['amount']})",
                        people,
                        key=f"item_{idx}"
                    )

                if st.button("Calculate Split"):

                    totals = {}

                    for person in people:
                        totals[person] = 0

                    for idx, row in df.iterrows():

                        person = assignments[idx]

                        totals[person] += float(
                            row["amount"]
                        )

                    result_df = pd.DataFrame(
                        {
                            "Person": totals.keys(),
                            "Amount": totals.values()
                        }
                    )

                    st.subheader("Split Result")

                    st.dataframe(
                        result_df,
                        use_container_width=True
                    )

st.divider()

st.subheader("All Receipts")

if st.session_state.receipt_results:

    summary_df = pd.DataFrame(
        st.session_state.receipt_results
    )

    st.dataframe(
        summary_df,
        use_container_width=True
    )

    csv = summary_df.to_csv(
        index=False
    )

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="receipt_summary.csv",
        mime="text/csv"
    )

    excel_buffer = BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        summary_df.to_excel(
            writer,
            index=False,
            sheet_name="Receipts"
        )

    st.download_button(
        label="Download Excel",
        data=excel_buffer.getvalue(),
        file_name="receipt_summary.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )