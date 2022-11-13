from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
# https://www.trolley.co.uk/search/?from=search&q=sugar

# Create your views here.
def index(request):
	return render(request, "index.html")
	if request.method=="POST":
		return search(request)

def search(request):
	#list_of_search_strings = ["milk", "pear", "sugar", "bottle gourd", "apples", "oranges", "brussel sprouts"]
	search_string = request.POST['search_string']
	list_of_search_strings = search_string.split(",")
	for i in range(len(list_of_search_strings)):
		list_of_search_strings[i].strip()
	list_of_search_strings.remove("")
	print(list_of_search_strings)
	returnArray = []

	for searchString in list_of_search_strings:
	    searchString.replace(" ", "+")
	    URL = "https://www.trolley.co.uk/search/?from=search&q=" + searchString
	    page = requests.get(URL)
	    soup = BeautifulSoup(page.content, "html.parser")
	    results = soup.find_all("div", class_="product-item")
	   
	    returnArray.append({"search_name": searchString.title(), "results": []})

	    number_of_outer_results = 3

	    for j in range(number_of_outer_results):
	        productURL = "https://www.trolley.co.uk/" + results[j].find("a", class_=None).get("href")

	        tempDict = dict()
	        tempDict["item_name"] = results[j].find("div", class_="_brand").text
	        tempDict["item_des"] = results[j].find("div", class_="_desc").text
	        tempDict["supermarkets"] = []

	        productPage = requests.get(productURL)
	        productSoup = BeautifulSoup(productPage.content, "html.parser")

	        storeResults = productSoup.find_all("title", class_=None)
	        storeResults.pop(0)

	        productPriceResults = productSoup.find_all("b", class_=None)
	        productPriceResults = [i for i in productPriceResults if "£" in str(i)]

	        for i in range(len(storeResults)):
	            tmpArray = []
	            tmpArray.append(storeResults[i].text)
	            tmpArray.append(productPriceResults[i].text.split(" ")[0])
	            tempDict["supermarkets"].append(tmpArray)

	        returnArray[len(returnArray) - 1]["results"].append(tempDict)

	    context = {'table_info' : returnArray}

	return render(request, "results.html", context)

		# 'table_info' : [{"search_name" : "milk", "results" : [{"item_name": "Cravendale", "item_des": "Fat Milk", "supermarkets":[["ASDA", "£2"], ["Sainsbury's", "£3"], ["Tesco", "£4"]]},
		# {"item_name": "Asla", "item_des": "Fat Milk", "supermarkets":[["ASDA", "£2.5"], ["Sainsbury's", "£3.5"], ["Tesco", "£4.5"]]}]},

		# {"search_name" : "eggs", "results" : [{"item_name": "Cravendale", "item_des": "12 eggs", "supermarkets":[["ASDA", "£4"], ["Sainsbury's", "£5"], ["Tesco", "£3"]]},
		# {"item_name": "Cravendale", "item_des": "6 eggs", "supermarkets":[["ASDA", "£2"], ["Sainsbury's", "£2"], ["Tesco", "£1"]]}]}
		# ]
		# }