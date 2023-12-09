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
               'varchar'  :  'std::string',
               'int'      :  'int',
               'double'   :  'double',
               'date'     :  'std::string',
               'datetime' :  'std::string',
             }
  VarLenMapper={
               'char(%s)'%(size)  : 'VarChar%s'%(size),
               }
  return VarLenMapper[dbType] if m else TypeMapper[dbType]

class CppGenerator:
  def __init__(self, moduleName, objList):
    logging.debug("moduleName %s; objList %s"%(moduleName,str(objList)))
    self.moduleName=moduleName
    self.objList=objList
    self.createHeader()
    self.createBody()

  @staticmethod
  def camelCase(L):
    if(len(L)):
      retVal=[L[0][0].upper()+L[0][1:]]
      for e in [el for el in camelCase(L[1:])]: 
        retVal.append(e)
      return "".join(retVal)
    else:
      return ""

  def createHeader(self):
    with open(self.moduleName+".h",'w+') as fp:
      macroName=("%s_h"%(self.moduleName)).upper()
      fp.write("#ifndef %s\n"%(macroName));
      fp.write("#define %s\n"%(macroName));
      fp.write("#include <string>\n")
      fp.write("#include <cstring>\n")
      fp.write('#include <iostream>\n')
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
#       fp.write('\n'.join(self.gettersBody(k,v)))
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
#   for el in self.gettersDef(className,objList):
#     retVal.append("    %s"%(el))

    for el in self.populateFromSqlDef(className,objList):
      retVal.append("    %s"%(el))

    retVal.append("  private:");
    for el in self.attribDef(objList):
      retVal.append("    %s"%(el))
    retVal.append("};");
    return retVal

  def genVarCharType(self, className, obj):
    retVal=[]
    retVal.append('typedef struct type24')
    retVal.append('{')
    retVal.append('  char val_[24];')
    retVal.append('  const char& operator[](int i) const { return val_[i];}')
    retVal.append('  char& operator[](int i){return val_[i];}')

    retVal.append("  type24(){memset(val_, '\\0', sizeof(val_));}")
    retVal.append('  type24(std::string val)')
    retVal.append('  {')
    retVal.append('    // initialize buffer to EOF string end indicator')
    retVal.append('    //  then, initialize with specified value while')
    retVal.append('    //  not overflowing the buffer');
    retVal.append('    // throw std::out_of_range exception if the specified')
    retVal.append('    // exceeds the capacity of the buffer length')
    retVal.append("                           memset(val_, '\\0', sizeof(val_));")
    retVal.append('                           const int len1=sizeof(val_)-1;')
    retVal.append('                           const int len2=val.length();')
    retVal.append('                           memcpy(val_,val.c_str(),std::min(len1,len2));')
    retVal.append('                         }')

    retVal.append('} VarChar24;')
    retVal.append('friend std::ostream& operator<<(std::ostream &ss, const VarChar24& val) {')
    retVal.append('  for(int i=0; i<sizeof(val); ++i) ss << val[i];')
    retVal.append('  return (ss);')
    retVal.append('}')
    return retVal

  def genVarLenTypes(self, className, objList):
    retVal=[]
    #varElList=[el for el in objList if re.match(r'.*\(.*\).*',el.name)]
    #varElList=[el for el in objList if re.match(r'.*\(.*\).*',el.name)]
    for obj in [el for el in objList if re.match(r'.*\(.*\).*',el.name)]:
      for e in self.genVarCharType(className, obj):
        retVal.append(e)

    return retVal

  def ctorDef(self,className,objList):
    retVal=list()
    argList=["const %s& %s"%(typeConverter(el.name),el.type) for el in [e for e in objList if e[2]]]
    retVal.append("%s(%s);"%(className,','.join(argList)))
    return retVal

  def setterSigniture(el):
    retVal=[]
    retVal.append('void set%s(%s %s)'%(el.name),'el.type','el.name')
    return retVal

  def settersDef(self,className,objList):
    retVal=[]
    for el in [el for el in objList if not el[2]]:
      retVal.append("void set%s(const %s& val);"%(camelCase([el.type]),typeConverter(el.name)));
    return retVal

  def gettersDef(self,className,objList):
    retVal=[]
    for el in [el for el in objList]:
      retVal.append("%s get%s() const;"%(typeConverter(el.name),el.type[0].upper()+el.type[1:]));
    return retVal

  def populateFromSqlDef(self, className, objList):
    retVal=[]
    retVal.append('//@todo; move to private?')
    retVal.append('void populateFromSql(const DbConnector::KvpType& kvp);')
    return retVal

  def attribDef(self,objList):
    return ['%s%s %s;'%('const ' if e[2] else '',typeConverter(e.name),e.type) for e in objList]


  #--================================================================================
  #-- Body Components
  #--================================================================================
  def ctorBody(self,className,objList):
    retVal=list()
    argList=["const %s& %s"%(typeConverter(el.name),el.type) for el in [e for e in objList if e[2]]]
    initList=["%s(%s)"%(e.type,e[0] if e[2] else '') for e in objList]
    fList=["%s %s%s"%(e.type,e.name,' NOT NULL' if e[2] else '') for e in objList]
    pList=[e[0] for e in objList if e[2]]
    createTableSql="CREATE TABLE %s (%s%s);"%(className,','.join(fList),',PRIMARY KEY(%s)'%(','.join(pList)) if len(pList) else '')
    insertSql='INSERT INTO %s (%s) VALUES (%s);'%(className,','.join([e.type for e in objList]),'" + ss.str().substr(0,ss.str().length()-1) + "')

    ssList=['ss << "\'" << this->%s << "\',";'%(e.type) for e in objList]
    
    retVal.append("%s::%s(%s)%s"%(className,className,','.join(argList),':'+','.join(initList)))
    retVal.append("{")
    retVal.append("  std::ostringstream ss;")
    for e in ssList:
      retVal.append("  %s"%(e))
    retVal.append('  if (DbConnector::instance()->tableExists("%s"))'%(className));
    retVal.append('  {')
    retVal.append('    try {')
    retVal.append('      DbConnector::instance()->execute("%s");'%(insertSql))
    retVal.append('    } catch(sql::SQLException e)')
    retVal.append('    {')
    retVal.append('      std::string error=e.what();')
    retVal.append('      const bool isDup=(error.find("Duplicate entry")!=std::string::npos) && (error.find("PRIMARY")!=std::string::npos);')
    retVal.append('      if(isDup)')
    retVal.append('      {')
    retVal.append('        std::ostringstream ss;')
    retVal.append('        ss << "SELECT * FROM %s WHERE %s=\'" << this->val01 << "\' LIMIT 1;";'%(className,argList[0]))
    retVal.append('        DbConnector::KvpList results=DbConnector::instance()->executeQuery("SELECT * from MyRecord01 WHERE val01=\'1\' LIMIT 1");')
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
    for el in [el for el in objList if not el[2]]:
      retVal.append("void %s::set%s(const %s& val)"%(className,camelCase([el.type]),typeConverter(el.name)));
      retVal.append("{")
      retVal.append("  this->%s=val;"%(el.type))
      pKeyList=[el.type for el in objList if el[2]]
      retVal.append("  std::ostringstream pKeyVal;");
      retVal.append('  pKeyVal<<this->val01;')
      retVal.append("  std::ostringstream valSS;");
      retVal.append("  valSS << val;")
      updateSql='UPDATE %s SET %s=\'"+valSS.str()+"\' WHERE (%s="+pKeyVal.str()+");'%(className,el.type,pKeyList.type)
      retVal.append('  DbConnector::instance()->execute("%s");'%(updateSql))
      retVal.append("}")
      retVal.append("")
    return retVal

  def gettersBody(self,className,objList):
    retVal=[]
    for el in [el for el in objList]:
      retVal.append("%s %s::get%s() const"%(typeConverter(el.name),className,el.type[0].upper()+el.type[1:]));
      retVal.append("{");
      retVal.append("  return(this->%s);"%(el.type))
      retVal.append("}");
      retVal.append('')
    return retVal

  def populateFromSqlBody(self, className, objList):
    retVal=[]
    retVal.append('//populateFromSqlBody')
    mutableAttribList=[el for el in objList if not el[2]]
    retVal.append('void %s::populateFromSql(const DbConnector::KvpType& kvp)'%(className))
    retVal.append('{')
    for e in mutableAttribList:
      dType=typeConverter(e.name)
      camelCaseType="%s%s"%(camelCase([dType]))
      typeConvertFx='DbConnector::convertTo%s(%s)'%(camelCaseType,'kvp.at("%s")'%(e.type)) if dType != 'std::string' else 'kvp.at("%s")'%e.type
      retVal.append('  this->%s=%s;'%(e.type,typeConvertFx))
    retVal.append('}')
    retVal.append('')
    return retVal
