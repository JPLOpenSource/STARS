all:
	gcc -c -Wall hsm_qf.c -o hsm_qf.o
	gcc -c -Wall log_event.c -o log_event.o
	ar rs libqhsm.a hsm_qf.o log_event.o

clean:
	rm -f libqhsm.a
	rm -f hsm_qf.o
	rm -f log_event.o
