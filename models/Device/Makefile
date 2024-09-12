MAKEFLAGS += --no-print-directory

all: QM-C-depend \
     QM-CPP-depend \
     QM-QF-depend \
     QM-Fprime-depend \
     UML-C-depend \
     UML-Fprime-depend 

QM-C-depend:
	cd QM-C && make clean && make && make ut

QM-CPP-depend:
	cd QM-CPP && make clean && make && make ut

QM-QF-depend:
	cd QM-QF && make clean && make && make ut

QM-Fprime-depend:
	cd QM-Fprime && make clean && make && make ut && make checkfpp

UML-C-depend:
	cd UML-C && make clean && make && make ut

UML-Fprime-depend:
	cd UML-Fprime && make clean && make && make ut && make checkfpp

