# Jerry Crowley
# Barret Jackson Scraper

from lxml import html
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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

def getData(auction,url,browser):
	browser.implicitly_wait(10) # seconds
	
	browser.get(url)

	wait = WebDriverWait(browser,30)

	try:
		#Car full name
		fullName = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'body > div:nth-child(4) > div:nth-child(2) > div.span9 > div > div.segment_box_inner > h1'))).text
	except:
		return None

	#Car Make/Model
	make = browser.find_element_by_css_selector('#Make').text
	model = browser.find_element_by_css_selector('#Model').text

	#Get Year
	yearText = browser.find_element_by_css_selector('#Year').text
	year = int(yearText)

	#Get lot
	lot = browser.find_element_by_css_selector('#Lot').text

	#Get price
	priceString = browser.find_element_by_css_selector('#Price').text
	tempString = priceString.replace("$","").replace(",","").split('.')
	try:
		price = int(tempString[0])
	except:
		price = tempString[0]

	#Sold or Not
	status = browser.find_element_by_css_selector('#Status').text
	if("sold" in status):
		salePrice = price
		highPrice = price
	else:
		salePrice = None
		highPrice = price

	#Get images
	try:
		img = browser.find_element_by_css_selector('body > div:nth-child(4) > div:nth-child(2) > div.span9 > div > div:nth-child(6) > div.span8 > div > div.bj-car-items-wrapper > div.bj-car-carousel-items.slick-initialized.slick-slider > div > div').find_elements_by_tag_name('img')
		images = []

		for link in img:
			try:
				tempString = link.get_attribute('src')
				linkString = tempString.replace("u'","").replace("'","")
				images.append(linkString)
			except:
				break;
	except:	
		print('No Images for %s')%(fullName)
		images = None	

	tempCar = make_car('Barrett-Jackson',auction,images,lot,year,make,model,None,fullName,salePrice,highPrice)
	print('%d: Finished %s')%(len(cars),tempCar.fullName)
	return (tempCar)

def numOfElements(url):
	path_to_chromedriver = '/home/jerry/Desktop/chromedriver'
	browser = webdriver.Chrome(executable_path = path_to_chromedriver)
	
	browser.get(url)
	temp = browser.find_elements_by_class_name('media-body')
	browser.close()
	return len(temp)

def barretJacksonScrapper(auction,url):
	print('STARTING: %s')%(auction)
	#Fetch cars
	page = requests.get(url)
	tree = html.fromstring(page.text)

	numElements = numOfElements(url)
	flag = False 

	while flag == False:
		try:	
			print('CONNECTING!')
			path_to_chromedriver = '/home/jerry/Desktop/chromedriver'
			browser = webdriver.Chrome(executable_path = path_to_chromedriver)
			flag = True
		except:
			print('Failed to Connect!')
			print('Trying Again......')

	counter = 1
	
	#top = Element('top')
	#comment = Comment('BARRET JACKSON')
	#top.append(comment)
	
	for x in range(1,numElements):
		try:
			if ( (counter%100) == 0):
				connectFlag = False
				browser.close()
				while connectFlag == False: 
					try:	
						print('Reconnecting to the chrome driver')
						path_to_chromedriver = '/home/jerry/Desktop/chromedriver'
						browser = webdriver.Chrome(executable_path = path_to_chromedriver)
						connectFlag = True
					except:
						print('Failed to Connect!')
						print('Trying Again......')

			carUrl = tree.xpath('//*[@id="search-results"]/div[1]/div['+str(x)+']/div/h2/a/@href')
			url1 = carUrl[0].replace("'","")
			newUrl = ('http://www.barrett-jackson.com'+url1)
			tempCar = getData(auction,newUrl,browser)
			if tempCar != None:
				cars.append(tempCar)
			counter = counter + 1
		except:
			print('SOMETHING WENT WRONG! TRYING AGAIN!')
			connectFlag = False
			while connectFlag == False:
				try:
					print('Reconnecting to the chrome driver')
					path_to_chromedriver = '/home/jerry/Desktop/chromedriver'
					browser = webdriver.Chrome(executable_path = path_to_chromedriver)
					connectFlag = True
				except:
					print('Failed to Connect!')
					print('Trying Again......')

		'''
		child = SubElement(top, 'car')
		child.text = tempCar.fullName
			
		child1 = SubElement(child,'auctionHouse')
		child1.text = tempCar.auctionHouse

		child2 = SubElement(child,'auction')
		child2.text = tempCar.auction
			
		child4 = SubElement(child,'lot')
		child4.text = tempCar.lot

		child5 = SubElement(child,'year')
		child5.text = tempCar.year

		child6 = SubElement(child,'make')
		child6.text = tempCar.make

		child7 = SubElement(child,'model')
		child7.text = tempCar.model

		child8 = SubElement(child,'description')
		child8.text = tempCar.description

		child9 = SubElement(child,'fullname')
		child9.text = tempCar.fullName

		child10 = SubElement(child,'salePrice')
		child10.text = tempCar.salePrice

		child11 = SubElement(child,'highBid')
		child11.text = tempCar.highBid
	
		child3 = SubElement(child,'image')
		for image in tempCar.images:
			child3.text = tempCar.auctionHouse'''
	browser.close()
	print ('DONE WITH %s')%(auction)

def getPreviousResults():
	print 'GETTING PREVIOUS'
	page = requests.get('http://www.barrett-jackson.com/Archive/Home')
	tree = html.fromstring(page.text)
	
	for x in range(1,28):
		#Get Auction
		auction = tree.xpath('//*[@id="bj-predefined-searches"]/div['+str(x)+']/div/div[1]/div/h2/text()')
		
		#Get Link
		link = tree.xpath('//*[@id="bj-predefined-searches"]/div['+str(x)+']/div/div[2]/div/a/@href')
		
		newPage = requests.get('http://www.barrett-jackson.com'+link[0])
		newTree = html.fromstring(newPage.text)
		
		finalLink = newTree.xpath('/html/body/div[3]/div/div[1]/div/a/@href')
		print('Scrapping %s')%(auction[0].strip())
		barretJacksonScrapper(auction[0].strip(),('http://www.barrett-jackson.com'+finalLink[0]))

def main():
	global cars
	cars = []
	getPreviousResults()
	for car in cars:
		print "AUCTION: %s \t\t LOT: %s \t\t YEAR: %d \t\t Make: %s \t\t Model: %s" % (car.auction,car.lot,car.year,car.make,car.model)
	print('FINISHED! Scrapped %d cars')%(len(cars))

'''
	print('Welcome to the Barrett-Jackson Scanner!')
	auction = input('Please type in the auction name')
	link = input('Please type in the link to the dockett')

	barretJacksonScrapper(auction,link)'''
main()
