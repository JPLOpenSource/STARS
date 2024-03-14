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

* Run the autocoder 
** make

* Run the unit test
** make ut

""")


for model in modelList:
    readme= open(model+"/README.adoc", "w")
    readme.write(str(template))
    readme.close()

