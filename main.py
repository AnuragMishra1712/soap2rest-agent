# main.py

from agents.soap_to_rest_agent import SOAPToRESTAgent
from pathlib import Path

if __name__ == "__main__":
    
    prompt = """
Write a valid Flask REST API in Python. Your code must start with:

from flask import Flask, request, jsonify
make sure identation is correct 
you are not keeping identation properly
make sure actual code starts just at the same level below
from flask import Flask, request, jsonify

for eg:
from flask import Flask, request, jsonify
app = Flask(__name__)
...
    
Do not return markdown. Do not explain anything.

Requirements:
- Create an endpoint: GET /currency?country_code=IN
- Input: country_code as a query parameter
- Output: JSON with the currency name

Mappings:
- IN → Rupees
- US → Dollar
- JP → Yen

Error Handling:
- If country_code is missing, return 400 with a clear error.
- If country_code is invalid, return 400 with a clear error.

The code must be fully runnable as a standalone Python script.

"""

    agent = SOAPToRESTAgent()
    output = agent.convert(prompt)

    Path("rest_output").mkdir(exist_ok=True)
    with open("rest_output/generated_rest_api.py", "w") as f:
        f.write(output)

    print("✅ REST API generated in rest_output/generated_rest_api.py")
