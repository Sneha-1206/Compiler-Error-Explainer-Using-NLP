from flask import Flask, request, render_template_string
from config import C_FILE, PY_FILE
from data.loader import load_dataset
from core.execution import run_python_code, run_cpp_code
from core.security import security_note
from core.ast_analysis import extract_python_context
from nlp.explainer import Explainer
from evaluation.evaluator import evaluate
from flask import render_template

app = Flask(__name__)

# Load
c_file = "/Users/valerusnehapriya/untitled folder/c++_bugs.json"
py_file = "/Users/valerusnehapriya/untitled folder/python bugs.json"
dataset = load_dataset(c_file,py_file)
explainer = Explainer(dataset)

print("Model Accuracy:", evaluate(explainer, dataset), "%")

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None

    if request.method == 'POST':
        code = request.form.get('code')
        language = request.form.get('language')

        error = run_python_code(code) if language == "python" else run_cpp_code(code)

        if error:
            output = explainer.explain(error, code, language)

            result = {
                "status": "error",
                "error": error,
                "explanation": output["explanation"],
                "fix": output["fix"],
                "confidence": output["confidence"],
                "context": output["context"],
                "security": security_note(code)
            }
        else:
            result = {
                "status": "success",
                "error": "No Error",
                "explanation": "Code executed successfully.",
                "fix": "No fix needed.",
                "confidence": 100,
                "context": extract_python_context(code),
                "security": security_note(code)
            }

    return render_template("index.html", result=result)

@app.route('/api/explain', methods=['POST'])
def api_explain():
    try:
        data = request.get_json()

        if not data:
            return {"error": "Invalid JSON input"}, 400

        code = data.get("code", "")
        language = data.get("language", "python")

        if not code:
            return {"error": "Code is required"}, 400

        # Run code
        if language == "python":
            error = run_python_code(code)
        elif language == "cpp":
            error = run_cpp_code(code)
        else:
            return {"error": "Unsupported language"}, 400

        # If error exists
        if error:
            output = explainer.explain(error, code, language)

            response = {
                "status": "error",
                "error": error,
                "explanation": output["explanation"],
                "fix": output["fix"],
                "confidence": output["confidence"],
                "context": output["context"],
                "security": security_note(code)
            }
        else:
            response = {
                "status": "success",
                "error": None,
                "message": "Code executed successfully",
                "confidence": 100,
                "context": extract_python_context(code),
                "security": security_note(code)
            }

        return response, 200

    except Exception as e:
        return {"error": str(e)}, 500
if __name__ == '__main__':
    app.run(debug=True)