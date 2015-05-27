# Jerry Crowley
# Gooding Scraper

from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

def getData(auction,url):
	path_to_chromedriver = '/Users/jerry/Desktop/chromedriver'
	browser = webdriver.Chrome(executable_path = path_to_chromedriver)
	
	browser.get(url)

	#Car full name
	wait = WebDriverWait(browser, 10)
	fullName = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#homeshow > div:nth-child(5) > div > h1'))).text

	#Get Year
	tempString = fullName.strip()
	newTempString = tempString.split(" ")
		
	if(newTempString[0].isdigit()):
		year = int(newTempString[0])
		make = newTempString[1]
	else:
		year = None
		make = newTempString[0]

	#Get lot
	lotString = browser.find_element_by_css_selector('#specs > div:nth-child(1) > div:nth-child(1) > div > a').text
	tempLotString = lotString.split(" ")
	lot = tempLotString[1]

	#Get price
	priceString = browser.find_element_by_css_selector('#specs > div:nth-child(1) > div:nth-child(5) > div.soldprice > strong').text
	tempPriceString = priceString.split(" ");
	tempString = tempPriceString[1].replace("$","").replace(",","")
	price = int(tempString)

	#Get images
	img = browser.find_element_by_css_selector('body > div.gallery').find_elements_by_tag_name('a')
	images = []

	for link in img:
		try:
			tempString = link.get_attribute('href')
			images.append(tempString)
		except:
			break

	browser.close()
	tempCar = make_car('Gooding & Company',auction,images,lot,year,make,None,None,fullName,price,price)
	return (tempCar)

def goodingScrapper():
	url = 'http://www.goodingco.com/results/realized/?cat=35'
	
	#Fetch cars
	page = requests.get(url)
	tree = html.fromstring(page.text)
	cars = []
	
	for x in range(1,4):
		try:
			auctionText = tree.xpath('/html/body/div[3]/div/div[1]/h2/text()')
			auction = auctionText[0]
			carUrl = tree.xpath('/html/body/div[3]/div/div[1]/div[2]/ul/a['+str(x)+']/@href')
			url1 = carUrl[0].replace("'","")
			cars.append(getData(auction,url1))
		except:
			break

	for car in cars:
		print "LOT: %s \t\t YEAR: %d \t\t CAR: %s" % (car.lot,car.year,car.fullName)


def main():
	goodingScrapper()
main()