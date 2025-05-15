import requests
import xml.etree.ElementTree as ET

SOAP_URL = "http://127.0.0.1:8000"
REST_URL = "http://127.0.0.1:5000/currency"

HEADERS = {
    "Content-Type": "text/xml; charset=utf-8"
}

def get_soap_currency(country_code):
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

    response = requests.post(SOAP_URL, data=body, headers=HEADERS)
    tree = ET.fromstring(response.content)

    ns = {
        "soap": "http://schemas.xmlsoap.org/soap/envelope/",
        "tns": "http://www.oorsprong.org/websamples.countryinfo"
    }

    try:
        result = tree.find(".//tns:GetCountryCurrencyResult", ns).text
        return result
    except:
        return "Unknown (Parsing Failed)"

def get_rest_currency(country_code):
    response = requests.get(REST_URL, params={"country_code": country_code})
    if response.status_code == 200:
        return response.json().get("currency", "Unknown")
    else:
        return f"REST Error: {response.status_code}"

def compare(country_code):
    soap_result = get_soap_currency(country_code)
    rest_result = get_rest_currency(country_code)

    print(f"\n🌐 Country Code: {country_code}")
    print(f"🧼 SOAP Currency: {soap_result}")
    print(f"🌍 REST Currency: {rest_result}")
    print("✅ Match!" if soap_result == rest_result else "❌ Mismatch!")

if __name__ == "__main__":
    for code in ["IN", "US", "JP", "FR"]:
        compare(code)

