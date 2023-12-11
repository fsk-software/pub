import logging
import re

#--provides mapping of 'general db types' to language-specific (e.g C++)
#-- data types
def typeConverter(dbType):
  m=re.match(r'.*\((.*)\).*',dbType)
  size=m.group(1) if m else None
  TypeMapper={
               'float'    :  'float',
               'bigint'   :  'long',
               'text'     :  'std::string',
               'char'     :  'char',
               'int'      :  'int',
               'long'      : 'long',
               'double'   :  'double',
               'date'     :  'std::string',
               'datetime' :  'std::string',
             }
  VarLenMapper={
               'char(%s)'%(size)  : 'VarChar%s'%(size),
               }
  return VarLenMapper[dbType] if m else TypeMapper[dbType]

def userDefinedTypeName(el):
  m=re.match(r'.*\((.*)\).*',el.type)
  dataSize=int(m.group(1))
  return 'VarChar%d'%(dataSize);

class CppGenerator:
  def __init__(self, moduleName, objList):
    logging.debug("moduleName %s; objList %s"%(moduleName,str(objList)))
    self.moduleName=moduleName
    self.objList=objList
    self.createHeader()
    self.createBody()

  @staticmethod
  def camelCase(el):
      retVal=[el[0].upper()+el[1:]]
      return "".join(retVal)

  def createHeader(self):
    with open(self.moduleName+".h",'w+') as fp:
      macroName=("%s_h"%(self.moduleName)).upper()
      fp.write("#ifndef %s\n"%(macroName));
      fp.write("#define %s\n"%(macroName));
      fp.write("#include <string>\n")
      fp.write("#include <cstring>\n")
      fp.write('#include <iostream>\n')
      fp.write('#include <sstream>\n')
      fp.write('#include "DbConnector.h"\n')
      for className,elList in self.objList.items():
        L=self.classDef(className,elList)
        fp.write("\n".join(L)+"\n")
      fp.write("#endif\n");

  def createBody(self):
    with open(self.moduleName+".cpp",'w+') as fp:
      fp.write('#include "%s.h"\n'%(self.moduleName))
      fp.write('#include <sstream>\n')
      fp.write('#include "DbConnector.h"\n')
      for k,v in self.objList.items():
        fp.write('\n'.join(self.ctorBody(k,v)))
        fp.write('\n\n')
        fp.write('\n'.join(self.settersBody(k,v)))
        fp.write('\n'.join(self.gettersBody(k,v)))
      fp.write("\n")

      for className,objList in self.objList.items():
        L=self.populateFromSqlBody(className, objList)
        fp.write('\n'.join(L))
        fp.write('\n')

  #--================================================================================
  #-- Header Components
  #--================================================================================
  def classDef(self,className,objList):
    retVal=list()
    retVal.append("")
    retVal.append("class %s"%(className))
    retVal.append("{");
    retVal.append("  public:");
    for el in self.genVarLenTypes(className,objList):
      retVal.append("    %s"%(el))
    for el in self.ctorDef(className,objList):
      retVal.append("    %s"%(el))
    for el in self.settersDef(className,objList):
      retVal.append("    %s"%(el))
    for el in self.gettersDef(className,objList):
      retVal.append("    %s"%(el))

    for el in self.populateFromSqlDef(className,objList):
      retVal.append("    %s"%(el))

    retVal.append("  private:");
    for el in self.attribDef(objList):
      retVal.append("    %s"%(el))
    retVal.append("};");
    return retVal

  def genVarCharType(self, className, obj, size):
    retVal=[]
    retVal.append('typedef struct type%d'%(size))
    retVal.append('{')
    retVal.append('  char val_[%d];'%(size))
    retVal.append('  const char& operator[](int i) const { return val_[i];}')
    retVal.append('  char& operator[](int i){return val_[i];}')

    retVal.append("  type%d(){memset(val_, '\\0', sizeof(val_));}"%(size))
    retVal.append('  type%d(std::string val)'%(size))
    retVal.append('  {')
    retVal.append('    // initialize buffer to EOF string end indicator')
    retVal.append('    //  then, initialize with specified value while')
    retVal.append('    //  not overflowing the buffer');
    retVal.append('    // throw std::out_of_range exception if the specified')
    retVal.append('    // exceeds the capacity of the buffer length')
    retVal.append("    memset(val_, '\\0', sizeof(val_));")
    retVal.append('    const int len1=sizeof(val_)-1;')
    retVal.append('    const int len2=val.length();')
    retVal.append('    if (len2 > len1)')
    retVal.append('    {')
    retVal.append("      std::ostringstream errSs;")
    retVal.append('      errSs << "exceeded buffer length " << len2 << " > " << len1;')
    retVal.append('      throw std::out_of_range(errSs.str());')
    retVal.append('    }')
    retVal.append('    memcpy(val_,val.c_str(),std::min(len1,len2));')
    retVal.append('   }')

    retVal.append('} %s;'%(userDefinedTypeName(obj)))
    retVal.append('friend std::ostream& operator<<(std::ostream &ss, const %s& val) {'%(userDefinedTypeName(obj)))
    retVal.append('  //return up up to the first instance of EOL, buffer is initialized to EOLs')
    retVal.append('  int i=0;')
    retVal.append("  while (i < sizeof(val) && val[i]!='\\0') ss << val[i++];")
    retVal.append('  return (ss);')
    retVal.append('}')
    return retVal

  def genVarLenTypes(self, className, objList):
    retVal=[]
    for obj in [el for el in objList if re.match(r'.*\(.*\).*',el.type)]:
      m=re.match(r'.*\((\d+)\).*',obj.type)
      if m:
        size=m.group(1)
        for e in self.genVarCharType(className, obj, int(size)):
          retVal.append(e)

    return retVal

  def ctorDef(self,className,objList):
    retVal=list()
    argList=["const %s& %s"%(typeConverter(el.type),el.name) for el in [e for e in objList if e[2]]]
    retVal.append("%s(%s);"%(className,','.join(argList)))
    return retVal

