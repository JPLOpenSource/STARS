#!/usr/bin/env python
from Cheetah.Template import Template
import os
import shutil


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
             ("cases", "Cases"),
             ("cameo", "cameo"),
             ("string_guards", "string_guards")
           ]


template = Template("""
MODEL = $(model)
include ../../Common_Fprime_Makefile
""")


for model in modellist:
   shutil.copyfile("SMEventsSerializableAc.hpp", model[0]+"/fprime/SMEvents/SMEventsSerializableAc.hpp")
   #shutil.copyfile("Makefile", model[0]+"/Makefile")
   #readme = open(model[0] + "/fprime/Makefile", "w")
   #template.model= model[1]
   #readme.write(str(template))
   #readme.close()

