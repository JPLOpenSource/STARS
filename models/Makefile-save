

all: QHsm-build TestModels/simple-build TestModels/actions-build TestModels/multiple_actions-build TestModels/arg_actions-build TestModels/simple_composite-build TestModels/complex_composite-build TestModels/string_guards-build TestModels/transitions-build TestModels/simple_junction-build TestModels/complex_junction-build TestModels/cases-build TestModels/cameo-build 

ut: TestModels/simple-ut TestModels/actions-ut TestModels/multiple_actions-ut TestModels/arg_actions-ut TestModels/simple_composite-ut TestModels/complex_composite-ut TestModels/string_guards-ut TestModels/transitions-ut TestModels/simple_junction-ut TestModels/complex_junction-ut TestModels/cases-ut TestModels/cameo-ut FaultModels/MissingInitialTransition-ut FaultModels/MissingInitialTransition2-ut FaultModels/MultipleInitialTransition-ut FaultModels/DuplicateStateNames-ut FaultModels/JunctionNoGuard-ut FaultModels/JunctionNoGuard2-ut FaultModels/Junction3Trans-ut FaultModels/JunctionDoubleGuard-ut FaultModels/EntryExitArgs-ut FaultModels/EntryExitArgs2-ut FaultModels/EntryExitArgs3-ut FaultModels/EntryExitArgs4-ut FaultModels/EntryExitArgs5-ut 

run: TestModels/simple-run TestModels/actions-run TestModels/multiple_actions-run TestModels/arg_actions-run TestModels/simple_composite-run TestModels/complex_composite-run TestModels/string_guards-run TestModels/transitions-run TestModels/simple_junction-run TestModels/complex_junction-run TestModels/cases-run TestModels/cameo-run 

clean: QHsm-clean TestModels/simple-clean TestModels/actions-clean TestModels/multiple_actions-clean TestModels/arg_actions-clean TestModels/simple_composite-clean TestModels/complex_composite-clean TestModels/string_guards-clean TestModels/transitions-clean TestModels/simple_junction-clean TestModels/complex_junction-clean TestModels/cases-clean TestModels/cameo-clean 

QHsm-build:
	@cd ../QHsm; \
	make
	@cd ..

QHsm-clean:
	@cd ../QHsm; \
	make clean
	@cd ..


# --------------------------
# actions FaultModels/MissingInitialTransition
# --------------------------

FaultModels/MissingInitialTransition-ut:
	@cd FaultModels/MissingInitialTransition; \
	make --no-print-directory ut
	@cd ..
# --------------------------
# actions FaultModels/MissingInitialTransition2
# --------------------------

FaultModels/MissingInitialTransition2-ut:
	@cd FaultModels/MissingInitialTransition2; \
	make --no-print-directory ut
	@cd ..
# --------------------------
# actions FaultModels/MultipleInitialTransition
# --------------------------

FaultModels/MultipleInitialTransition-ut:
	@cd FaultModels/MultipleInitialTransition; \
	make --no-print-directory ut
	@cd ..
# --------------------------
# actions FaultModels/DuplicateStateNames
# --------------------------

FaultModels/DuplicateStateNames-ut:
	@cd FaultModels/DuplicateStateNames; \
	make --no-print-directory ut
	@cd ..
# --------------------------
# actions FaultModels/JunctionNoGuard
# --------------------------

FaultModels/JunctionNoGuard-ut:
	@cd FaultModels/JunctionNoGuard; \
	make --no-print-directory ut
	@cd ..
# --------------------------
# actions FaultModels/JunctionNoGuard2
# --------------------------

FaultModels/JunctionNoGuard2-ut:
	@cd FaultModels/JunctionNoGuard2; \
	make --no-print-directory ut
	@cd ..
# --------------------------
# actions FaultModels/Junction3Trans
# --------------------------

FaultModels/Junction3Trans-ut:
	@cd FaultModels/Junction3Trans; \
	make --no-print-directory ut
	@cd ..
# --------------------------
# actions FaultModels/JunctionDoubleGuard
# --------------------------

FaultModels/JunctionDoubleGuard-ut:
	@cd FaultModels/JunctionDoubleGuard; \
	make --no-print-directory ut
	@cd ..
# --------------------------
# actions FaultModels/EntryExitArgs
# --------------------------

FaultModels/EntryExitArgs-ut:
	@cd FaultModels/EntryExitArgs; \
	make --no-print-directory ut
	@cd ..
# --------------------------
# actions FaultModels/EntryExitArgs2
# --------------------------

FaultModels/EntryExitArgs2-ut:
	@cd FaultModels/EntryExitArgs2; \
	make --no-print-directory ut
	@cd ..
# --------------------------
# actions FaultModels/EntryExitArgs3
# --------------------------

FaultModels/EntryExitArgs3-ut:
	@cd FaultModels/EntryExitArgs3; \
	make --no-print-directory ut
	@cd ..
# --------------------------
# actions FaultModels/EntryExitArgs4
# --------------------------

FaultModels/EntryExitArgs4-ut:
	@cd FaultModels/EntryExitArgs4; \
	make --no-print-directory ut
	@cd ..
# --------------------------
# actions FaultModels/EntryExitArgs5
# --------------------------

FaultModels/EntryExitArgs5-ut:
	@cd FaultModels/EntryExitArgs5; \
	make --no-print-directory ut
	@cd ..


# --------------------------
# actions TestModels/simple
# --------------------------

TestModels/simple-clean:
	@cd TestModels/simple; \
	make clean
	@cd ..

TestModels/simple-build:
	@cd TestModels/simple; \
	make
	@cd ..

TestModels/simple-run:
	@cd TestModels/simple; \
	make run
	@cd ..

