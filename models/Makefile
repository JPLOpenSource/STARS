MAKEFLAGS += --no-print-directory

all: Hsm-depend \
	simple-depend \
	actions-depend \
	arg_actions-depend \
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

Hsm-depend:
	cd ../QHsm && make

simple-depend:
	cd TestModels/simple/QM-Fprime && make autocode && make build

actions-depend:
	cd TestModels/actions/QM-Fprime && make autocode && make build

arg_actions-depend:
	cd TestModels/arg_actions/QM-Fprime && make autocode && make

cases-depend:
	cd TestModels/cases/QM-Fprime && make autocode && make build

complex_composite-depend:
	cd TestModels/complex_composite/QM-Fprime && make autocode && make

complex_junction-depend:
	cd TestModels/complex_junction/QM-Fprime && make autocode && make

multiple_actions-depend:
	cd TestModels/multiple_actions/QM-Fprime && make autocode && make

simple_composite-depend:
	cd TestModels/simple_composite/QM-Fprime && make autocode && make

simple_junction-depend:
	cd TestModels/simple_junction/QM-Fprime && make autocode && make

string_guards-depend:
	cd TestModels/string_guards/QM-Fprime && make autocode && make

transitions-depend:
	cd TestModels/transitions/QM-Fprime && make autocode && make

# ---------------
# ut targets
# ---------------

simple-ut:
	cd TestModels/simple/QM-Fprime && make ut

actions-ut:
	cd TestModels/actions/QM-Fprime && make ut

arg_actions-ut:
	cd TestModels/arg_actions/QM-Fprime && make ut

cases-ut:
	cd TestModels/cases/QM-Fprime && make ut

complex_composite-ut:
	cd TestModels/complex_composite/QM-Fprime && make ut

complex_junction-ut:
	cd TestModels/complex_junction/QM-Fprime && make ut

multiple_actions-ut:
	cd TestModels/multiple_actions/QM-Fprime && make ut

simple_composite-ut:
	cd TestModels/simple_composite/QM-Fprime && make ut

simple_junction-ut:
	cd TestModels/simple_junction/QM-Fprime && make ut

string_guards-ut:
	cd TestModels/string_guards/QM-Fprime && make ut

transitions-ut:
	cd TestModels/transitions/QM-Fprime && make ut

