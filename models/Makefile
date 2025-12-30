MAKEFLAGS += --no-print-directory

all: Hsm-depend \
	simple-depend \
	actions-depend \
	arg_actions-depend \
	cameo-depend \
	cases-depend \
	complex_composite-depend \
	complex_junction-depend \
	multiple_actions-depend \
	simple_composite-depend \
	simple_junction-depend \
	string_guards-depend \
	transitions-depend 

ut: simple-ut \
	actions-ut \
	arg_actions-ut \
	cameo-ut \
	cases-ut \
	complex_composite-ut \
	complex_junction-ut \
	multiple_actions-ut \
	simple_composite-ut \
	simple_junction-ut \
	string_guards-ut \
	transitions-ut 

clean: simple-clean \
	actions-clean \
	arg_actions-clean \
	cameo-clean \
	cases-clean \
	complex_composite-clean \
	complex_junction-clean \
	multiple_actions-clean \
	simple_composite-clean \
	simple_junction-clean \
	string_guards-clean \
	transitions-clean 


# ---------------
# All targets
# ---------------

Hsm-depend:
	cd ../QHsm && make

simple-depend:
	cd TestModels/simple && make

actions-depend:
	cd TestModels/actions && make

arg_actions-depend:
	cd TestModels/arg_actions && make

cameo-depend:
	cd TestModels/cameo && make

cases-depend:
	cd TestModels/cases && make

complex_composite-depend:
	cd TestModels/complex_composite && make

complex_junction-depend:
	cd TestModels/complex_junction && make

multiple_actions-depend:
	cd TestModels/multiple_actions && make

simple_composite-depend:
	cd TestModels/simple_composite && make

simple_junction-depend:
	cd TestModels/simple_junction && make

string_guards-depend:
	cd TestModels/string_guards && make

transitions-depend:
	cd TestModels/transitions && make


# ---------------
# Ut targets
# ---------------
simple-ut:
	cd TestModels/simple && make ut

actions-ut:
	cd TestModels/actions && make ut

arg_actions-ut:
	cd TestModels/arg_actions && make ut

cameo-ut:
	cd TestModels/cameo && make ut

cases-ut:
	cd TestModels/cases && make ut

complex_composite-ut:
	cd TestModels/complex_composite && make ut

complex_junction-ut:
	cd TestModels/complex_junction && make ut

multiple_actions-ut:
	cd TestModels/multiple_actions && make ut

simple_composite-ut:
	cd TestModels/simple_composite && make ut

simple_junction-ut:
	cd TestModels/simple_junction && make ut

string_guards-ut:
	cd TestModels/string_guards && make ut

transitions-ut:
	cd TestModels/transitions && make ut

# ---------------
# clean targets
# ---------------
simple-clean:
	cd TestModels/simple && make clean

actions-clean:
	cd TestModels/actions && make clean

arg_actions-clean:
	cd TestModels/arg_actions && make clean

cameo-clean:
	cd TestModels/cameo && make clean

cases-clean:
	cd TestModels/cases && make clean

complex_composite-clean:
	cd TestModels/complex_composite && make clean

complex_junction-clean:
	cd TestModels/complex_junction && make clean

multiple_actions-clean:
	cd TestModels/multiple_actions && make clean

simple_composite-clean:
	cd TestModels/simple_composite && make clean

simple_junction-clean:
	cd TestModels/simple_junction && make clean

string_guards-clean:
	cd TestModels/string_guards && make clean

transitions-clean:
	cd TestModels/transitions && make clean

