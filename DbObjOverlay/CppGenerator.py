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

  def createHeader(self):
    with open(self.moduleName+".h",'w+') as fp:
      macroName=("%s_h"%(self.moduleName)).upper()
      fp.write("#ifndef %s\n"%(macroName));
      fp.write("#define %s\n"%(macroName));
      fp.write("#include <string>\n")
      fp.write('#include "DbConnector.h"\n')
      for k,v in self.objList.items():
        L=self.classDef(k,v)
        fp.write("\n".join(L)+"\n")
      fp.write("#endif\n");

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

  def genVarLenTypes(self, className, objList):
    retVal=[]
    varElList=[el for el in objList if re.match(r'.*\(.*\).*',el[1])]
    retVal.append('typedef struct type24')
    retVal.append('{')
    retVal.append('char x[24];')
    retVal.append('const char& operator[](int i) const { return x[i];}')
    retVal.append('} VarChar24;')
    retVal.append('')
    retVal.append('')
    return retVal

  def ctorDef(self,className,objList):
    retVal=list()
    argList=["const %s& %s"%(typeConverter(el[1]),el[0]) for el in [e for e in objList if e[2]]]
    retVal.append("%s(%s);"%(className,','.join(argList)))
    return retVal

  def populateFromSqlDef(self, className, objList):
    retVal=[]
    retVal.append('//@todo; move to private?')
    retVal.append('void populateFromSql(const DbConnector::KvpType& kvp);')
    return retVal

  def populateFromSqlBody(self, className, objList):
    retVal=[]
    retVal.append('//populateFromSqlBody')
    mutableAttribList=[el for el in objList if not el[2]]
    retVal.append('void %s::populateFromSql(const DbConnector::KvpType& kvp)'%(className))
    retVal.append('{')
    for e in mutableAttribList:
      dType=typeConverter(e[1])
      camelCaseType="%s%s"%(dType[0].upper(),dType[1:])
      typeConvertFx='DbConnector::convertTo%s(%s)'%(camelCaseType,'kvp.at("%s")'%(e[0])) if dType != 'std::string' else 'kvp.at("%s")'%e[0]
      retVal.append('  this->%s=%s;'%(e[0],typeConvertFx))
    retVal.append('}')
    retVal.append('')
    return retVal

  def settersDef(self,className,objList):
    retVal=[]
    for el in [el for el in objList if not el[2]]:
      retVal.append("void set%s(const %s& val);"%(el[0][0].upper()+el[0][1:],typeConverter(el[1])));
    return retVal

  def settersBody(self,className,objList):
    retVal=[]
    for el in [el for el in objList if not el[2]]:
      retVal.append("void %s::set%s(const %s& val)"%(className,el[0][0].upper()+el[0][1:],typeConverter(el[1])));
      retVal.append("{")
      retVal.append("  this->%s=val;"%(el[0]))
      pKeyList=[el[0] for el in objList if el[2]]
      retVal.append("  std::ostringstream pKeyVal;");
      retVal.append('  pKeyVal<<this->val01;')
      retVal.append("  std::ostringstream valSS;");
      retVal.append("  valSS << val;")
      updateSql='UPDATE %s SET %s=\'"+valSS.str()+"\' WHERE (%s="+pKeyVal.str()+");'%(className,el[0],pKeyList[0])
      retVal.append('  DbConnector::instance()->execute("%s");'%(updateSql))
      retVal.append("}")
      retVal.append("")
    return retVal

  def gettersDef(self,className,objList):
    retVal=[]
    for el in [el for el in objList]:
      retVal.append("%s get%s() const;"%(typeConverter(el[1]),el[0][0].upper()+el[0][1:]));
    return retVal

  def gettersBody(self,className,objList):
    retVal=[]
    for el in [el for el in objList]:
      retVal.append("%s %s::get%s() const"%(typeConverter(el[1]),className,el[0][0].upper()+el[0][1:]));
      retVal.append("{");
      retVal.append("  return(this->%s);"%(el[0]))
      retVal.append("}");
      retVal.append('')
    return retVal

  def attribDef(self,objList):
    return ['%s%s %s;'%('const ' if e[2] else '',typeConverter(e[1]),e[0]) for e in objList]

  def ctorBody(self,className,objList):
    retVal=list()
    argList=["const %s& %s"%(typeConverter(el[1]),el[0]) for el in [e for e in objList if e[2]]]
    initList=["%s(%s)"%(e[0],e[0] if e[2] else '') for e in objList]
    fList=["%s %s%s"%(e[0],e[1],' NOT NULL' if e[2] else '') for e in objList]
    pList=[e[0] for e in objList if e[2]]
    createTableSql="CREATE TABLE %s (%s%s);"%(className,','.join(fList),',PRIMARY KEY(%s)'%(','.join(pList)) if len(pList) else '')
    insertSql='INSERT INTO %s (%s) VALUES (%s);'%(className,','.join([e[0] for e in objList]),'" + ss.str().substr(0,ss.str().length()-1) + "')

    ssList=['ss << "\'" << this->%s << "\',";'%(e[0]) for e in objList]
    
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

