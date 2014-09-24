#!/usr/bin/env python
from __future__ import print_function
from bs4 import BeautifulSoup
from StringIO import StringIO
from time import gmtime, strftime
from zipfile import ZipFile
import csv
import os
import pprint
import re
import sys
import urllib2


class Printer(pprint.PrettyPrinter):
	def format(self, object, context, maxlevels, level):
		if isinstance(object, unicode):
			return ('"%s"' % object.encode('utf8').replace('\\', '\\\\').replace('"', '\\"'), True, False)
		return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

	def print_var(self, var, data):
		self.print("%s = " % var, end="")
		self.pprint(data)
		self.print("")

	def print(self, *args, **kwargs):
		print(*args, file=self._stream, **kwargs)


output = open(os.path.join(os.path.dirname(__file__), 'edost', 'codes.py'), 'w')
printer = Printer(stream=output, indent=4, width=1000)
printer.print(
	"# coding: utf-8\n"
	"# This file was automatically generated on %s\n"
	"from __future__ import unicode_literals\n" % strftime("%Y-%m-%d %H:%M:%S UTC", gmtime()),
)


def generate_tariff_codes():
	soup = BeautifulSoup(urllib2.urlopen("http://edost.ru/kln/help.html").read().decode('cp1251'))
	a = soup.find('a', attrs={'name': 'DeliveryCode'})
	codes = []
	for tr in a.find('table', attrs={'width': '100%'}).find_all('tr')[1:]:
		tds = tr.find_all('td')
		tariff_id = int(tds[0].p.text)
		tariff_name = tds[1].p.text
		codes.append((tariff_id, tariff_name))
	printer.print_var("EDOST_TARIFFS", codes)


def generate_city_codes():

	# Read city codes from zipped CSV file.
	# This is required because the HTML page listing doesn't associate region capitals with their regions.

	sio = StringIO()
	sio.write(urllib2.urlopen("http://www.edost.ru/kln/cities_edost.zip").read())
	sio.seek(0)
	zip = ZipFile(sio)
	cities = []
	for row in csv.reader(zip.open('cities_edost.csv'), delimiter=';'):
		row = [x.decode('cp1251') for x in row]
		city_id, city, region, full_city, xx = row
		city_id = int(city_id)
		cities.append((city_id, city, region, full_city))

	city_for_id = {city_id: (city, region, full_city) for city_id, city, region, full_city in cities}
	id_for_city = {city: city_id for city_id, city, region, full_city in cities}

	printer.print_var("EDOST_CITIES", cities)
	printer.print_var("EDOST_CITY_FOR_ID", city_for_id)
	printer.print_var("EDOST_ID_FOR_CITY", id_for_city)

	# Read country and region codes

	soup = BeautifulSoup(urllib2.urlopen("http://edost.ru/kln/code.html").read().decode('cp1251'))
	tables = soup.find_all('table', attrs={'width': 300})

	def parse_table(table, data_name, lookup_name, reverse_name):
		data = []
		lookup = {}
		reverse = {}
		for tr in table.find_all('tr')[1:]:
			tds = tr.find_all('td')
			name = tds[0].text
			code = int(tds[1].text)
			data.append((code, name))
			lookup[code] = name
			reverse[name] = code
		printer.print_var(data_name, data)
		printer.print_var(lookup_name, lookup)
		printer.print_var(reverse_name, reverse)

	parse_table(tables[0], "EDOST_COUNTRIES", "EDOST_COUNTRY_FOR_ID", "EDOST_ID_FOR_COUNTRY")
	parse_table(tables[1], "EDOST_REGIONS", "EDOST_REGION_FOR_ID", "EDOST_ID_FOR_REGION")


if __name__ == "__main__":
	generate_tariff_codes()
	generate_city_codes()
