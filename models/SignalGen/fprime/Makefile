MODEL = SignalSm
GOLDY = goldy.txt
BACK-END = fprime
COMPONENT = SignalGen
IMPLHEADER = SignalGen.hpp
NAMESPACE = Ref
INCLUDEDIRS = -I. \
              -IFw/SMEvents \
		-I../../TestModels

all: autocode build

autocode:
	@printf "**** Running the state-machine autocoder ****\n"
	../../../autocoder/Stars.py -backend $(BACK-END) -namespace $(NAMESPACE) -model ../$(MODEL).qm

build:
	@printf "**** Building an executable model ****\n"
	g++ -c -Wall $(MODEL).cpp $(INCLUDEDIRS) -o $(MODEL).o
	g++ -c -Wall testDrv.cpp $(INCLUDEDIRS) -o testDrv.o
	g++ -c -Wall sendEvent.cpp $(INCLUDEDIRS) -o sendEvent.o
	g++ -c -Wall SignalGen.cpp $(INCLUDEDIRS) -o SignalGen.o
	g++ -Wall main.cpp $(INCLUDEDIRS) $(MODEL).o testDrv.o sendEvent.o SignalGen.o -o test

run:
	@printf "**** Running the executable model ****\n"
	./test

ut:
	@./../../../autocoder/test/run.py $(MODEL) $(GOLDY) $(BACK-END)


clean:
	rm -rf test
	rm -rf *.o