TestModels/simple-ut:
	@cd TestModels/simple; \
	make --no-print-directory ut
	@cd ..
        
# --------------------------
# actions TestModels/actions
# --------------------------

TestModels/actions-clean:
	@cd TestModels/actions; \
	make clean
	@cd ..

TestModels/actions-build:
	@cd TestModels/actions; \
	make
	@cd ..

TestModels/actions-run:
	@cd TestModels/actions; \
	make run
	@cd ..

TestModels/actions-ut:
	@cd TestModels/actions; \
	make --no-print-directory ut
	@cd ..
        
# --------------------------
# actions TestModels/multiple_actions
# --------------------------

TestModels/multiple_actions-clean:
	@cd TestModels/multiple_actions; \
	make clean
	@cd ..

TestModels/multiple_actions-build:
	@cd TestModels/multiple_actions; \
	make
	@cd ..

TestModels/multiple_actions-run:
	@cd TestModels/multiple_actions; \
	make run
	@cd ..

TestModels/multiple_actions-ut:
	@cd TestModels/multiple_actions; \
	make --no-print-directory ut
	@cd ..
        
# --------------------------
# actions TestModels/arg_actions
# --------------------------

TestModels/arg_actions-clean:
	@cd TestModels/arg_actions; \
	make clean
	@cd ..

TestModels/arg_actions-build:
	@cd TestModels/arg_actions; \
	make
	@cd ..

TestModels/arg_actions-run:
	@cd TestModels/arg_actions; \
	make run
	@cd ..

TestModels/arg_actions-ut:
	@cd TestModels/arg_actions; \
	make --no-print-directory ut
	@cd ..
        
# --------------------------
# actions TestModels/simple_composite
# --------------------------

TestModels/simple_composite-clean:
	@cd TestModels/simple_composite; \
	make clean
	@cd ..

TestModels/simple_composite-build:
	@cd TestModels/simple_composite; \
	make
	@cd ..

TestModels/simple_composite-run:
	@cd TestModels/simple_composite; \
	make run
	@cd ..

TestModels/simple_composite-ut:
	@cd TestModels/simple_composite; \
	make --no-print-directory ut
	@cd ..
        
# --------------------------
# actions TestModels/complex_composite
# --------------------------

TestModels/complex_composite-clean:
	@cd TestModels/complex_composite; \
	make clean
	@cd ..

TestModels/complex_composite-build:
	@cd TestModels/complex_composite; \
	make
	@cd ..

TestModels/complex_composite-run:
	@cd TestModels/complex_composite; \
	make run
	@cd ..

TestModels/complex_composite-ut:
	@cd TestModels/complex_composite; \
	make --no-print-directory ut
	@cd ..
        
# --------------------------
# actions TestModels/string_guards
# --------------------------

TestModels/string_guards-clean:
	@cd TestModels/string_guards; \
	make clean
	@cd ..

TestModels/string_guards-build:
	@cd TestModels/string_guards; \
	make
	@cd ..

TestModels/string_guards-run:
	@cd TestModels/string_guards; \
	make run
	@cd ..

TestModels/string_guards-ut:
	@cd TestModels/string_guards; \
	make --no-print-directory ut
	@cd ..
        
# --------------------------
# actions TestModels/transitions
# --------------------------

TestModels/transitions-clean:
	@cd TestModels/transitions; \
	make clean
	@cd ..

TestModels/transitions-build:
	@cd TestModels/transitions; \
	make
	@cd ..

TestModels/transitions-run:
	@cd TestModels/transitions; \
	make run
	@cd ..

TestModels/transitions-ut:
	@cd TestModels/transitions; \
	make --no-print-directory ut
	@cd ..
        
# --------------------------
# actions TestModels/simple_junction
# --------------------------

TestModels/simple_junction-clean:
	@cd TestModels/simple_junction; \
	make clean
	@cd ..

TestModels/simple_junction-build:
	@cd TestModels/simple_junction; \
	make
	@cd ..

TestModels/simple_junction-run:
	@cd TestModels/simple_junction; \
	make run
	@cd ..

TestModels/simple_junction-ut:
	@cd TestModels/simple_junction; \
	make --no-print-directory ut
	@cd ..
        
# --------------------------
# actions TestModels/complex_junction
# --------------------------

TestModels/complex_junction-clean:
	@cd TestModels/complex_junction; \
	make clean
	@cd ..

TestModels/complex_junction-build:
	@cd TestModels/complex_junction; \
	make
	@cd ..

TestModels/complex_junction-run:
	@cd TestModels/complex_junction; \
	make run
	@cd ..

TestModels/complex_junction-ut:
	@cd TestModels/complex_junction; \
	make --no-print-directory ut
	@cd ..
        
# --------------------------
# actions TestModels/cases
# --------------------------

TestModels/cases-clean:
	@cd TestModels/cases; \
	make clean
	@cd ..

TestModels/cases-build:
	@cd TestModels/cases; \
	make
	@cd ..

TestModels/cases-run:
	@cd TestModels/cases; \
	make run
	@cd ..

TestModels/cases-ut:
	@cd TestModels/cases; \
	make --no-print-directory ut
	@cd ..
        
# --------------------------
# actions TestModels/cameo
# --------------------------

TestModels/cameo-clean:
	@cd TestModels/cameo; \
	make clean
	@cd ..

TestModels/cameo-build:
	@cd TestModels/cameo; \
	make
	@cd ..

TestModels/cameo-run:
	@cd TestModels/cameo; \
	make run
	@cd ..

TestModels/cameo-ut:
	@cd TestModels/cameo; \
	make --no-print-directory ut
	@cd ..
        



