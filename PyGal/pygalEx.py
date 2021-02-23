#!/usr/bin/python

import pygal
import csv
import pygal.maps.world
import time

def readCsvAsDict(fileName, keyField, separator=',', quote='"'):
    """
    Inputs:
      fileName  - Name of CSV file
      keyField  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      column values for that row.
    """
    retval = dict()
    with open(fileName, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in reader:
            retval[row[keyField]] = row
    return retval


def example01():
  chart = pygal.Line()
  chart.title = 'Browser usage evolution (in %)'
  chart.x_labels = map(str, range(2002, 2013))
  chart.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
  chart.render_in_browser()

def example02a():
  data=readCsvAsDict('data.csv','Major_code')

  Fields=['Women','Men','Total']
  plotData=dict()
  for key in Fields:
    D=[(k,v[key]) for (k,v) in sorted(data.items())]
    L=([int(el[1]) if el[1].isdigit() else None for el in D])
    xLabel=([el[0] for el in D])
    plotData[key]=L
  
  chart=pygal.Line()
  chart.title='Major Code By Gender (Line)'
  for key in Fields:
    chart.add(key,plotData[key])
  chart.x_labels = xLabel
  chart.render_in_browser()

def example02b():
  # Why? : https://blog.datawrapper.de/stacked-column-charts/
  data=readCsvAsDict('data.csv','Major_code')

  Fields=['Women','Men']
  plotData=dict()
  for key in Fields:
    D=[(k,v[key]) for (k,v) in sorted(data.items())[100:120]]
    L=([int(el[1]) if el[1].isdigit() else None for el in D])
    xLabel=([el[0] for el in D])
    plotData[key]=L
  
  chart=pygal.StackedLine(fill=True)
  chart.title='Major Code By Gender (Stacked Line)'
  for key in Fields:
    chart.add(key,plotData[key])
  chart.x_labels = xLabel
  chart.render_in_browser()

def example03a():
  data=readCsvAsDict('data.csv','Major_code')

  Fields=['Women','Men','Total']
  plotData=dict()
  for key in Fields:
    D=[(k,v[key]) for (k,v) in sorted(data.items())[100:120]]
    L=([int(el[1]) if el[1].isdigit() else None for el in D])
    xLabel=([el[0] for el in D])
    plotData[key]=L
  
  chart=pygal.Bar()
  chart.title='Major Code By Gender (Bar)'
  for key in Fields:
    chart.add(key,plotData[key])
  chart.x_labels = xLabel
  chart.render_in_browser()

def example03b():
  data=readCsvAsDict('data.csv','Major_code')

  Fields=['Women','Men','Total']
  plotData=dict()
  for key in Fields:
    D=[(k,v[key]) for (k,v) in sorted(data.items())[100:120]]
    L=([int(el[1]) if el[1].isdigit() else None for el in D])
    xLabel=([el[0] for el in D])
    plotData[key]=L
  
  chart=pygal.HorizontalBar()
  chart.title='Major Code By Gender (Horizontal Bar)'
  for key in Fields:
    chart.add(key,plotData[key])
  chart.x_labels = xLabel
  chart.render_in_browser()


def example03c():
  # Why? : https://blog.datawrapper.de/stacked-column-charts/
  data=readCsvAsDict('data.csv','Major_code')

  Fields=['Women','Men']
  plotData=dict()
  for key in Fields:
    D=[(k,v[key]) for (k,v) in sorted(data.items())[100:120]]
    L=([int(el[1]) if el[1].isdigit() else None for el in D])
    xLabel=([el[0] for el in D])
    plotData[key]=L
  
  chart=pygal.StackedBar()
  chart.title='Major Code By Gender (Stacked Bar)'
  for key in Fields:
    chart.add(key,plotData[key])
  chart.x_labels = xLabel
  chart.render_in_browser()

def example04():
  data=readCsvAsDict('data.csv','Major_code')

  plotData=dict()
  for (key,val) in data.items():
    try:
      plotData[val['Major_category']].append(int(val['Median']))
    except:
      plotData[val['Major_category']]=list()
      plotData[val['Major_category']].append(int(val['Median']))

  categories=[val['Major_category'] for (k,val) in data.items()]
  chart = pygal.Histogram()
  chart.title='Salary Range By Major Category'
  for k in set(categories):
    x0=min(plotData[k])
    x1=max(plotData[k])
    y=sum(plotData[k])/float(len(plotData[k]))
    chart.add(k,[(y,x0,x1)])
  chart.render_in_browser()

def example05():
  data=readCsvAsDict('data.csv','Rank')
  chart = pygal.XY()
  chart.title='Salary vs Unemployment Rate'
  for (k,v) in sorted(data.items()):
    chart.add(v['Major'],[(float(v['Unemployment_rate']),int(v['Median']))])
  chart.render_in_browser()

def example06a():
  data=readCsvAsDict('data.csv','Major_code')
  chart = pygal.Pie()
  chart.title='Major by Totals'
  for (k,v) in sorted(data.items()):
    val = int(v['Total']) if v['Total'].isdigit() else None
    chart.add(v['Major'],val)
  chart.render_in_browser()
  
def example06b():
  data=readCsvAsDict('data.csv','Major_code')
  chart = pygal.Pie()
  chart.title='Top Majors by Total Student Count'
  L=[(int(v['Total']),v['Major']) for (k,v) in data.items() if v['Total'].isdigit()]
  L=L[0:10]
  N=sum([v for (v,k) in L])
  for (t,k) in sorted(L,reverse=True):
    chart.add(k,t)
  chart.render_in_browser()

def example06c():
  data=readCsvAsDict('data.csv','Major_code')
  chart = pygal.Pie()
  chart.title='Top Majors by Total Student Count (w/Labels)'
  L=[(int(v['Total']),v['Major']) for (k,v) in data.items() if v['Total'].isdigit()]
  L=L[0:10]
  N=sum([v for (v,k) in L])
  for (t,k) in sorted(L,reverse=True):
    chart.add(k,[{'value': t, 'label': "%0.2f%%"%(float(100*t)/N)}])
  chart.render_in_browser()
  
def example06d():
  data=readCsvAsDict('data.csv','Major_code')
  chart = pygal.Pie()
  chart.title='Top Majors by Total Student Count (Multi-series Pie)'
  L=[(int(v['Total']),v['Major'],int(v['Men']),int(v['Women'])) for (k,v) in data.items() if v['Total'].isdigit()]
  L=L[0:10]
  N=sum([v for (v,t,m,w) in L])
  for (t,k,m,w) in sorted(L,reverse=True):
#   chart.add(k,[m,w])
    chart.add(k,[{'value':m,'label':'men: %02f%%'%(float(100*m)/t)},{'value':w,'label':'women:%02f%%'%(float(100*w)/t)}])
  chart.render_in_browser()
  
def example07():
  data=readCsvAsDict('data.csv','Major_code')
  chart = pygal.Radar()
  chart.title = 'Radar Plot'

  chart.x_labels=['Men','Women','Employment Rate']
  for val in [v for (k,v) in data.items() if v['Total'].isdigit()][0:5]:
    L=[]
    L.append(float(val['Men'])/float(val['Total']));
    L.append(float(val['Women'])/float(val['Total']));
    L.append(1.0-float(val['Unemployment_rate']));
    chart.add(val['Major'],L)
  chart.render_in_browser()

def example08():
  data=readCsvAsDict('data.csv','Major_code')
  plotData=dict()
  for val in [v for (k,v) in data.items() if v['Median'].isdigit()]:
    category=val['Major_category']
    try:
      plotData[category].append(int(val['Median']))
    except(KeyError):
      plotData[category]=list()
      plotData[category].append(int(val['Median']))

  chart = pygal.Box()
  chart.title = 'Salary Range by Major Category'
  for (k,v) in plotData.items():
    chart.add(k,v)
  chart.render_in_browser()

def example09():
  data=readCsvAsDict('data.csv','Major_code')
  plotData=dict()
  for val in [v for (k,v) in data.items() if v['Total'].isdigit()][0:10]:
    category=val['Major']
    try:
      plotData[category].append(int(val['Men']))
      plotData[category].append(int(val['Women']))
    except(KeyError):
      plotData[category]=list()
      plotData[category].append(int(val['Men']))
      plotData[category].append(int(val['Women']))

  chart = pygal.Dot(x_label_rotation=30)
  chart.title = 'Major by Gender'
  chart.x_labels = ['Men', 'Women']
  for (k,v) in plotData.items():
    chart.add(k, v)
  chart.render_in_browser()

def convertCountryCodeToPygal(countryCode):
  convertCountryCodeToPygal.data=readCsvAsDict('WDICountry.csv','Country Code')
  return convertCountryCodeToPygal.data[countryCode]['2-alpha code'].lower()
  
def example10():
  data=readCsvAsDict('school.csv','Country Code')

  chart = pygal.maps.world.World()
  chart.title = 'Secondary School Rate / Country'
  year=2016
  plotData=dict()
  for (k,v) in data.items()[0:-1]:
    try:
      plotData[convertCountryCodeToPygal(k)]=float(v[str(year)])
    except:
      pass
  chart.add(str(year),plotData)
  chart.render_in_browser()

def runAll():
  for fx in [ 'example01' ,'example02a' ,'example02b' ,'example03a' ,'example03b' ,'example03c' \
             ,'example04' ,'example05' ,'example06a' ,'example06b' ,'example06c' ,'example06d' \
             ,'example07' ,'example08' ,'example09' ,'example10']:
    eval("%s()"%(fx))
    time.sleep(2)

#---main---
runAll()
