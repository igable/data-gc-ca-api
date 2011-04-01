#!/usr/bin/python

# Copyright (C) 2011 Ian Gable
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

## Auth.: Ian Gable

import urllib
import sys
from xml.etree.ElementTree import ElementTree



class CityIndex:
    def __init__(self):
        # this class could be changed to pass these two
        # hardcoded paths in
        self.city_list_url =  "http://dd.weatheroffice.ec.gc.ca/citypage_weather/xml/siteList.xml"
        self.base_url = "http://dd.weatheroffice.ec.gc.ca/citypage_weather/xml/"
        self.cities = {}
        cityListTree = ElementTree()

        try:
            urlhandle = urllib.urlopen(self.city_list_url)
        except IOError:
            print "[Error] Unable to open the data url: " + self.city_list_url
            sys.exit(1)

        cityListTree.parse(urlhandle)
        siteList = cityListTree.findall("site")

        for site in siteList:
            cityNameEnglish = site.findtext("nameEn").encode('utf-8')
            
            self.cities[cityNameEnglish] = {\
                    'sitecode': site.attrib['code'].encode('utf-8'),\
                    'provincecode': site.findtext("provinceCode").encode('utf-8'),\
                    'nameFr': site.findtext("nameFr").encode('utf-8') }

            
    def isCity(self, name):
        """
        Returns True if name is a valid city
        """
        return name in self.cities

    def getDataUrl(self,name):
        """
        Returns resource URL for the city denoted by name
        """
        if self.isCity(name):
            return self.base_url + self.getProvince(name) + "/" + self.getSiteCode(name) + "_e.xml"
        return None

    def getProvince(self,name):
        """
        Returns Province code (e.g. 'ON', 'BC', etc) of the city denoted by name
        """
        if self.isCity(name):
            return self.cities[name]['provincecode']
        return None

    def getSiteCode(self,name):
        """
        Returns the environment canada site for a city. For example Athabasca, AB
        has the site code s0000001
        """
        if self.isCity(name):
            return self.cities[name]['sitecode']
        return None
    
    def getFrenchName(self,name):
        if self.isCity(name):
            return self.cities[name]['nameFr']
        return None

    def getEnglishCityList(self):
        return self.cities.keys()

    def getFrenchCityList(self):
        return [v['nameFr'] for k, v in self.cities.iteritems()]


class City():

    # note that we are are grabbing a different 
    # data URL then in city list

    def __init__(self, dataurl):
        self.tree = ElementTree()

        try:
            urlhandle = urllib.urlopen(dataurl)
        except IOError:
            print "[Error] Unable to open the data url: " + dataurl
            sys.exit(1)

        self.tree.parse(urlhandle)

    def getQuantity(self,path):
        """Get the quatity contained at the XML XPath"""
        return self.tree.findtext(path)

    def getAttribute(self, path, attribute):
        """Get the atribute of the element at XPath path"""
        element = self.tree.find(path)
        if attribute in element:
            return element['attribute']
        return None
        
    def getAvailableQuantities(self):
        """Get a list of all the available quatities in the form of their
        XML XPaths
        """

        pathlist =[]
        self._getAllXPaths(pathlist,"",self.tree.getroot())
        return pathlist

    # This nasty little function recursively traverses
    # an element tree to get all the available XPaths
    # you have to pass in the pathlist you want to contain
    # the list
    def _getAllXPaths(self, pathlist, path, element):
        children = element.getchildren()
        if not children:
            sys.stdout.write(path + "/"+element.tag + "\n")
            pathlist.append(path + "/"+element.tag)
        else:
            for child in children:
                self._getAllXPaths(pathlist, path + "/" + element.tag, child)
        
