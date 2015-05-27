# Jerry Crowley
# Auctions America Scraper

from lxml import html
from selenium import webdriver
import requests
import cookielib
import urllib
import urllib2

class Car:
	auctionHouse = ""
	auction = ""
	image = []
	lot = ""
	year = 0
	make = ""
	model = ""
	description = ""
	fullName = ""
	salePrice = 0
	highBid = 0
	
	def __init__(self, auctionHouse, auction, image, lot, year, make, model, description, fullName, salePrice, highBid):
		self.auctionHouse = auctionHouse
		self.auction = auction
		self.image = image
		self.lot = lot
		self.year = year
		self.make = make
		self.model = model
		self.description = description
		self.fullName = fullName
		self.salePrice = salePrice
		self.highBid = highBid

def make_car(auctionHouse,auction,image,lot,year,make,model,description,fullName, salePrice, highBid):
	car = Car(auctionHouse,auction,image,lot,year,make,model,description,fullName, salePrice, highBid)
	return car

def getData(fullAuctionName, url):
	path_to_chromedriver = '/Users/jerry/Desktop/chromedriver'
	browser = webdriver.Chrome(executable_path = path_to_chromedriver)
	
	browser.get(url)

	#Get Car
	fullName = browser.find_element_by_css_selector('#leftCol > div.tab_content > div.contentBlock > h3').text
	
	#Get Lot
	lotString = browser.find_element_by_css_selector('#leftCol > div.tab_content > div.contentBlock > p:nth-child(6) > strong').text
	lot = lotString.replace("Lot No. ","").strip()
	
	#Get Price
	tempString = browser.find_element_by_css_selector('#featureDescription').text
	priceString = tempString.replace(',','').split(" ")
	priceString1 = priceString[(len(priceString)-1)].replace("u'","").replace("'","").replace("$","")
	price = int(priceString1)
	
	#Sold or Not
	if("sold" in tempString):
		salePrice = price
		highPrice = price
	elif("bid" in tempString):
		salePrice = None
		highPrice = price
	else:
		salePrice = None
		highPrice = None

	#Get year
	newTempString = fullName.strip().split(" ")
	if(newTempString[0].isdigit()):
		year = int(newTempString[0])
		make = newTempString[1]
	else:
		year = None
		make = newTempString[0]

	#Get Images
	img = browser.find_element_by_css_selector('#slides').find_elements_by_tag_name('img')
	images = []

	for link in img:
		try:
			tempString = link.get_attribute('src')
			linkString = tempString.replace("u'","").replace("'","")
			images.append(linkString)
		except:
			break;

	browser.close()

	tempCar = make_car('Auctions America',fullAuctionName,images,lot,year,make,None,None,fullName,salePrice,highPrice)
	return (tempCar)

def auctionsAmericaScrapper():
	#auctionAbbreviation = input('Enter auction abbrev: ')
	#auction = input('Enter full auction name: ')
	auctionAbbreviation = 'af14'
	auction = 'Auburn 2014'
	
	#Fetch data
	page = requests.get('http://www.auctionsamerica.com/events/all-lots.cfm?SaleCode='+auctionAbbreviation+'&search=&category=vehicles&year=&make=&model=&collection=&day=&order=price&noreserve=&feature=&stillforsale=&grouping=&rowsperpage=')
	tree = html.fromstring(page.text)
	cars = []

	for x in range(2,5):
		try:
			tempString = str(x)
			seq = ('//*[@id="lotsContent"]/div[',']/@onclick')
			url = tree.xpath(tempString.join(seq))
			url1 = url[0].replace('location.href=','')
			newUrl = ('http://www.auctionsamerica.com'+((url1.strip().replace("'",""))))
			cars.append(getData(auction,newUrl))
		except:
			break

	for car in cars:
		print("LOT: ",car.lot,"\t\t","YEAR: ",car.year,"\t\t","CAR: ",car.fullName)

def main():
	auctionsAmericaScrapper()

main()