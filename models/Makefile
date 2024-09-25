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
	cd TestModels/simple/UML-Fprime && make autocode && make build
	cd TestModels/simple/Cameo-Fprime && make autocode && make build

actions-depend:
	cd TestModels/actions/QM-Fprime && make autocode && make build
	cd TestModels/actions/UML-Fprime && make autocode && make build
	cd TestModels/actions/Cameo-Fprime && make autocode && make build

arg_actions-depend:
	cd TestModels/arg_actions/QM-Fprime && make autocode && make
	cd TestModels/arg_actions/UML-Fprime && make autocode && make build
	cd TestModels/arg_actions/Cameo-Fprime && make autocode && make build

cases-depend:
	cd TestModels/cases/QM-Fprime && make autocode && make build
	cd TestModels/cases/UML-Fprime && make autocode && make build
	cd TestModels/cases/Cameo-Fprime && make autocode && make build

complex_composite-depend:
	cd TestModels/complex_composite/QM-Fprime && make autocode && make
	cd TestModels/complex_composite/UML-Fprime && make autocode && make build
	cd TestModels/complex_composite/Cameo-Fprime && make autocode && make build

complex_junction-depend:
	cd TestModels/complex_junction/QM-Fprime && make autocode && make
	cd TestModels/complex_junction/UML-Fprime && make autocode && make build
	cd TestModels/complex_junction/Cameo-Fprime && make autocode && make build

multiple_actions-depend:
	cd TestModels/multiple_actions/QM-Fprime && make autocode && make
	cd TestModels/multiple_actions/UML-Fprime && make autocode && make build
	cd TestModels/multiple_actions/Cameo-Fprime && make autocode && make build

simple_composite-depend:
	cd TestModels/simple_composite/QM-Fprime && make autocode && make
	cd TestModels/simple_composite/UML-Fprime && make autocode && make build
	cd TestModels/simple_composite/Cameo-Fprime && make autocode && make build

simple_junction-depend:
	cd TestModels/simple_junction/QM-Fprime && make autocode && make
	cd TestModels/simple_junction/UML-Fprime && make autocode && make build
	cd TestModels/simple_junction/Cameo-Fprime && make autocode && make build

string_guards-depend:
	cd TestModels/string_guards/QM-Fprime && make autocode && make
	cd TestModels/string_guards/UML-Fprime && make autocode && make build
	cd TestModels/string_guards/Cameo-Fprime && make autocode && make build

transitions-depend:
	cd TestModels/transitions/QM-Fprime && make autocode && make
	cd TestModels/transitions/UML-Fprime && make autocode && make build
	cd TestModels/transitions/Cameo-Fprime && make autocode && make build

# ---------------
# ut targets
# ---------------

simple-ut:
	@cd TestModels/simple/QM-Fprime && make ut
	@cd TestModels/simple/UML-Fprime && make ut
	@cd TestModels/simple/Cameo-Fprime && make ut

actions-ut:
	@cd TestModels/actions/QM-Fprime && make ut
	@cd TestModels/actions/UML-Fprime && make ut
	@cd TestModels/actions/Cameo-Fprime && make ut

arg_actions-ut:
	@cd TestModels/arg_actions/QM-Fprime && make ut
	@cd TestModels/arg_actions/UML-Fprime && make ut
	@cd TestModels/arg_actions/Cameo-Fprime && make ut

cases-ut:
	@cd TestModels/cases/QM-Fprime && make ut
	@cd TestModels/cases/UML-Fprime && make ut
	@cd TestModels/cases/Cameo-Fprime && make ut

complex_composite-ut:
	@cd TestModels/complex_composite/QM-Fprime && make ut
	@cd TestModels/complex_composite/UML-Fprime && make ut
	@cd TestModels/complex_composite/Cameo-Fprime && make ut

complex_junction-ut:
	@cd TestModels/complex_junction/QM-Fprime && make ut
	@cd TestModels/complex_junction/UML-Fprime && make ut
	@cd TestModels/complex_junction/Cameo-Fprime && make ut

multiple_actions-ut:
	@cd TestModels/multiple_actions/QM-Fprime && make ut
	@cd TestModels/multiple_actions/UML-Fprime && make ut
	@cd TestModels/multiple_actions/Cameo-Fprime && make ut

simple_composite-ut:
	@cd TestModels/simple_composite/QM-Fprime && make ut
	@cd TestModels/simple_composite/UML-Fprime && make ut
	@cd TestModels/simple_composite/Cameo-Fprime && make ut

simple_junction-ut:
	@cd TestModels/simple_junction/QM-Fprime && make ut
	@cd TestModels/simple_junction/UML-Fprime && make ut
	@cd TestModels/simple_junction/Cameo-Fprime && make ut

string_guards-ut:
	@cd TestModels/string_guards/QM-Fprime && make ut
	@cd TestModels/string_guards/UML-Fprime && make ut
	@cd TestModels/string_guards/Cameo-Fprime && make ut

transitions-ut:
	@cd TestModels/transitions/QM-Fprime && make ut
	@cd TestModels/transitions/UML-Fprime && make ut
	@cd TestModels/transitions/Cameo-Fprime && make ut

