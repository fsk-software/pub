CC=g++
LIBS += -L/usr/lib -lmysqlcppconn -llog4cxx
INCLUDE+="-I../"

all: Foo.cpp Foo
	${SH} ./Foo

go:
	${SH} ln -sf ../odbPreprocessor odbPreprocessor.py

Foo.cpp:
	${SH} ./testGenerator > $@

Foo: MyDb01.h MyDb01.cpp ../DbConnector.cpp
	${CC} $@.cpp $^ -o $@ ${INCLUDE} ${LIBS}

%.h: %.odb
	${SH} ../odbPreprocessor --verbose --input $< --lang Cpp --outfile $@

clean:
	#--clobber odb output files
	${SH} rm -f $(shell find . -name "*.odb" | sed -e 's/.odb/.cpp/')
	${SH} rm -f $(shell find . -name "*.odb" | sed -e 's/.odb/.h/')
	${RM} Foo Foo.cpp
	${RM} -rf ./__pycache__

