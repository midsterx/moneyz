from bs4 import BeautifulSoup
from requests import get
from multiprocessing import Pool
import time

'''
In case you don't have them already

pip install beautifulsoup4
pip install requests
pip install multiprocessing
''' 

f=open("links.txt","r")
links=f.readlines()
links=[link[0:len(link)-1] for link in links]

#for url in links:
	#url="http://www.moneycontrol.com/india/stockpricequote/diversified/3mindia/MI42"
def f(url):
	try:
		data=get(url).text
		soup=BeautifulSoup(data,"lxml")
		title=soup.find(class_="b_42 company_name").text #company name
		bse=soup.find(id="Bse_Prc_tick").text #BSE price
		bse_pclose=soup.find(id="b_prevclose").text #previous closing price
		bse_open=soup.find(id="b_open").text #opening price
		bse_bid=soup.find(id="b_bidprice_qty").text 
		bse_bid_price=bse_bid[0:bse_bid.index("(")-1] #bid price
		bse_bid_qty=bse_bid[bse_bid.index("(")+1:bse_bid.index(")")] #bid quantity
		bse_offer=soup.find(id="b_offerprice_qty").text #offer price
		bse_offer_price=bse_offer[0:bse_offer.index("(")-1] #offer quantity
		bse_offer_qty=bse_offer[bse_offer.index("(")+1:bse_offer.index(")")]

		nse=soup.find(id="Nse_Prc_tick").text # same prices for NSE
		nse_pclose=soup.find(id="b_prevclose").text
		nse_open=soup.find(id="b_open").text
		nse_bid=soup.find(id="b_bidprice_qty").text
		nse_bid_price=nse_bid[0:nse_bid.index("(")-1]
		nse_bid_qty=nse_bid[nse_bid.index("(")+1:nse_bid.index(")")]
		nse_offer=soup.find(id="b_offerprice_qty").text
		nse_offer_price=nse_offer[0:nse_offer.index("(")-1]
		nse_offer_qty=nse_offer[nse_offer.index("(")+1:nse_offer.index(")")]
		return([(title,bse,bse_pclose,bse_open,bse_bid_price,bse_bid_qty,bse_offer_price,bse_offer_qty),(title,nse,nse_pclose,nse_open,nse_bid_price,nse_bid_qty,nse_offer_price,nse_offer_qty)])
	except:
		print(url)

p=Pool(10) #for multiprocessing-speeds up scraping by spawning multiple processes
r=p.map(f,links)
p.terminate()
p.join()