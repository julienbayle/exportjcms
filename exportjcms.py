import optparse
import csv
import requests
import lxml.etree

def getIDs(inputfile):
	with open(inputfile, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
		next(csvreader, None)  # skip the headers
		IDs = [row[0] for row in csvreader if len(row) > 0]
	return IDs

def convert(item, categories):
	data = item.text

	if 'class' in item.attrib and item.attrib['class'] == "com.jalios.jcms.Category" :
		if len(categories) == 0 or item.attrib['id'] in categories:
			data = item.text[item.text.rfind('/')-len(item.text)+1:]
		else:
			data = ""
	
	return data.encode("latin-1", errors='ignore').strip()

def getData(url, identifier) :
	response = requests.get(url + "/rest/data/" + identifier)

	if response.status_code != 200:
		raise Exception("Unable to get DATA for object {0} : {1}".format(identifier, response.status_code))

	return lxml.etree.fromstring(response.text.encode("UTF-8"))

def getValues(url, identifier, fields, categories):
	values = {}
	r = getData(url, identifier) 

	for field in fields:
		d = r.xpath('//field[@name="' + field + '"]')
		if len(d) == 1:
			value = [convert(it, categories) for it in d[0].findall('item') ]
			if len(value) == 0:
				value.append(convert(d[0], categories))
			values[field] = ", ".join(filter(None, value))

	return values

def export(options):
	identifiers = getIDs(options.inputfile)
	success_count = 0
	error_count = 0
	with open(options.outputfile, 'wb') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=options.fields, delimiter=';', quotechar='"')
		writer.writeheader()

		for identifier in identifiers :
			try :
				writer.writerow(getValues(options.url, identifier, options.fields, options.categories))
				success_count += 1
			except Exception as e:
				print e
				error_count += 1

	print "Exported to {0} with {1} success and {2} error(s)".format(options.outputfile, success_count, error_count) 


if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option('--field', action="append", dest='fields', default=[], help="Field name")
	parser.add_option('--categoryfilter', action="append", dest='categories', default=[], help="Limit categories to this list")
	parser.add_option('--input', action="store", dest='inputfile', default="results.csv", help="CSV source (First column must contain JCMS ID)")
	parser.add_option('--output', action="store", dest='outputfile', default="export.csv", help="CSV output filename ")
	parser.add_option('--url', action="store", dest='url', default="http://sunweb1:15961", help="JCMS base URL (exemple : localhost:8080)")

	options, _ = parser.parse_args()
   	export(options)
