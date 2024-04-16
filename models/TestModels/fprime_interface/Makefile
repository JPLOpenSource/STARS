all: fprime-depend
ut: fprime-ut
run: fprime-run
clean: fprime-clean


C: c-depend
QF: qf-depend
CPP: cpp-depend
FPRIME: fprime-depend
QF-Cameo: qf-cameo-depend
UML: uml-depend

uml-depend:
	@cd C-UML; \
        make
	@cd ..

c-depend:
	@cd C; \
        make
	@cd ..

qf-depend:
	@cd QF; \
        make
	@cd ..

qf-cameo-depend:
	@cd QF-Cameo; \
        make
	@cd ..

cpp-depend:
	@cd C++; \
        make
	@cd ..

fprime-depend:
	@cd fprime; \
	make
	@cd ..

uml-clean:
	@cd C-UML; \
        make clean
	@cd ..

c-clean:
	@cd C; \
        make clean
	@cd ..

qf-clean:
	@cd QF; \
        make clean
	@cd ..

qf-cameo-clean:
	@cd QF-Cameo; \
        make clean
	@cd ..

cpp-clean:
	@cd C++; \
        make clean
	@cd ..

fprime-clean:
	@cd fprime; \
	make clean
	@cd ..

uml-ut:
	@cd C-UML; \
	make ut
	@cd ..

c-ut:
	@cd C; \
	make ut
	@cd ..

qf-ut:
	@cd QF; \
	make ut
	@cd ..

qf-cameo-ut:
	@cd QF-Cameo; \
	make ut
	@cd ..

cpp-ut:
	@cd C++; \
	make ut
	@cd ..

fprime-ut:
	@cd fprime; \
	make ut
	@cd ..

c-run:
	@cd C; \
	make run
	@cd ..

uml-run:
	@cd C-UML; \
	make run
	@cd ..

qf-run:
	@cd QF; \
	make run
	@cd ..

qf-cameo-run:
	@cd QF-Cameo; \
	make run
	@cd ..

cpp-run:
	@cd C++; \
	make run
	@cd ..

fprime-run:
	@cd fprime; \
	make run
	@cd ..
