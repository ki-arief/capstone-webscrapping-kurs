from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('tbody')
table_exc_rates = table.find_all('a', attrs= {'class':'w'} )
row_length = len(table_exc_rates)

temp = [] #initiating a list 

for i in range(1, row_length):
#insert the scrapping process here
    #scrapping process
    #get tanggal 
   tanggal = table.find_all('a', attrs={'class':'n'})[i].text
    
    #get kurs
   kurs = table.find_all('span', attrs={'class':'w'})[i].text
       
   temp.append((tanggal, kurs))
    
temp = temp[::-1]

#change into dataframe
inflation_rate = pd.DataFrame(temp, columns=('tanggal', 'kurs'))

#insert data wrangling here
inflation_rate['kurs'] = inflation_rate['kurs'].str[-6:]
inflation_rate['kurs'] = inflation_rate['kurs'].str.replace(',', '')
inflation_rate['tanggal'] = inflation_rate['tanggal'].astype('datetime64[ns]')
inflation_rate['kurs'] = inflation_rate['kurs'].astype('float64')

inflation_rate = inflation_rate.set_index('tanggal')
#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{inflation_rate["kurs"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = inflation_rate.plot(figsize = (12,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)