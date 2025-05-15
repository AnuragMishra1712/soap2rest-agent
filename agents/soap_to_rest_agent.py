import requests
import textwrap

class SOAPToRESTAgent:
    def __init__(self, model="mistral"):
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"

    def convert(self, soap_description: str) -> str:
        response = requests.post(self.ollama_url, json={
            "model": self.model,
            "prompt": soap_description,
            "stream": False
        })

        if response.status_code != 200:
            raise RuntimeError(f"AI generation failed: {response.text}")

        code = response.json()["response"].strip()

        # 🔻 Remove markdown if present
        if code.startswith("```python"):
            code = code.replace("```python", "").strip()
        if code.endswith("```"):
            code = code.rstrip("```").strip()

        # 🔧 Fix indentation (removes common leading whitespace)
        code = textwrap.dedent(code)

        # ✅ Fix missing request import (as before)
        if "request.args" in code and "request" not in code.splitlines()[0]:
            lines = code.splitlines()
            if "from flask import Flask, jsonify" in lines[0]:
                lines[0] = "from flask import Flask, request, jsonify"
                code = "\n".join(lines)

        return code
