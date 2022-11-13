from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name='index'),
	path("search/", views.search, name='search'),
	path("recipe-search/", views.recipe_search, name='recipe_search'),
	path("recipe-result/", views.recipe_result, name='recipe_result'),
]

