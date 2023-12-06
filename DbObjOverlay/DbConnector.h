#ifndef DBCONNECTOR_H
#define DBCONNECTOR_H
#include "mysql_connection.h"
#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/statement.h>
#include <string>
#include <vector>
#include <map>

class DbConnector
{
  public:
    static DbConnector* instance();
    void execute(const std::string& command);
    typedef std::map<std::string, std::string> KvpType;
    typedef std::vector<KvpType> KvpList;
    KvpList executeQuery(const std::string& command);
    bool tableExists(const std::string& tableName);

    static std::string convertToString(const int& val);
    static std::string convertToString(const float& val);
    static std::string convertToString(const double& val);
    static std::string convertToString(const long& val);

    static int convertToInt(const std::string& val);
    static float convertToFloat(const std::string& val);
    static double convertToDouble(const std::string& val);
    static long convertToLong(const std::string& val);
  private:
    DbConnector();
    sql::Driver *driver;
    sql::Connection *con;
};
#endif
