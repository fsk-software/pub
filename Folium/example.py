#!/usr/bin/python3

import folium
import sys
import numpy
import csv
import webbrowser
import os
import pandas as pd

def log(msg):
  print("(LOG) %s"%(msg))

def openInBrowser(htmlFileName):
  webbrowser.open(htmlFileName, new=2)

def convertToPng(htmlFileName, pngFileName, pageLoadDelayMs=5000):
  os.system("cutycapt --delay=%d --url=file://%s --out=%s 2>/dev/null"%(pageLoadDelayMs, os.path.realpath(htmlFileName),pngFileName))

def test00():
  tempFile='./index.html'
  latLong=(43.669428, -92.974317)
  map = folium.Map(location=latLong)
  map.save(tempFile)
  openInBrowser(tempFile)

def test01():
  tempFile='./index.html'
  latLong=(43.669428, -92.974317)
  for tileType in ['OpenStreetMap', 'Stamen Terrain', 'Stamen Toner']:
    print(tileType)
    map = folium.Map(location=latLong, zoom_start=13, tiles=tileType)
    map.save(tempFile)
    convertToPng(tempFile, '%s.png'%(tileType.replace(' ','')), pageLoadDelayMs=5000)

def processFile(fileName):
  fileName=sys.argv[1]
  tempFile='./index.html'
  latLong=(39.809830, -98.559149)
  map = folium.Map(location=latLong, zoom_start=4)
  with open(fileName, 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
      log(row)
      folium.CircleMarker(
          location=[float(row['Latitude']),float(row['Longitude'])],
          radius=2,
          popup="",
          color="#3186cc",
          fill=True,
          fill_color="#3186cc",
      ).add_to(map)
  map.save(tempFile)
  openInBrowser(tempFile)

def test02():
  state_unemp = pd.read_csv("state_unemployment.csv")
  url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
  state_geo = f'{url}/us-states.json'        #for state level data
  map = folium.Map(location=[48, -102], zoom_start=4)
  folium.Choropleth(
      geo_data = state_geo,                  #json
      name ='choropleth',                  
      data = state_unemp,                     
      columns = ['State', 'Unemployment'], #columns to work on
      key_on ='feature.id',
      fill_color ='YlGnBu',     #I passed colors Yellow,Green,Blue
      fill_opacity = 0.7,
      line_opacity = 0.2,
     legend_name = "Unemployment scale"
  ).add_to(map)
  tempFile='./index.html'
  map.save(tempFile)
  openInBrowser(tempFile)
  convertToPng(tempFile, './foo.png')

#---main---
#test00()
#test01()
#test02()
fileName=sys.argv[1]
processFile(fileName)
