#!/usr/bin/python

# Copyright (C) 2011 Ian Gable
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

## Auth.: Ian Gable

import urllib
import sys


# If we don't have at least python 2.7 we want to require
# elementtree which has full XPath support. The 2.7 version
# of this includes this already.

if float(sys.version[:3]) >= 2.7:
    from xml.etree.ElementTree import ElementTree
else:
    from elementtree.ElementTree import ElementTree

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
            raise  IOError("Unable to open the data url: " + self.city_list_url)

        cityListTree.parse(urlhandle)
        siteList = cityListTree.findall("site")

        for site in siteList:
            cityNameEnglish = site.findtext("nameEn").encode('utf-8')
            
            self.cities[cityNameEnglish] = {\
                    'sitecode': site.attrib['code'].encode('utf-8'),\
                    'provincecode': site.findtext("provinceCode").encode('utf-8'),\
                    'nameFr': site.findtext("nameFr").encode('utf-8') }

            
    def is_city(self, name):
        """
        Returns True if name is a valid city
        """
        return name in self.cities

    def data_url(self,name):
        """
        Returns resource URL for the city denoted by name
        """
        if self.is_city(name):
            return self.base_url + self.province(name) + "/" + self.site_code(name) + "_e.xml"
        return None

    def province(self,name):
        """
        Returns Province code (e.g. 'ON', 'BC', etc) of the city denoted by name
        """
        if self.is_city(name):
            return self.cities[name]['provincecode']
        return None

    def site_code(self,name):
        """
        Returns the environment canada site for a city. For example Athabasca, AB
        has the site code s0000001
        """
        if self.is_city(name):
            return self.cities[name]['sitecode']
        return None
    
    def french_name(self,name):
        if self.is_city(name):
            return self.cities[name]['nameFr']
        return None

    def english_city_list(self):
        return self.cities.keys()

    def french_city_list(self):
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
        self.forecast_object_list = self._make_forecast_list()

    def get_quantity(self,path):
        """Get the quatity contained at the XML XPath"""
        return self.tree.findtext(path)

    def get_atrribute(self, path, attribute):
        """Get the atribute of the element at XPath path"""
        element = self.tree.find(path)
        if attribute in element:
            return element['attribute']
        return None
        
    def get_available_quantities(self):
        """Get a list of all the available quatities in the form of their
        XML XPaths
        """

        pathlist =[]
        # we are getting the full XPath with the attribute strings
        # this output is pretty long so maybe it would be wise
        # to also have an option to get the XPath without the attributes
        # self._get_all_xpaths(pathlist,"",self.tree.getroot())

        self._get_all_xpaths_with_attributes(pathlist,"",self.tree.getroot())
        return pathlist

    # This nasty little function recursively traverses
    # an element tree to get all the available XPaths
    # you have to pass in the pathlist you want to contain
    # the list
    def _get_all_xpaths(self, pathlist, path, element):
        children = element.getchildren()
        if not children:
            pathlist.append(path + "/"+element.tag)
        else:
            for child in children:
                self._get_all_xpaths(pathlist, path + "/" + element.tag, child)

    def _make_attribute_list(self, attrib):
        xpathattrib = ""
        for attribute, value in attrib.iteritems():
            xpathattrib = xpathattrib + "[@" + attribute + "='" + value + "']"
        return xpathattrib


    # This nasty little function recursively traverses
    # an element tree to get all the available XPaths
    # you have to pass in the pathlist you want to contain
    # the list
    def _get_all_xpaths_with_attributes(self, pathlist, path, element):
        children = element.getchildren()
        if not children:
            xpathattrib = self._make_attribute_list(element.attrib)

            if path == "":
                pathlist.append(element.tag + xpathattrib)
            else:
                pathlist.append(path + "/" + element.tag + xpathattrib)

        else:
            xpathattrib = self._make_attribute_list(element.attrib)

            for child in children:
                # skip the root tag
                if element.tag == "siteData":
                    self._get_all_xpaths_with_attributes(pathlist, path, child)
                else:
                    # we avoid the opening / since we start below the root 
                    if path == "":
                        self._get_all_xpaths_with_attributes(pathlist, element.tag + xpathattrib, child)
                    else:
                        self._get_all_xpaths_with_attributes(pathlist, path + "/" + element.tag + xpathattrib, child)

    def dump_forecast(self):
        for forecast in self.forecast_object_list:
            period = forecast.get_period().ljust(15)
            high = "    "
            low = "    "
            if forecast.has_low():
                low = forecast.get_low().ljust(4)
            if forecast.has_high():
                high = forecast.get_high().ljust(4)
            print "%s Low:%s High:%s" % (period,low,high)


    def _make_forecast_list(self):
        forecasts_tree_list = self.tree.findall('forecastGroup/forecast')
        forecast_object_list = []
        for forecast_tree in forecasts_tree_list:
            forecast_object_list.append(Forecast(forecast_tree))
        return forecast_object_list

class Forecast():

    def __init__(self,forcast):
        self.tree = forcast

    def get_period(self):
        return self.tree.findtext('period')

    def get_text_summary(self):
        return self.tree.findtext('textSummary')

    def has_low(self):
        low = False
        for temperature in self.tree.findall('temperatures/temperature'):
            if temperature.get('class') == 'low':
                low = True
        return low

    def has_high(self):
        high = False
        for temperature in self.tree.findall('temperatures/temperature'):
            if temperature.get('class') == 'high':
                high = True
        return high

    def get_high(self):
        if self.has_high():
            for temperature in self.tree.findall('temperatures/temperature'):
                if temperature.get('class') == 'high':
                    return temperature.text

    def get_low(self):
        if self.has_low():
            for temperature in self.tree.findall('temperatures/temperature'):
                if temperature.get('class') == 'low':
                    return temperature.text





