CC=g++
LIBS += -L/usr/lib -lmysqlcppconn -llog4cxx
INCLUDE+="-I../"

all: Foo.cpp Foo
	${SH} ./Foo

Foo.cpp: MyTestDb01.odb
	${SH} ./testGenerator2 --verbose --input $^ --outfile $@ 

Foo: Foo.cpp MyTestDb01.h MyTestDb01.cpp ../DbConnector.cpp
	${CC} $^ -o $@ ${INCLUDE} ${LIBS}

%.h: %.odb
	${SH} ../odbPreprocessor.py --verbose --input $< --lang Cpp --outfile $@

clean:
	#--clobber odb output files
	${SH} rm -f $(shell find . -name "*.odb" | sed -e 's/.odb/.cpp/')
	${SH} rm -f $(shell find . -name "*.odb" | sed -e 's/.odb/.h/')
	${RM} Foo Foo.cpp
	${RM} -rf ./__pycache__

