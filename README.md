# Smart Split Bill OCR

Smart Split Bill OCR is a Streamlit application that extracts information from receipt images using Vision Language Models (VLMs) and automatically calculates how much each person should pay.

The project was built to explore OCR workflows using modern multimodal AI models and compare their performance on real-world receipt data.

Currently supported models:

* Gemini 2.5 Flash
* Llama 4 Scout (Groq)

---

## Features

* Upload receipt images (JPG, JPEG, PNG)
* Extract receipt information into structured JSON
* View detected store name, date, items, and totals
* Split bills across multiple people
* Compare inference runtime between Gemini and Groq
* Export receipt summaries to CSV and Excel

---

## Example Workflow

```text
Upload Receipt
      ↓
Select Model
      ↓
Extract Receipt
      ↓
Review Items
      ↓
Assign Items to People
      ↓
Calculate Split
      ↓
Export Results
```

---

## Project Structure

```text
Smart_Split_Bill_OCR/
│
├── app/
│   ├── main.py
│   ├── vlm.py
│   ├── groq_vlm.py
│   ├── parser.py
│   ├── evaluator.py
│   └── static/
│
├── receipts/
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/weizshahzadkalia/Smart_Split_Bill_OCR.git
cd Smart_Split_Bill_OCR
```

Create and activate a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## API Keys

This project requires API keys for both Gemini and Groq.

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
```

The `.env` file is intentionally excluded from GitHub through `.gitignore`.

### Getting API Keys

**Gemini**

1. Visit Google AI Studio
2. Generate an API key
3. Copy the key into `.env`

**Groq**

1. Create an account on Groq
2. Generate an API key
3. Copy the key into `.env`

---

## Running the Application

From the project root directory:

```bash
streamlit run app/main.py
```

Streamlit will start a local server and provide a URL similar to:

```text
http://localhost:8501
```

Open the URL in your browser.

---

## Using the Application

1. Upload a receipt image.
2. Select either Gemini or Groq.
3. Click **Extract Receipt**.
4. Review the extracted receipt information.
5. Enter participant names.
6. Assign each item to a person.
7. Click **Calculate Split**.
8. Export results if needed.

---

## Benchmarking

One of the goals of this project is to compare different VLMs on receipt extraction tasks.

The application records:

* Model used
* Receipt information
* Inference runtime

Example:

| Model  | Runtime (sec) |
| ------ | ------------: |
| Gemini |          2.31 |
| Groq   |          0.94 |

This makes it possible to compare speed and extraction quality across models using the same receipt dataset.

---

## Tech Stack

* Python
* Streamlit
* Pandas
* Gemini API
* Groq API
* OpenPyXL

---

## Future Improvements

* Additional VLM models
* Accuracy benchmarking
* Database integration
* Receipt history tracking
* Cloud deployment

---

## Author

Built as a hands-on project to explore OCR, Vision Language Models, and practical AI-assisted expense sharing.