# def setterSigniture(el):
#   retVal=[]
#   retVal.append('void set%s(%s %s)'%(self.camelCase(el.name),'el.type','el.name'))
#   return retVal

  def settersDef(self,className,objList):
    retVal=[]
    for el in [el for el in objList if not el.isKey]:
      retVal.append("void set%s(const %s& val);"%(self.camelCase(el.name),typeConverter(el.type)))
    return retVal

  def gettersDef(self,className,objList):
    retVal=[]
    for el in [el for el in objList]:
      retVal.append("%s get%s() const;"%(typeConverter(el.type),el.name[0].upper()+el.name[1:]));
    return retVal

  def populateFromSqlDef(self, className, objList):
    retVal=[]
    retVal.append('//@todo; move to private?')
    retVal.append('void populateFromSql(const DbConnector::KvpType& kvp);')
    return retVal

  def attribDef(self,objList):
    return ['%s%s %s;'%('const ' if e.isKey else '',typeConverter(e.type),e.name) for e in objList]


  #--================================================================================
  #-- Body Components
  #--================================================================================
  def ctorBody(self,className,objList):
    retVal=list()
    argList=["const %s& %s"%(typeConverter(el.type),el.name) for el in [e for e in objList if e.isKey]]
    initList=["%s(%s)"%(e.name,e.name if e.isKey else '') for e in objList]
    fList=["%s %s%s"%(e.name,e.type,' NOT NULL' if e.isKey else '') for e in objList]
    pList=[e.name for e in objList if e.isKey]
    createTableSql="CREATE TABLE %s (%s%s);"%(className,','.join(fList),',PRIMARY KEY(%s)'%(','.join(pList)) if len(pList) else '')
    insertSql='INSERT INTO %s (%s) VALUES (%s);'%(className,','.join([e.name for e in objList]),'" + ss.str().substr(0,ss.str().length()-1) + "')
    ssList=['ss << "\'" << this->%s << "\',";'%(e.name) for e in objList]
    
    retVal.append("%s::%s(%s)%s"%(className,className,','.join(argList),':'+','.join(initList)))
    retVal.append("{")
    retVal.append("  std::ostringstream ss;")
    for e in ssList:
      retVal.append("  %s"%(e))
    retVal.append('  if (DbConnector::instance()->tableExists("%s"))'%(className));
    retVal.append('  {')
    retVal.append('    try {')
    retVal.append("      // strip off trailing ',' from insert command")
    retVal.append('      DbConnector::instance()->execute("%s");'%(insertSql))
    retVal.append('    } catch(sql::SQLException e)')
    retVal.append('    {')
    retVal.append('      std::string error=e.what();')
    retVal.append('      const bool isDup=(error.find("Duplicate entry")!=std::string::npos) && (error.find("PRIMARY")!=std::string::npos);')
    retVal.append('      if(isDup)')
    retVal.append('      {')
    retVal.append('        std::ostringstream ss;')
    retVal.append('        ss << "SELECT * FROM %s WHERE %s=\'" << this->val01 << "\' LIMIT 1;";'%(className,argList[0]))
    retVal.append('        DbConnector::KvpList results=DbConnector::instance()->executeQuery("SELECT * from %s WHERE val01=\'1\' LIMIT 1");'%(className))
    retVal.append('        populateFromSql(results.at(0));')
    retVal.append('      }')
    retVal.append('      else')
    retVal.append('      {')
    retVal.append('      std::cout << "error: " << error << std::endl;')
    retVal.append('        throw(e);')
    retVal.append('      }')
    retVal.append('    }')
    retVal.append('  }')
    retVal.append('  else')
    retVal.append('  {')
    retVal.append('    DbConnector::instance()->execute("%s");'%(createTableSql))
    retVal.append('    DbConnector::instance()->execute("%s");'%(insertSql))
    retVal.append('  }')
    retVal.append("}")
    return retVal

  def settersBody(self,className,objList):
    retVal=[]
    for el in [el for el in objList if not el.isKey]:
      retVal.append("void %s::set%s(const %s& val)"%(className,self.camelCase(el.name),typeConverter(el.type)))
      retVal.append("{")
      retVal.append("  this->%s=val;"%(el.name))
      pKeyList=[el.name for el in objList if el.isKey]
      pKeyName=pKeyList[0]
      retVal.append("  std::ostringstream pKeyVal;");
      retVal.append("  pKeyVal << this->val01;")
      retVal.append("  std::ostringstream valSS;");
      retVal.append("  valSS << this->%s;"%(el.name))
      updateSql="UPDATE %s SET %s='%s' WHERE %s='%s'"%(className,el.name,'"+valSS.str()+"',pKeyName,'"+pKeyVal.str()+"')
      retVal.append('  DbConnector::instance()->execute("%s");'%(updateSql))
      retVal.append("}")
      retVal.append("")
    return retVal

  def gettersBody(self,className,objList):
    retVal=[]
    for el in [el for el in objList]:
      isPrimitiveType=(re.match(r'.*\((.*)\).*',el.type)==None)
      typeName=typeConverter(el.type) if isPrimitiveType else "%s::%s"%(className,userDefinedTypeName(el))
      retVal.append("%s %s::get%s() const"%(typeName,className,el.name[0].upper()+el.name[1:]));
      retVal.append("{");
      retVal.append("  return(this->%s);"%(el.name))
      retVal.append("}");
      retVal.append('')
    return retVal

  def populateFromSqlBody(self, className, objList):
    retVal=[]
    mutableAttribList=[el for el in objList if not el.isKey]
    retVal.append('void %s::populateFromSql(const DbConnector::KvpType& kvp)'%(className))
    retVal.append('{')
    for e in mutableAttribList:
      dType=typeConverter(e.type)
      baseTypeName=dType.split(":")[-1]
      convertFxn='DbConnector::convertTo%s(%s)'%(self.camelCase(baseTypeName),'kvp.at("%s")'%(e.name))
      retVal.append('  this->%s=%s;'%(e.name,convertFxn))
    retVal.append('}')
    return retVal
