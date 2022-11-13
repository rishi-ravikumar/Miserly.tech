from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def index(request):
	# return render(request, "index.html")
	# if request.method=="POST":
		return search(request)

def search(request):
	return render(request, "sample.html", {
		'table_info' : [{"search_name" : "milk", "results" : [{"item_name": "Cravendale", "item_des": "Fat Milk", "supermarkets":[["ASDA", "£2"], ["Sainsbury's", "£3"], ["Tesco", "£4"]]},
		{"item_name": "Asla", "item_des": "Fat Milk", "supermarkets":[["ASDA", "£2.5"], ["Sainsbury's", "£3.5"], ["Tesco", "£4.5"]]}]},

		{"search_name" : "eggs", "results" : [{"item_name": "Cravendale", "item_des": "12 eggs", "supermarkets":[["ASDA", "£4"], ["Sainsbury's", "£5"], ["Tesco", "£3"]]},
		{"item_name": "Cravendale", "item_des": "6 eggs", "supermarkets":[["ASDA", "£2"], ["Sainsbury's", "£2"], ["Tesco", "£1"]]}]}
		]
		})
