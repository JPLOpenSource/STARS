MAKEFLAGS += --no-print-directory

all: simple-depend \
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


# ---------------
# All targets
# ---------------
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

