import json

def load_dataset(c_file, py_file):
    data = []

    with open(c_file) as f:
        for item in json.load(f):
            if item.get("error_message") and item.get("explanation"):
                data.append({
                    "error_type": item.get("error_type", ""),
                    "buggy_code": item.get("buggy_code", ""),
                    "error_message": item["error_message"],
                    "explanation": item["explanation"],
                    "fix": item.get("fix_suggestion", ""),
                    "language": "cpp"
                })

    with open(py_file) as f:
        for item in json.load(f):
            msg = item.get("error_message", "")
            if msg and "no error" not in msg:
                data.append({
                    "error_type": item.get("error_type", ""),
                    "buggy_code": item.get("buggy_code", ""),
                    "error_message": msg,
                    "explanation": item.get("explanation", ""),
                    "fix": item.get("fix_suggestion", ""),
                    "language": "python"
                })

    return data