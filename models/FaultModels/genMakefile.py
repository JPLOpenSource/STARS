#!/usr/bin/env python
from Cheetah.Template import Template

modelList = [
             "MissingInitialTransition",
             "MissingInitialTransition2",
             "MissingInitialTransition3",
             "MultipleInitialTransition",
             "DuplicateStateNames",
             "JunctionNoGuard",
             "JunctionNoGuard2",
             "Junction3Trans",
             "JunctionDoubleGuard",
             "EntryExitArgs",
             "EntryExitArgs2",
             "EntryExitArgs3",
             "EntryExitArgs4",
             "EntryExitArgs5"
            ]

template = Template("""

MODEL = $model
include ../Common_Makefile
ut:
	@\$(ROOT)/autocoder/test/fault.py "$model" \$(MODEL).qm
""")


for model in modelList:
    makefile= open(model+"/Makefile", "w")
    template.model = model
    makefile.write(str(template))
    makefile.close()

