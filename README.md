# 🚀 Compiler Error Explainer using NLP

A high-performance, AI-powered web application designed to help developers understand and fix compiler and runtime errors in **Python** and **C/C++**. By leveraging a hybrid AI engine, this tool provides clear explanations, exact code fixes, and confidence scores in real-time.

---

## ✨ Key Features

- **Hybrid AI Engine**: Combines rule-based logic, semantic search (Retrieval), and generative AI (Llama 3) for the most accurate results.
- **Multi-Language Support**: Complete support for Python and C/C++ error analysis.
- **Deep Code Analysis**: Uses AST (Abstract Syntax Tree) analysis for Python to provide context-aware insights.
- **Real-time Execution**: Captures actual compiler and runtime output by executing code in a safe environment.
- **Glassmorphism UI**: A stunning, modern, and responsive interface built for an exceptional developer experience.
- **Security Guard**: Built-in security checks to identify potentially harmful code patterns.

---

## 🛠️ Technology Stack

- **Backend**: [Flask](https://flask.palletsprojects.com/) (Python)
- **NLP Engine**:
  - **Retrieval**: [SBERT](https://www.sbert.net/) (`all-MiniLM-L6-v2`) & TF-IDF
  - **Generations**: [Groq API](https://groq.com/) (Llama 3 70B)
  - **Preprocessing**: [Transformers](https://huggingface.co/docs/transformers/index), [Scikit-learn](https://scikit-learn.org/)
- **Frontend**: HTML5, CSS3 (Custom Glassmorphism Design), Vanilla JavaScript
- **Core Logic**: Multi-stage pipeline (Rule -> Retrieval -> LLM Generation)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- GCC/G++ (for C++ code analysis)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/compiler-error-explainer.git
   cd compiler-error-explainer
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**:
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Running the Application

Start the Flask development server:
```bash
python3 app.py
```
The application will be available at `http://127.0.0.1:5000`.

---

## 📁 Project Structure

```text
├── app.py              # Flask Application Entry Point
├── config.py           # Configuration Settings
├── requirements.txt    # Project Dependencies
├── core/               # Execution & Security logic
│   ├── ast_analysis.py # Python AST context extraction
│   ├── execution.py    # Code execution handlers
│   └── security.py     # Security note generator
├── nlp/                # NLP & AI Logic
│   ├── explainer.py    # Hybrid Explanation Pipeline
│   └── generator_api.py # Groq API Integration
├── data/               # Datasets
│   └── loader.py       # JSON Dataset Loader
├── dataset/            # Compiled error datasets (JSON)
├── templates/          # UI Components
│   └── index.html      # Main Web Interface
└── evaluation/         # Model Accuracy Tests
```

---

## 🧠 How it Works

The project uses a **triple-layered approach** to provide the best possible explanation:

1.  **Rule-Based Layer**: Checks for common, easily identifiable patterns (e.g., missing semicolons, indentation errors).
2.  **Retrieval Layer**: Uses SBERT and TF-IDF to search the internal dataset for highly similar previously solved bugs.
3.  **Generative Layer**: If no high-confidence match is found, it sends the code and error context to the Llama 3 model via the Groq API for a human-like explanation and fix.

---

## 🛡️ Security Note

This tool executes code to capture compiler errors. While basic security checks are implemented, always ensure you are running code from trusted sources.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
