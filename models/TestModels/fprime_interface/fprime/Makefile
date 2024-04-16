
BACK-END = fprime
GOLDY = goldy.txt
NAMESPACE = Ref
INCLUDEDIRS = -I. \
              -IFw/SMEvents \
                -I../..

all: autocode build

autocode:
	@printf "**** Running the state-machine autocoder ****\n"
	../../../../autocoder/Stars.py -noImpl -backend $(BACK-END) -namespace $(NAMESPACE) -model ../Simple.plantuml
	../../../../autocoder/Stars.py -noImpl -backend $(BACK-END) -namespace $(NAMESPACE) -model ../Toggle.plantuml
	../../../../autocoder/Stars.py -smbase

build:
	@printf "**** Building an executable model ****\n"
	g++ -c -Wall Simple.cpp $(INCLUDEDIRS) -o Simple.o
	g++ -c -Wall Toggle.cpp $(INCLUDEDIRS) -o Toggle.o
	g++ -c -Wall testDrv.cpp $(INCLUDEDIRS) -o testDrv.o
	g++ -c -Wall SignalGen.cpp $(INCLUDEDIRS) -o SignalGen.o
	g++ -c -Wall SignalGenSmBase.cpp $(INCLUDEDIRS) -o SignalGenSmBase.o
	g++ -Wall main.cpp $(INCLUDEDIRS) Simple.o Toggle.o testDrv.o SignalGen.o SignalGenSmBase.o -o test

run:
	@printf "**** Running the executable model ****\n"
	./test

ut:
	@./../../../../autocoder/test/run.py Simple $(GOLDY) $(BACK-END)


clean:
	rm -rf test
	rm -rf *.o
	rm -rf *.hpp
	rm -rf *.cpp
	rm -rf *.h
