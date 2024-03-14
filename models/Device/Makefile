MAKEFLAGS += --no-print-directory

all: c-depend qf-depend
ut: c-ut qf-ut
run: c-run
clean: c-clean qf-clean

C: c-depend
QF: qf-depend

c-depend:
	cd C; \
        make
	cd ..

qf-depend:
	cd QF; \
        make
	cd ..

c-ut:
	@cd C; \
	make ut
	@cd ..

qf-ut:
	@cd QF; \
	make ut
	@cd ..

c-run:
	@cd C; \
	make run
	@cd ..

qf-run:
	@cd QF; \
	make run
	@cd ..

c-clean:
	@cd C; \
	make clean
	@cd ..

qf-clean:
	@cd QF; \
	make clean
	@cd ..

