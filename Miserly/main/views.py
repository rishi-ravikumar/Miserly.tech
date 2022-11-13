from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from parse_ingredients import parse_ingredient
import unicodedata
# https://www.trolley.co.uk/search/?from=search&q=sugar

# Create your views here.
def index(request):
	# if request.method=="POST":
	# 	return search(request)
	return render(request, "index.html")

def search(request):
	#list_of_search_strings = ["milk", "pear", "sugar", "bottle gourd", "apples", "oranges", "brussel sprouts"]
	search_string = request.POST['search_string']
	if(search_string)=="":
		return render(request, "error.html")
	list_of_search_strings = search_string.split(',')
	for i in range(len(list_of_search_strings)):
		list_of_search_strings[i] = list_of_search_strings[i].strip()
	while(list_of_search_strings.count('')>0):
		list_of_search_strings.remove('')
	while(list_of_search_strings.count('hot water')>0):
		list_of_search_strings.remove('hot water');
	returnArray = []

	for searchString in list_of_search_strings:
	    searchString.replace(" ", "+")
	    URL = "https://www.trolley.co.uk/search/?from=search&q=" + searchString
	    page = requests.get(URL)
	    soup = BeautifulSoup(page.content, "html.parser")
	    results = soup.find_all("div", class_="product-item")
	   
	    returnArray.append({"search_name": searchString.title(), "results": []})

	    number_of_outer_results = 3

	    for j in range(min(number_of_outer_results, len(results))):
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

	        for i in range(len(productPriceResults)):
	            tmpArray = []
	            tmpArray.append(storeResults[i].text)
	            tmpArray.append(productPriceResults[i].text.split(" ")[0])
	            tempDict["supermarkets"].append(tmpArray)

	        returnArray[len(returnArray) - 1]["results"].append(tempDict)
	if(returnArray)==[]:
		return render(request, "error.html")
	context = {'table_info' : returnArray}

	return render(request, "results.html", context)

		# 'table_info' : [{"search_name" : "milk", "results" : [{"item_name": "Cravendale", "item_des": "Fat Milk", "supermarkets":[["ASDA", "£2"], ["Sainsbury's", "£3"], ["Tesco", "£4"]]},
		# {"item_name": "Asla", "item_des": "Fat Milk", "supermarkets":[["ASDA", "£2.5"], ["Sainsbury's", "£3.5"], ["Tesco", "£4.5"]]}]},

		# {"search_name" : "eggs", "results" : [{"item_name": "Cravendale", "item_des": "12 eggs", "supermarkets":[["ASDA", "£4"], ["Sainsbury's", "£5"], ["Tesco", "£3"]]},
		# {"item_name": "Cravendale", "item_des": "6 eggs", "supermarkets":[["ASDA", "£2"], ["Sainsbury's", "£2"], ["Tesco", "£1"]]}]}
		# ]
		# }

def recipe_search(request):
	return render(request, "recipeIndex.html") 

def recipe_result(request):
	ingredients = []
	returnDict = dict()
	searchString = request.POST['search_string']
	if(searchString)=="":
		return render(request, "error.html")
	searchURL = "https://tasty.co/search?q=" + searchString.replace(" ", "+") + "&sort=popular"
	page = requests.get(searchURL)
	soup = BeautifulSoup(page.content, "html.parser")

	searchResults = soup.find("li", class_="feed-item")
	if(searchResults == None):
	    return render(request, "error.html")
	urlExtension = searchResults.find("a", class_=None).get("href")
	recipeTitle = urlExtension.split("/")[-1].replace("-", " ").title()
	returnDict["recipe_title"] = recipeTitle
	resultURL = "https://tasty.co/" + urlExtension
	returnDict["recipe_url"] = resultURL
	recipeTitle = soup.find("div", _class="feed-item__title")

	recipePage = requests.get(resultURL)
	recipeSoup = BeautifulSoup(recipePage.content, "html.parser")
	ingredientsSection = recipeSoup.find("div", class_="ingredients-prep")
	ingredients = ingredientsSection.find_all("li", class_="ingredient")

	returnDict["ingredients"] = []

	for ing in ingredients:
	    if(any(char.isdigit() for char in str(ing.contents[0])) or any(unicodedata.name(char).startswith('VULGAR FRACTION') for char in str(ing.contents[0]))):
	        returnDict["ingredients"].append(str(ing.contents[2]))
	    else:
	        returnDict["ingredients"].append(str(ing.contents[0]))

	if(returnDict)==[]:
		return render(request, "error.html")
	context = {'table_info' : returnDict}

	return render(request, "recipeResult.html", context)

#{'recipe_title': 'Pav Bhaji', 'recipe_url': 'https://tasty.co//recipe/pav-bhaji', 'ingredients': ['coriander seed', 'cumin seeds', 'whole clove', 'cinnamon stick', 'whole black peppercorn', 'fennel seeds', 'cardamom pods', 'fresh ginger', 'garlic cloves', 'yukon gold potatoes', 'beefsteak tomatoes', 'frozen english peas', 'ground turmeric', 'chile powder', 'cold water', 'kosher salt', 'paprika', 'cayenne', 'unsalted butter', 'red onion', 'jalapeñoes', 'tomato paste', 'fresh cilantro', 'soft buns', 'lemon wedge', 'spice grinder', 'potato masher']}