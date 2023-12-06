#include "DbConnector.h"
#include <sstream>
#include <map>

DbConnector* DbConnector::instance()
{
  static DbConnector* obj=new DbConnector();
  return obj;
}

DbConnector::DbConnector():driver(get_driver_instance()),con(driver->connect("tcp://127.0.0.1:3306", "dbadmin", "Mariner"))
{
  const std::string DbName("MyDb01");
  try {
    con->setSchema(DbName);
  } catch(sql::SQLException)
  {
    execute("CREATE DATABASE "+ DbName + ";");
    con->setSchema(DbName);
  }
}

void DbConnector::execute(const std::string& command)
{
//std::cout << "" << __FILE__ << ":" << __LINE__ << " executing: '" << command << "'" << std::endl;
  sql::Statement *stmt = con->createStatement();
  const bool success = stmt->execute(command.c_str());
}

DbConnector::KvpList DbConnector::executeQuery(const std::string& command)
{
//std::cout << "" << __FILE__ << ":" << __LINE__ << " executing: '" << command << "'" << std::endl;

  KvpList retVal;
  sql::Statement *stmt = con->createStatement();
  sql::ResultSet *res = stmt->executeQuery(command.c_str());
  sql::ResultSetMetaData* res_meta = res->getMetaData();
  for(int i=0; i<res_meta->getColumnCount(); ++i)
  {
  const int dbIndex=i+1;

  while (res->next())
  {
    KvpType valMap;
    for(int i=0; i<res_meta->getColumnCount(); ++i)
    {
      const int dbIndex=i+1;
      const std::string fLabel=res_meta->getColumnLabel(dbIndex);
      const std::string fType=res_meta->getColumnTypeName(dbIndex);
      valMap[fLabel]=res->getString(fLabel);
    }
    retVal.push_back(valMap);
  }

  }

  return (retVal);
}

bool DbConnector::tableExists(const std::string& tableName) 
{
  bool retVal=false;
  std::ostringstream ss;
  ss << "DESCRIBE " << tableName << ";";
  try
  {
    executeQuery(ss.str());
    retVal=true;
  }
  catch(sql::SQLException e)
  { 
    retVal=false;
  }
  return retVal;
}

std::string DbConnector::convertToString(const int& val)
{
  std::ostringstream ss;
  ss << val;
  return ss.str();
}

std::string convertToString(const float& val)
{
  std::ostringstream ss;
  ss << val;
  return ss.str();
}

std::string convertToString(const double& val)
{
  std::ostringstream ss;
  ss << val;
  return ss.str();
}

std::string convertToString(const long& val)
{
  std::ostringstream ss;
  ss << val;
  return ss.str();
}


int DbConnector::convertToInt(const std::string& val)
{
  return(stoi(val));
}

float DbConnector::convertToFloat(const std::string& val)
{
  return std::stof(val);
}

double DbConnector::convertToDouble(const std::string& val)
{
  return std::stod(val);
}

long DbConnector::convertToLong(const std::string& val)
{
  return std::stold(val);
}

