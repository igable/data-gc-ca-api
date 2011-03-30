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
        Returns True iff name is a valid city
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
        return self.tree.findtext(path)

    def getAttribute(self, name, attribute):
        element = self.tree.find(name)
        if attribute in element:
            return element['attribute']
        return None
        


