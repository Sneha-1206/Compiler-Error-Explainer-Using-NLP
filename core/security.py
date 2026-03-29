def security_note(code):
    if "except:" in code or "pass" in code:
        return "⚠️ Ignoring exceptions can hide bugs and create risks."
    return ""