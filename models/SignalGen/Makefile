MAKEFLAGS += --no-print-directory

all: fprime-depend
ut: fprime-ut
run: fprime-run
clean: fprime-clean

FPRIME: fprime-depend

fprime-depend:
	cd fprime; \
        make
	cd ..

fprime-ut:
	@cd fprime; \
	make ut
	@cd ..

fprime-run:
	@cd fprime; \
	make run
	@cd ..

fprime-clean:
	@cd fprime; \
	make clean
	@cd ..

