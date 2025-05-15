import requests
import xml.etree.ElementTree as ET

def get_soap_currency(country_code):
    url = "http://127.0.0.1:8000"
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

    response = requests.post(url, data=body, headers=headers)
    print(f"✅ SOAP Status Code: {response.status_code}")

    # Parse XML and extract result
    tree = ET.fromstring(response.content)
    ns = {
        "soap": "http://schemas.xmlsoap.org/soap/envelope/",
        "tns": "http://www.oorsprong.org/websamples.countryinfo"
    }

    try:
        result = tree.find(".//tns:GetCountryCurrencyResult", ns).text
        print(f"💬 Currency for {country_code}: {result}")
    except:
        print("❌ Could not extract currency from SOAP response")

# 🧪 Test
for code in ["IN", "US", "JP", "FR"]:
    get_soap_currency(code)
