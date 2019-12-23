JCMS data exporter
==================

This python script allows you to export data from JCMS using the OpenAPI

Usage :
* Go to the JCMS backend
* Export a list of the selected objects as a CSV (JCMS back end native function)
* Add you IP and activate openAPI in the admin preferences

Then :
``` 
python exportjcms.py --field mails --field author --url http://sunweb1:15961 --input objects.csv --output export.csv
```

This python script :
* gets the object ID in the objects.csv file generated by JCMS
* calls the open API for each object and then extracts values of the desired field (here mails and author)
* Then it writes the result into export.csv file.
