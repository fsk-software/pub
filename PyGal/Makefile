all: 

#--https://datacatalog.worldbank.org/dataset/world-development-indicators
WDI_csv.zip:
	${SH} wget http://databank.worldbank.org/data/download/WDI_csv.zip . | true

WDIData.csv: WDI_csv.zip
	${SH} unzip $<

#--https://github.com/fivethirtyeight/data/tree/master/college-majors
data.csv:
	${SH} wget https://raw.githubusercontent.com/fivethirtyeight/data/master/college-majors/recent-grads.csv -O $@

school.csv: WDIData.csv
	${SH} head -1 $< > $@
	${SH} grep "Progression to secondary school (%)" $< >> $@
	${SH} dos2unix $@
	${SH} dos2unix WDICountry.csv

setup:
	${SH} sudo apt-get install -y python-pip
	${SH} sudo pip install pygal
	${SH} sudo pip install pygal_maps_world

run: data.csv school.csv
	${SH} ./pygalEx.py


clean:
	${RM} *.pyc data.csv *.csv *.zip
