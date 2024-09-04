MAKEFLAGS += --no-print-directory

all: QM-C-depend \
     QM-CPP-depend \
     QM-QF-depend \
     QM-Fprime-depend \
     UML-C-depend \
     UML-Fprime-depend \
     Cameo-C-depend \
     Cameo-QF-depend \
     Cameo-Fprime-depend

QM-C-depend:
	cd QM-C && make clean && make && make ut

QM-CPP-depend:
	cd QM-CPP && make clean && make && make ut

QM-QF-depend:
	cd QM-QF && make clean && make && make ut

QM-Fprime-depend:
	cd QM-Fprime && make clean && make && make ut

UML-C-depend:
	cd UML-C && make clean && make && make ut

UML-Fprime-depend:
	cd UML-Fprime && make clean && make && make ut

Cameo-C-depend:
	cd Cameo-C && make clean && make && make ut

Cameo-QF-depend:
	cd Cameo-QF && make clean && make && make ut

Cameo-Fprime-depend:
	cd Cameo-Fprime && make clean && make && make ut

