.PHONY: test
all:

setup:
#	${SH} sudo apt-get install -y libmysqlcppconn-dev
#	${SH} sudo apt-get install -y mysql-server
#	${SH} sudo apt-get install -y python-mysql.connector
#	${SH} sudo apt-get install -y cpputest
#	${SH} sudo mysql -u root -e "CREATE USER 'dbadmin'@'localhost' IDENTIFIED BY 'Mariner'; GRANT ALL ON *.* TO 'dbadmin'@'localhost';"
#	${SH} sudo apt-get install -y liblog4cxx-dev

test:
	${SH} cd tests; make


clean:
	${SH} cd tests; make clean
	${RM} -rf ./__pycache__/
