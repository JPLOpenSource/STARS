MAKEFLAGS += --no-print-directory

all: UML-C-depend \
     UML-CPP-depend \
     UML-QF-depend \
     UML-Fprime-depend \
     Cameo-C-depend \
     Cameo-CPP-depend \
     Cameo-QF-depend \
     Cameo-Fprime-depend

ut:  UML-C-ut \
     UML-CPP-ut \
     UML-QF-ut \
     UML-Fprime-ut \
     Cameo-C-ut \
     Cameo-CPP-ut \
     Cameo-QF-ut \
     Cameo-Fprime-ut

# ---------------
# All targets
# ---------------

UML-C-depend:
	cd UML-C && make clean && make

UML-CPP-depend:
	cd UML-CPP && make clean && make

UML-QF-depend:
	cd UML-QF && make clean && make

UML-Fprime-depend:
	cd UML-Fprime && make clean && make

Cameo-C-depend:
	cd Cameo-C && make clean && make

Cameo-CPP-depend:
	cd Cameo-CPP && make clean && make

Cameo-QF-depend:
	cd Cameo-QF && make clean && make

Cameo-Fprime-depend:
	cd Cameo-Fprime && make clean && make

# ---------------
# UT targets
# ---------------

UML-C-ut:
	@cd UML-C && make ut

UML-CPP-ut:
	@cd UML-CPP && make ut

UML-QF-ut:
	@cd UML-QF && make ut

UML-Fprime-ut:
	@cd UML-Fprime && make ut && make checkfpp

Cameo-C-ut:
	@cd Cameo-C && make ut

Cameo-CPP-ut:
	@cd Cameo-CPP && make ut

Cameo-QF-ut:
	@cd Cameo-QF && make ut

Cameo-Fprime-ut:
	@cd Cameo-Fprime && make ut && make checkfpp

