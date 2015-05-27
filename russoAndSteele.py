# Jerry Crowley
# Russo And Stelle Scraper

from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
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

def getNumberOfPages(url):
	#Fetch data
	page = requests.get(url)
	tree = html.fromstring(page.text)
	
	#Get the number of Pages
	getPageNumbers = tree.xpath('//*[@id="table"]/div[22]/a/text()')
	return int(getPageNumbers[len(getPageNumbers)-1])

def getData(browser,url,price,auction):
	browser.get(url)

	#Get full name
	fullName = browser.find_element_by_css_selector('body > div.wrapper > div > div > div.content_inner > div.full_width > div > div:nth-child(1) > div > div > div > div > div > ul > li > div > div > div > div > div > div > div > div:nth-child(3) > div.column1 > div > span:nth-child(1)').text
	print('Started %s')%(fullName)
	
	#Get year
	tempString = fullName.strip()
	newTempString = tempString.split(" ")
		
	if(newTempString[0].isdigit()):
		year = int(newTempString[0])
		make = newTempString[1]
		modelList = newTempString[2:]
		model = ' '.join(modelList)
	else:
		year = None
		make = newTempString[0]
		modelList = newTempString[1:]
		model = ' '.join(modelList)

	#Get lot number
	lotNum = browser.find_element_by_css_selector('body > div.wrapper > div > div > div.content_inner > div.full_width > div > div:nth-child(1) > div > div > div > div > div > ul > li > div > div > div > div > div > div > div > div:nth-child(3) > div.column1 > div > span:nth-child(3)').text

	#Clean up lot number
	tempString = lotNum.split(" ")
	lot = tempString[2]

	#Get Images
	img = browser.find_element_by_css_selector('#gallery-1').find_elements_by_tag_name('a')
	images = []

	#Get Description
	description = browser.find_element_by_css_selector('body > div.wrapper > div > div > div.content_inner > div.full_width > div > div:nth-child(1) > div > div > div > div > div > ul > li > div > div > div > div > div > div > div > div:nth-child(4) > div.column1 > div > div:nth-child(3) > p').text

	for link in img:
		images.append(link.get_attribute('href'))

	print('Finished %s %s')%(make,model)

	tempCar = make_car('Russo And Steele',auction,images,lot,year,make,model,description,fullName,price,price)
	return tempCar

def russoAndStelleScraper(auction,link):
	print('Scrapping %s!')%(auction)
	path_to_chromedriver = '/Users/jerry/Desktop/chromedriver'
	browser = webdriver.Chrome(executable_path = path_to_chromedriver)
	url = link+'&showpage=1'
	
	pageNum = getNumberOfPages(url)
	print('Number of Pages: %d')%(pageNum)
	signInFlag = 0
	cars = []
	
	for page in range(1,pageNum+1):
		print('On Page: %d')%(page)
		browser.get(link+'&showpage='+str(page))
		numOfCars = browser.find_elements_by_xpath('//*[@id="table"]/div')
		
		#print('NUM OF CARS: %d')%(len(numOfCars))

		if(signInFlag == 0):
			print('Signing In....')
			signInFlag = signInFlag + 1
			browser.find_element_by_css_selector("#table > div:nth-child(1) > div.column1 > div > div > div.column2 > div > div > a").click()
			
			firstName = browser.find_element_by_css_selector("#member_first_name")
			lastName = browser.find_element_by_css_selector("#member_last_name")
			email = browser.find_element_by_css_selector("#member_email")
			
			firstName.send_keys("FirstName")
			lastName.send_keys("LastName")
			email.send_keys("email@mail.com")
			
			browser.find_element_by_css_selector("#member_form > div > button:nth-child(1)").click()
	
		for car in range(1,(len(numOfCars)-2)):
			browser.get(link+'&showpage='+str(page))
			wait = WebDriverWait(browser, 30)

			#Get price
			price = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#table > div:nth-child('+str(car)+') > div.column1 > div > div > div.column2 > div > div > b'))).text
			
			#Clean up price to turn into integer
			tempString = price.split(" ")
			tempString1 = tempString[1].split(".")
			newPriceString = tempString1[0].replace("$","")
			price = newPriceString.replace(",","")
			
			#Get URL to get images
			url = browser.find_element_by_xpath('//*[@id="table"]/div['+str(car)+']/div[2]/div/a').get_attribute('href')
			tempCar = getData(browser,url,price,auction)
			cars.append(tempCar)
		
	browser.close()

def getPastResults():
	print('Loading Previous Results')
	url = 'https://russoandsteele.com/results/'
	page = requests.get(url)
	tree = html.fromstring(page.text)

	oddCounter = 1;
	oddLinkCounter = 2;
	
	evenCounter = 4;
	evenLinkCounter = 5;
	
	for x in range(1,3):
		if(x%2!=0):
			auction = tree.xpath('/html/body/div[2]/div/div/div[2]/div[2]/div/section['+str(oddCounter)+']/div/div/div[1]/div/div[2]/div/p[1]/span/b/text()')
			link = tree.xpath('/html/body/div[2]/div/div/div[2]/div[2]/div/section['+str(oddLinkCounter)+']/div/div/div[1]/div/div/div/div[2]/div/a/@href')
			oddCounter = oddCounter + 2
			oddLinkCounter = oddLinkCounter + 2
		else:
			auction = tree.xpath('/html/body/div[2]/div/div/div[2]/div[2]/div/div['+str(evenCounter)+']/div/div/div[1]/div/div[2]/div/p[1]/span/b/text()')
			link = tree.xpath('/html/body/div[2]/div/div/div[2]/div[2]/div/div['+str(evenLinkCounter)+']/div/div/div[1]/div/div/div/div[2]/div/a/@href')
			if not auction:
				auction = tree.xpath('/html/body/div[2]/div/div/div[2]/div[2]/div/div['+str(evenCounter)+']/div/div/div[1]/div/div[2]/div/p[1]/span/strong/text()')
			evenCounter = evenCounter + 4
			evenLinkCounter = evenLinkCounter + 4

		print('Got Auction: %s')%(auction[0])
		russoAndStelleScraper(auction[0],link[0])

def main():
	print('Welcome to Russo and Stelle Scanner!')
	getPastResults()

	auction = input("Auction Name: ")
	link = input("Link to results: ")

main()