# mock_soap_server.py

from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

class CountryService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def GetCountryCurrency(ctx, sCountryISOCode):
        mapping = {
            "IN": "Rupees",
            "US":"Dollar",
            "JP":"Yen"
        }
        return mapping.get(sCountryISOCode, "Unknown")

application = Application(
    [CountryService],
    tns='http://www.oorsprong.org/websamples.countryinfo',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)

if __name__ == '__main__':
    print("🚀 SOAP server running on http://127.0.0.1:8000/")
    server = make_server('127.0.0.1', 8000, wsgi_app)
    server.serve_forever()
