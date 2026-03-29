from transformers import pipeline
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from core.preprocess import clean_error
from core.ast_analysis import extract_python_context
from nlp.generator_api import generate_explanation
class Explainer:
    def __init__(self, dataset):
        self.generator = pipeline("text2text-generation", model="google/flan-t5-small")
        self.dataset = dataset

        # SBERT
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        self.lang_data = {"python": [], "cpp": []}

        for d in dataset:
            self.lang_data[d["language"]].append(d)

        self.lang_embeddings = {}
        self.tfidf = {}
        self.tfidf_matrix = {}

        for lang, items in self.lang_data.items():

            texts = [
             f"{d['error_type']} {d['error_message']} {d['buggy_code']} {d['explanation']}"
             for d in items
            ]

            # SBERT embeddings
            self.lang_embeddings[lang] = self.model.encode(
                texts, convert_to_numpy=True
            )

            # TF-IDF
            vectorizer = TfidfVectorizer()
            tfidf_mat = vectorizer.fit_transform(texts)

            self.tfidf[lang] = vectorizer
            self.tfidf_matrix[lang] = tfidf_mat
    def rule_based(self, error):
        e = error.lower()

        # C/C++ Errors
        if "expected" in e and ";" in e:
            return {
                "method": "rule",
                "explanation": "You likely missed a semicolon at the end of a statement in your C/C++ code.",
                "fix": "Add ';' at the end of the previous statement."
            }

        if "undefined reference" in e:
            return {
                "method": "rule",
                "explanation": "The linker cannot find the definition of a function or variable.",
                "fix": "Make sure the function is defined and all files are compiled and linked correctly."
            }

        if "not declared in this scope" in e:
            return {
                "method": "rule",
                "explanation": "You are using a variable or function that was not declared.",
                "fix": "Declare the variable or include the required header file."
            }

        if "expected primary expression" in e:
            return {
                "method": "rule",
                "explanation": "There is a syntax issue, often due to missing operands or incorrect expression.",
                "fix": "Check for missing values, operators, or misplaced symbols."
            }

        # Python Errors
        if "indentationerror" in e:
            return {
                "method": "rule",
                "explanation": "There is an indentation problem in your Python code.",
                "fix": "Ensure consistent indentation (usually 4 spaces)."
            }

        if "syntaxerror" in e and "invalid syntax" in e:
            return {
                "method": "rule",
                "explanation": "There is a syntax mistake in your Python code.",
                "fix": "Check for missing colons, parentheses, or incorrect structure."
            }

        if "nameerror" in e:
            return {
                "method": "rule",
                "explanation": "You are using a variable that has not been defined.",
                "fix": "Define the variable before using it."
            }
        if "keyerror" in e:
            match = re.search(r"'(.+?)'", error)
            key = match.group(1) if match else "unknown"
            return {
             "method": "rule",
             "explanation": f"The key '{key}' is accessed in the dictionary, but it does not exist.",
             "fix": f"Ensure '{key}' exists in the dictionary or use d.get('{key}') to avoid the error."
            }

        return None
    def retrieve(self, error, code="", language="python", top_k=3):

        candidates = self.lang_data.get(language, [])
        if not candidates:
            return None, 0

        query_text = clean_error(error) + " " + code

        # SBERT
        query_sbert = self.model.encode([query_text], convert_to_numpy=True)
        sbert_sim = cosine_similarity(
            query_sbert,
        self.lang_embeddings[language]
        )[0]

        # TF-IDF
        tfidf_vec = self.tfidf[language].transform([query_text])
        tfidf_sim = cosine_similarity(
            tfidf_vec,
            self.tfidf_matrix[language]
        )[0]

        #  NEW WEIGHTING (better balance)
        final_scores = 0.8 * sbert_sim + 0.2 * tfidf_sim

        #  TOP-K retrieval
        top_indices = np.argsort(final_scores)[-top_k:][::-1]

        best_idx = top_indices[0]
        confidence = float(final_scores[best_idx])

        if best_idx >= len(candidates):
            return None, 0
        return candidates[best_idx], confidence
    
    def generate(self, error, context, code=""):
        explanation, fix = generate_explanation(error, context, code)

        return {
        "method": "groq_api",
        "explanation": explanation,
        "fix": fix
        }

    def explain(self, error, code="",language="python"):
        context = extract_python_context(code) if language=="python" else "C++ analysis limited"
        rule = self.rule_based(error)
        if rule:
            return rule
        result = self.retrieve(error,code,language)

        if isinstance(result, tuple) and len(result) == 2:
            retrieved, confidence = result
        else:
            retrieved, confidence = None, 0

        if retrieved and confidence > 0.4:
            return {
                "method": "retrieval",
                "explanation": retrieved["explanation"],
                "fix": retrieved["fix"],
                "confidence": round(confidence * 100, 2),
                "context": context
            }
        elif confidence >= 0.2:
            generated = self.generate(error, context)
            return {
                "method": "transformer",
                "explanation": generated,
                "fix": "Derived from explanation",
                "confidence": round(confidence * 100, 2),
                "context": context
            }
        else:
            generated = self.generate(error, context)
            return {
        "method": "api",
        "explanation": generated["explanation"],
        "fix": generated["fix"],
        "confidence": round(confidence * 100, 2),
        "context": context
             }
    def generate(self, error, context):
        explanation, fix = generate_explanation(error, context)

        return {
        "method": "api",
        "explanation": explanation,
        "fix": fix
        }