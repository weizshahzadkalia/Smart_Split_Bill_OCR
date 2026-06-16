import json
import re

#Cleaning the output model

def parse_json(text):

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if match:
        try:
            return json.loads(
                match.group()
            )
        except:
            return {
                "error":
                "Invalid JSON"
            }

    return {
        "error":
        "No JSON found"
    }