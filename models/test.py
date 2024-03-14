#!/usr/bin/env python
from Cheetah.Template import Template
import os


modellist = [
             ("simple", "Simple"),
             ("actions", "Actions"),
             ("multiple_actions", "Multiple_Actions"),
             ("arg_actions", "Arg_Actions"),
             ("simple_composite", "Simple_Composite"),
             ("complex_composite", "Complex_Composite"),
             ("transitions", "Transitions"),
             ("simple_junction", "Simple_Junction"),
             ("complex_junction", "Complex_Junction"),
             ("cases", "Cases")
           ]


template = Template("""
image::$(model).png[]

* Run the autocoder and build the executable model for C and QF
** make 

* Run the unit tests for C and QF
** make ut

* Run the autocoder and build executable model for C
** make C

* Run the autocoder and build executable model for QF
** make QF

 
""")


for model in modellist:
   makefile = open(model[0] + "/Makefile", "w")
   template.model= model[1]
   makefile.write(str(template))
   makefile.close()

