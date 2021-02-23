all: 

#2020-01.csv:
#	${SH} wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2020-01.csv -O $@

state_unemployment.csv:
	${SH} wget https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/US_Unemployment_Oct2012.csv -O $@

#sample.csv: 2020-01.csv
#	${SH} head -100000 $< > $@

windpower.csv:
	${SH} wget https://openei.org/datasets/dataset/5fb0a6e2-a02b-4776-a5de-08a47828943f/resource/df55e4c8-258a-4845-a145-df00bd7d79aa/download/millerkeith2018data2.csv -O $@

#world-countries.json:
#	${SH} wget https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json

#data.csv:
#	${SH} echo 'Num,Country_0,Count_0' > $@
#	${SH} echo '0,  United States of America   ,18425' >> $@
#	${SH} echo '1,  United Kingdom             ,3070' >> $@
#	${SH} echo '2,  France                     ,2705' >> $@
#	${SH} echo '3,  Canada                     ,1498' >> $@
#	${SH} echo '4,  Japan                      ,1493' >> $@
#	${SH} echo '5,  Italy                      ,1471' >> $@
#	${SH} echo '6,  Germany                    ,1418' >> $@
#	${SH} echo '7,  Russia                     ,800' >> $@
#	${SH} echo '8,  India                      ,783' >> $@
#	${SH} echo '9,  Spain                      ,601' >> $@
#	${SH} echo '10, Australia                  ,506' >> $@
#	${SH} echo '11, Hong Kong                  ,468' >> $@
#	${SH} echo '12, South Korea                ,457' >> $@
#	${SH} echo '13, Sweden                     ,396' >> $@
#	${SH} echo '14, Finland                    ,324' >> $@
#	${SH} echo '15, China                      ,300' >> $@
#	${SH} echo '16, Belgium                    ,299' >> $@
#	${SH} echo '17, Denmark                    ,297' >> $@
#	${SH} echo '18, Brazil                     ,262' >> $@
#	${SH} echo '19, Poland                     ,245' >> $@
#	${SH} echo '20, Mexico                     ,236' >> $@
#	${SH} echo '21, Netherlands                ,226' >> $@
#	${SH} echo '22, Argentina                  ,211' >> $@
#	${SH} echo '23, Czech Republic             ,163' >> $@
#	${SH} echo '24, Austria                    ,151' >> $@
#	${SH} echo '25, Ireland                    ,135' >> $@
#	${SH} echo '26, Turkey                     ,134' >> $@
#	${SH} echo '27, Greece                     ,131' >> $@
#	${SH} echo '28, Norway                     ,124' >> $@
#	${SH} echo '29, Hungary                    ,119' >> $@
#	${SH} echo '30, Switzerland                ,99' >> $@

#data.zip:
#	${SH} wget https://simplemaps.com/static/data/world-cities/basic/simplemaps_worldcities_basicv1.73.zip -o $@

run: windpower.csv
	${SH} ./example.py $<

clean:
	${RM} *.csv *.html *.png *.json

