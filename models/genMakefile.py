#!/usr/bin/env python
from Cheetah.Template import Template


modellist = [
             "TestModels/simple", 
             "TestModels/actions", 
             "TestModels/multiple_actions", 
             "TestModels/arg_actions", 
             "TestModels/simple_composite", 
             "TestModels/complex_composite", 
             "TestModels/string_guards", 
             "TestModels/transitions", 
             "TestModels/simple_junction",
             "TestModels/complex_junction",
             "TestModels/cases",
             "TestModels/cameo"
           ]

faultlist = [
             "FaultModels/MissingInitialTransition",
             "FaultModels/MissingInitialTransition2",
             "FaultModels/MultipleInitialTransition",
             "FaultModels/DuplicateStateNames",
             "FaultModels/JunctionNoGuard",
             "FaultModels/JunctionNoGuard2",
             "FaultModels/Junction3Trans",
             "FaultModels/JunctionDoubleGuard",
             "FaultModels/EntryExitArgs",
             "FaultModels/EntryExitArgs2",
             "FaultModels/EntryExitArgs3",
             "FaultModels/EntryExitArgs4",
             "FaultModels/EntryExitArgs5"
            ]

template = Template("""

all: QHsm-build #slurp
#for $model in $modellist 
$model-build #end for

ut: #slurp
#for $model in $modellist + $faultlist
$model-ut #end for

run: #slurp
#for $model in $modellist 
$model-run #end for

clean: QHsm-clean #slurp
#for $model in $modellist 
$model-clean #end for

QHsm-build:
	@cd ../QHsm; \\
	make
	@cd ..

QHsm-clean:
	@cd ../QHsm; \\
	make clean
	@cd ..


#for fault in $faultlist
# --------------------------
# actions $fault
# --------------------------

$fault-ut:
	@cd $fault; \\
	make --no-print-directory ut
	@cd ..
#end for


#for model in $modellist
# --------------------------
# actions $model
# --------------------------

$model-clean:
	@cd $model; \\
	make clean
	@cd ..

$model-build:
	@cd $model; \\
	make
	@cd ..

$model-run:
	@cd $model; \\
	make run
	@cd ..

$model-ut:
	@cd $model; \\
	make --no-print-directory ut
	@cd ..
        
#end for


""")


template.modellist = modellist
template.faultlist = faultlist
print (str(template))
