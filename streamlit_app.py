import streamlit as st
import requests
import xml.etree.ElementTree as ET
from agents.soap_to_rest_agent import SOAPToRESTAgent
from pathlib import Path

SOAP_URL = "http://127.0.0.1:8000"
REST_URL = "http://127.0.0.1:5000/currency"

def get_soap_response(country_code):
    headers = {
        "Content-Type": "text/xml; charset=utf-8"
    }
    body = f"""<?xml version="1.0" encoding="utf-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:web="http://www.oorsprong.org/websamples.countryinfo">
       <soapenv:Header/>
       <soapenv:Body>
          <web:GetCountryCurrency>
             <web:sCountryISOCode>{country_code}</web:sCountryISOCode>
          </web:GetCountryCurrency>
       </soapenv:Body>
    </soapenv:Envelope>"""

    try:
        res = requests.post(SOAP_URL, headers=headers, data=body)
        tree = ET.fromstring(res.content)
        ns = {
            "soap": "http://schemas.xmlsoap.org/soap/envelope/",
            "tns": "http://www.oorsprong.org/websamples.countryinfo"
        }
        result = tree.find(".//tns:GetCountryCurrencyResult", ns).text
        return result, res.text
    except Exception as e:
        return "Error", str(e)

def get_rest_response(country_code):
    try:
        res = requests.get(REST_URL, params={"country_code": country_code})
        if res.status_code == 200:
            return res.json().get("currency", "Unknown"), res.text
        else:
            return "Error", res.text
    except Exception as e:
        return "Error", str(e)

def regenerate_rest_api(prompt):
    agent = SOAPToRESTAgent()
    output = agent.convert(prompt)
    Path("rest_output").mkdir(exist_ok=True)
    with open("rest_output/generated_rest_api.py", "w") as f:
        f.write(output)
    return output

st.set_page_config(page_title="SOAP to REST AI UI", layout="wide")
st.title("🧠 SOAP to REST AI Converter")

with st.sidebar:
    st.header("🧠 AI Prompt")
    default_prompt = """
Write a valid Flask REST API in Python. Your code must start with:
from flask import Flask, request, jsonify
Ensure proper indentation and formatting.

Do not return markdown. Do not explain anything.

Requirements:
- Create endpoint: GET /currency?country_code=IN
- Input: country_code (query param)
- Output: JSON with currency name

Mappings:
- IN → Rupees
- US → Dollar
- JP → Yen

Error Handling:
- Return 400 with an error if missing or invalid
"""
    user_prompt = st.text_area("LLM Prompt for REST API Generation", value=default_prompt, height=300)
    if st.button("🔄 Regenerate REST API using ITLIZE_AI"):
        with st.spinner("Generating REST API code using AI..."):
            output_code = regenerate_rest_api(user_prompt)
            st.success("REST API regenerated!")
            st.code(output_code, language="python")

st.markdown("Enter a country code and compare outputs from your SOAP and REST APIs.")
country_code = st.text_input("Enter Country Code", value="IN")

if st.button("🔍 Compare SOAP vs REST"):
    soap_currency, soap_raw = get_soap_response(country_code)
    rest_currency, rest_raw = get_rest_response(country_code)

    col1, col2 = st.beta_columns(2)  # ✅ Works in older versions


    with col1:
        st.subheader("🧼 SOAP Response")
        st.code(soap_raw, language="xml")
        st.write(f"Parsed Currency: `{soap_currency}`")

    with col2:
        st.subheader("🌍 REST Response")
        st.code(rest_raw, language="json")
        st.write(f"Parsed Currency: `{rest_currency}`")

    if soap_currency == rest_currency:
        st.success("✅ SOAP and REST responses MATCH")
    else:
        st.error("❌ SOAP and REST responses DO NOT match")

st.markdown("---")
st.markdown("Built with ITLIZE AI, Flask, and Streamlit.*")
