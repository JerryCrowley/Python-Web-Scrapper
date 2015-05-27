# Jerry Crowley
# Mecum Scraper

from lxml import html
from selenium import webdriver
#import sys
#from PyQt4.QtGui import *
#from PyQt4.QtCore import *
#from PyQt4.QtWebKit import *
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

def getNumberOfPages(auction):
	#Fetch data
	page = requests.get('https://www.mecum.com/view-lots.cfm?auctionid='+auction+'&featureValue=ALL&page=1')
	tree = html.fromstring(page.text)
	
	#Get the number of Pages
	getPageNumbers = tree.xpath('//*[@id="public"]/div[1]/div[2]/table/tr/td[2]/div[1]/div/span/text()')
	pageNum = getPageNumbers[0].split( );
	
	returnList = [int(pageNum[3]),tree]

	return(returnList)

def getImages(url):
	path_to_chromedriver = '/Users/jerry/Desktop/chromedriver'
	browser = webdriver.Chrome(executable_path = path_to_chromedriver)

	browser.get(url)
	img = browser.find_element_by_css_selector('#slider1_container > div > div > div:nth-child(2)').find_elements_by_tag_name("div")
	
	images = []

	for link in img:
		try:
			images.append(link.get_attribute('innerHTML').split('"')[3].replace("u'",""))
		except:
			browser.close()
			break;

	return(images)

def mecumScraper(fullAuctionName,auction):
	#auction = input('Enter auction: ')
	
	# Store the cookies and create an opener that will hold them
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		
	# Add our headers
	opener.addheaders = [('User-agent', 'MecumTesting')]
	
	# Install our opener (note that this changes the global opener to the one
	# we just made, but you can also just call opener.open() if you want)
	urllib2.install_opener(opener)
	
	# The action/ target from the form
	authentication_url = 'https://www.mecum.com//infonet-login-action.cfm'
	
	# Input parameters we are going to send
	payload = {
		'email': 'jaxjags1767@yahoo.com',
	}
	
	# Use urllib to encode the payload
	data = urllib.urlencode(payload)
	binary_data = data.encode('utf-8')
	
	# Build our Request object (supplying 'data' makes it a POST)
	req = urllib2.Request(authentication_url, binary_data)
	
	# Make the request and read the response
	resp = urllib2.urlopen(req)

	cars = []

		
	#Get number of pages to traverse
	returnedFromgetNumOfPages = getNumberOfPages(auction)
	numPages = returnedFromgetNumOfPages[0]

	for x in range(1,2):
		newReq1 = opener.open('https://www.mecum.com/view-lots.cfm?auctionid='+auction+'&featureValue=ALL&page='+str(x))
		tree1 = html.fromstring(newReq1.read())
		
		for y in range(1,3):
			try:
				url = tree1.xpath('//*[@id="public"]/div[1]/div[2]/table/tr/td[2]/div[2]/ul['+str(y)+']/li[3]/a/@href')
				newUrl = ('https://www.mecum.com'+((url[0].strip().replace('"',''))))
				newReq = opener.open(newUrl)
				tree = html.fromstring(newReq.read())
				
				lot = tree.xpath('//*[@id="public"]/div[1]/div[2]/div/div[1]/h1/span[1]/text()')
				price = tree.xpath('//*[@id="public"]/div[1]/div[2]/div/div[1]/h1/span[6]/text()')
				highOrSold = tree.xpath('//*[@id="public"]/div[1]/div[2]/div/div[1]/h1/span[6]/img/@src')
				other = tree.xpath('//*[@id="public"]/div[1]/div[2]/div/div[1]/h1/text()')
				description = tree.xpath('//*[@id="public"]/div[1]/div[2]/div/div[1]/h1/span[7]/text()')
				
				#Clear up lot
				tempString = lot[0].replace("Lot","")
				lotString = tempString.strip()
				
				#Clean up price to turn into integer
				tempString = price[1].strip()
				newPriceString = tempString.replace("$","")
				priceString = newPriceString.replace(",","")
				
				#Get images
				images = getImages(newUrl)
				for image in images:
					image.replace("u'","")

				#Get prices
				if("sold" in highOrSold[0]):
					salePrice = int(priceString)
					highPrice = int(priceString)
				elif("bgo" in highOrSold[0]):
					salePrice = None
					highPrice = int(priceString)
				else:
					salePrice = None
					highPrice = None
				
				#Get description
				if(len(description) == 0):
					descriptionStr = ""
				else:
					descriptionStr = description[0].strip()
				
				#Get year
				tempString = other[7].strip()
				newTempString = tempString.split(" ")
				
				if(newTempString[0].isdigit()):
					year = int(newTempString[0])
					make = newTempString[1]
				else:
					year = None
					make = newTempString[0]
				
			
				tempCar = make_car('Mecum',fullAuctionName,images,lotString,year,make,"",descriptionStr,other[7].strip(),salePrice,highPrice)
				cars.append(tempCar)
		
				print(other[7].strip())
			except:
				break

def getPreviousResults():
	
	file = open('testAuction.txt')

	for line in file:
		text_line = line.split(",")
		auction = text_line[0]
		fullAuctionName = text_line[1].split(".")
		fileName = text_line[1].rstrip('\n').strip()

		mecumScraper(fullAuctionName[0],auction)


def main():
	getPreviousResults()
	
	'''
	print('Welcome to Mecum Scrapper!')
	auction = input('Please enter auction name')
	auctionAbbrev = input('Please enter auction abbreviation')
	
	mecumScraper(auction,auctionAbbrev)
	'''
main()