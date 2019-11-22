from flask import Flask, request, url_for, jsonify
import urllib.request

src_url="https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml"

src_file="file.xml"
app = Flask(__name__)

@app.route("/")
def home():
    return """<h1>Please Try with parameters mode like:</h1>
    <p>1 : /converter/amount/XXX/src_currency/YYY/dest_currency/KKK/ference_date/ZZZ-ZZ-ZZ</p>
    <p>2 : http://localhost:5000/converter?amount=XXX&src_currency=YYY&st_currency=KKK&ference_date=ZZZZ-ZZ-ZZ</p>
    """
@app.route("/converter")
def convertor():
    # print(" Ciao ",request.args)
    conv = convertor()
    conv.get_file()
    conv.readXml(src_file)
    
    amount=request.args.get('amount')
    src_currency=request.args.get('src_currency')
    dest_currency=request.args.get('dest_currency')
    ference_date=request.args.get('ference_date')
    
    result = conv.currencyConverter(src_currency,amount,dest_currency,ference_date)
    
    return jsonify(result)
	
	
@app.route('/converter/amount/<amount>/src_currency/<src_currency>/dest_currency/<dest_currency>/ference_date/<ference_date>', methods=['GET', 'POST'])
def converter(amount,src_currency,dest_currency,ference_date):
    
    conv = convertor()
    conv.get_file()
    conv.readXml(src_file)
    
    result = conv.currencyConverter(src_currency,amount,dest_currency,ference_date)
    return jsonify(result)

    
class convertor:
    
    def __init__(self):
        self.currencyData={}
		
    # Download and save the file in local
    def get_file(self):
        with urllib.request.urlopen(src_url) as response, open(src_file, 'wb') as out_file:
            data = response.read() # a `bytes` object
            out_file.write(data) 
    
	# Read the file to load Data and save it in dictionary dic[data][currency][date]
    def readXml(self, data):
        import xml.etree.ElementTree as ET
        tree = ET.parse(data)
        root = tree.getroot()
        for elem in root:
            for subelem in elem:
                get_date = subelem.attrib.get('time')
                if get_date != None:
                    dateCurrency={}
                    for sub in subelem:
                        dateCurrency[sub.attrib.get('currency')]=float(sub.attrib.get('rate'))
                    self.currencyData[get_date]=dateCurrency
    
	# function currency Converter   
    def currencyConverter(self,var_src_currency,var_montant,var_dest_currency,var_ference_date):
        rest = {}
        if var_src_currency == None or var_dest_currency == None or var_ference_date == None or var_montant == None:
            msg = 'One or more parameters are null',
            rest = {'amount':var_montant,'src_currency':var_src_currency,'dest_currency':var_dest_currency,'ference_date':var_ference_date, 'Message error':  msg }
            return rest
        var_src_currency = str(var_src_currency).upper()
        var_dest_currency = str(var_dest_currency).upper()
        data_currency = self.currencyData
        if var_src_currency == var_dest_currency:
            msg = 'src_currency and dest_currency are the same value ',var_src_currency
            rest = {'amount':var_montant,'currency':var_src_currency, 'Message error':  msg }
        else:
            if var_ference_date in self.currencyData.keys():
                rate = self.currencyData.get(var_ference_date).get(var_dest_currency)
                if rate: 
                    rest_value=rate
                    rate_eval = rate * float(var_montant)
                    rest_value = float("{0:.2f}".format(rate_eval))
                    rest = {'amount':rest_value,'currency':var_dest_currency}
                else:
                    msg = 'dest_currency : '+var_dest_currency+' Not Found'
                    rest = {'amount':var_montant,'currency':var_src_currency,'Message error':  msg }
            else:
                msg = 'ference_date : '+var_ference_date+ ' Not Found'
                rest = {'amount':var_montant,'src_currency':var_src_currency, 'Message error':  msg }
        return rest


if __name__ == "__main__":
    app.run()