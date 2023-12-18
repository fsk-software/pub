#!/usr/bin/python3
import argparse
import logging
import re
from CppGenerator import CppGenerator
from collections import namedtuple

class Odb:
  def __init__(self):
    self.recName=None
    self.objMap={}

  def parseOdbFile(self,fileName):
    RegExMatcher={
                   'Kvp'         : r' *(\S+) *(\S+).*',
                   'RecordStart' : r'.*dbclass *(\S+).*',
                   'RecordEnd'   : r' *end;.*',
                 }
    with open(fileName, 'r') as fp:
      C=fp.read()
  
      for line in C.split('\n'):
        for k,v in RegExMatcher.items():
          m=re.match(v,line)
          if m:
            fx='self.handle%s(m)'%(k)
            eval(fx)
    return self.objMap

  def handleRecordStart(self,G):
    if not re.match(r'#.*',G[0]):
      self.recName=G[1]
      logging.debug('processing record %s'%(self.recName))
      self.objMap[self.recName]=list()

  def handleKvp(self,G):
    Element=namedtuple('Element',['type','name','isKey'])
    if self.recName and (not re.match(' *end;.*',G[0])):
      isPrimaryKey=(re.match(r'.*as key;',G[0]) != None)
      dType=G[1]
      field=G[2].strip(';').strip()
      logging.debug("%s has %s of %s"%(self.recName,field,dType))
      self.objMap[self.recName].append(Element(dType,field,isPrimaryKey))

  def handleRecordEnd(self,G):
    self.recName=None
  
def processFile(fileName):
  logging.debug("processing fileName '%s'"%(fileName))
  objList=Odb().parseOdbFile(fileName)
  for k,v in objList.items():
    print(v)
  moduleName=args.input.replace(".odb","")
  fx='%sGenerator(moduleName,objList)'%(args.lang)
  logging.debug("executing %s"%(fx))
  eval(fx)

#--main--
if __name__ == "__main__":
  parser=argparse.ArgumentParser(description='ODB precompiler')
  parser.add_argument('--verbose',action='store_true', default=False)
  parser.add_argument('--input',action='store',required=True)
  parser.add_argument('--lang',action='store',required=True)
  args,unk = parser.parse_known_args()
  
  if args.verbose:
    logLevel=logging.DEBUG
  else:
    logLevel=logging.INFO

  logging.basicConfig(format='%(asctime)s [%(filename)s:%(lineno)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p',level=logLevel)
  processFile(args.input)
