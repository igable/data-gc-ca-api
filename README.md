# data-gc-ca-api 0.2.2 README

## Introduction
data-gc-ca-api: a simple python api for the Canada Open Data Portal

The Government of Canada recently released a number of open data sets at the website
[www.data.gc.ca](http://www.data.gc.ca/).  This simple python package has tools
for accessing the [City Weather](http://goo.gl/Xkcqp) open data set. It could
be expanded to include more.

The data_gc_ca_api directory contains the file cityweather.py which has two classes City
and CityIndex. There two classes can be used to access all available quatities
published in the Environment Canada city XML files. Environment Canada provides
a [description](http://goo.gl/XD7w4) of what can be accessed but it's far easier
to look at an example [city XML](http://goo.gl/vyL7r).

## Installation

This package is available from the [Python Package Index](http://pypi.python.org). It
can be easily installed using pip as follows
 
    $ pip install data-gc-ca-api

Tarballs of are available from the [project website](https://github.com/igable/data-gc-ca-api).
To install from a tarball:

    $ tar xzvf data-gc-ca-api-X.Y.Z.tar.gz
    $ cd data-gc-ca-api-X.Y.Z
    $ python setup.py install

## Command line tool: weatherca

This package also includes a command line tool 'weatherca' for quickly getting
information. It also serves as an example of how to use the data-gc-ca-api
python module. 

Here are some quick examples of how to use the weatherca:

    $ weatherca --help

List the available cities:

    $ weatherca --list

Show the current temperature in Victoria:

    $ weatherca --city "Victoria" --quantity currentConditions/temperature

Get the wind speed in Ottawa:

    $ weatherca --city "Ottawa (Richmond - Metcalfe)" --quantity currentConditions/wind/speed

## Contributors

* Ian Gable
* Johan Harjono

## Data License

The terms for accessing the data available from the Canada Open Data Portal can
be found by visiting the [www.data.gc.ca](http://www.data.gc.ca/)

## Software License

This program is free software; you can redistribute it and/or modify
it under the terms of either:

a) the GNU General Public License as published by the Free
Software Foundation; either version 3, or (at your option) any
later version, or

b) the Apache v2 License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See either
the GNU General Public License or the Apache v2 License for more details.

You should have received a copy of the Apache v2 License with this
software, in the file named "LICENSE".

You should also have received a copy of the GNU General Public License
along with this program in the file named "COPYING". If not, write to the
Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, 
Boston, MA 02110-1301, USA or visit their web page on the internet at
http://www.gnu.org/copyleft/gpl.html.

