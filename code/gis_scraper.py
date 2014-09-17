import csv
import urllib
import os
from zipfile import ZipFile

with open("gis_links.csv","rb") as f:
	reader = csv.DictReader(f)
	for row in reader:
		print(row)
		try:
			head, tail = os.path.split(row['link'])
			urllib.urlretrieve(row['link'],tail)
			ZipFile(tail).extractall(tail.split(".")[0])
		except Exception, e:
			print(e)
			pass

"""
Errors:
{'link': 'http://www.nyc.gov/html/dcp/download/biggapps/DCP_nyhaav_001.zip\xa0\xa0', 'name': 'Health Areas'}
[Errno 71] Protocol error: 'DCP_nyhaav_001.zip\xa0\xa0'

{'link': 'http://www.nyc.gov/html/dcp/download/biggapps/DCP_population_projections_001.xls', 'name': 'DCP Population Projection 2000-2030'}
File is not a zip file

"""

