from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def index(request):
	# return render(request, "homepage.html")
	# if request.method=="POST":
		return search(request)

def search(request):
	return render(request, "sample.html", {
		'table_info' : [{"name": "milk", "supermarkets":[["ASDA", "£2"], ["Sainsbury's", "£3"], ["Tesco", "£4"]]},
		{"name": "eggs", "supermarkets":[["ASDA", "£1"], ["Sainsbury's", "£2"], ["Tesco", "£3"]]}]
		})
