# currency_api
Amount currency converter  endpoint

Online currency converter, providing a Web API endpoint with :
Flask is a lightweight WSGI web application framework.

## Documentation

Full documentation is available at [https://palletsprojects.com/p/flask/](https://palletsprojects.com/p/flask/).

## Overview
  currency_api read online xml date form https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml
  create in locale xml file `file.xml` to tranfome the xml data in the dictionary using the method readXml().
  ```py
  class convertor():
    def get_file(self):
          with urllib.request.urlopen(src_url) as response, open(src_file, 'wb') as out_file:
              data = response.read() # a `bytes` object
              out_file.write(data)


    def readXml(self, data):
          import xml.etree.ElementTree as ET
          tree = ET.parse(data)
          root = tree.getroot()
          for elem in root:
              for subelem in elem:
                  get_date = subelem.attrib.get('time')
                  if get_date:
                      dateCurrency={}
                      for sub in subelem:
                          dateCurrency[sub.attrib.get('currency')]=float(sub.attrib.get('rate'))
                      self.currencyData[get_date]=dateCurrency          
  ```
  This dictionary self.currencyData is used to provide data to the method currencyConverter for rending json data 
  ```py
  def currencyConverter(self,var_src_currency,var_montant,var_dest_currency,var_ference_date):
        rest = {}
        if var_src_currency == None or var_dest_currency == None or var_ference_date == None or var_montant == None:
            msg = 'One or more parameters are null',
            rest = {'amount':var_montant,
            'src_currency':var_src_currency,
            'dest_currency':var_dest_currency,
            'ference_date':var_ference_date, 
            'Message error':  msg }
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
```
## Example
The endPoint return Json data
  {
  amount: 20.00,
  currency: "EUR"
  }
  convert to currency CBP dat to 2019-10-14
  
url like :
  http://localhost:5000/converter?amount=20.00&src_currency=EUR&dest_currency=gbp&ference_date=2019-10-14
  or
  http://localhost:5000/converter/amount/20.00/src_currency/eur/dest_currency/GBP/ference_date/2019-10-14

return somehing like :
```Json
  {
  amount: 17.6,
  currency: "GBP"
  }
```
## Installation

From inside your project folder, run:

Download and install python 3+ : 
https://www.python.org/downloads/

```bash
$ pip install flask
```

To install the web components polyfills needed for older browsers:

```bash
$ python converter.py
```
if the serve don't run try with,
Start the application as follows:

FLASK_APP=converter.py FLASK_DEBUG=1 flask run


