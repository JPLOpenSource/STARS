MODEL = Device
GOLDY = goldy.txt
BACK-END = qf 
IMPL = $(MODEL)Impl

INCLUDEDIRS = -I. \
              -I../../../QHsm

all: autocode build 

autocode:
	@printf "**** Running the state-machine autocoder ****\n"
	../../../autocoder/Stars.py $(BACK-END) ../$(MODEL).qm

build:
	@printf "**** Building an executable model ****\n"
	gcc -c -Wall $(INCLUDEDIRS) $(MODEL).c -o $(MODEL).o
	gcc -c -Wall $(INCLUDEDIRS) $(IMPL).c -o $(IMPL).o
	gcc -c -Wall $(INCLUDEDIRS) main.c -o main.o
	gcc -c -Wall $(INCLUDEDIRS) testDrv.c -o testDrv.o
	gcc -c -Wall $(INCLUDEDIRS) sendEvent.c -o sendEvent.o
	gcc -o test $(MODEL).o $(IMPL).o main.o testDrv.o sendEvent.o -L../../../QHsm -lqhsm

run:
	@printf "**** Running the executable model ****\n"
	./test

ut:
	@./../../../autocoder/test/run.py $(MODEL) $(GOLDY) $(BACK-END)

clean:
	rm -rf test    
	rm -rf *.o
