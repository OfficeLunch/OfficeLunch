import os
import sys
import json

#add into hashmap for unique tags and value numbers
def sortRestaurants(metatags,response):
	metaList = {}
	listofBusiness = []
	weightList = {}
	for tag in metatags:
		if not tag in metaList:
			metaList[tag] = 1
		else:
			metaList[tag] += 1

    for x in response.businesses:
    	print x.categories
    	for key in metaList:
    		if(x.categories in key):
                listofBusiness.append(x)

    for dictionary in listofBusiness:
        for listCategories in dictionary.categories:
        	if cat in listCategories:
                if not dictionary.name in weightList:
                    weightList[dictionary.name] = 1
                else:
                    weightList[dictionary.name] += 1

    return listofBusiness[:10]		

def unitTest(phrase):
	return phrase + "hi"