MAKEFLAGS += --no-print-directory

all: cpp-depend
ut: cpp-ut
run: cpp-run
clean: cpp-clean

CPP: cpp-depend

cpp-depend:
	cd C++; \
        make
	cd ..

cpp-ut:
	@cd C++; \
	make ut
	@cd ..

cpp-run:
	@cd C++; \
	make run
	@cd ..

cpp-clean:
	@cd C++; \
	make clean
	@cd ..

