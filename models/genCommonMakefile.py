#!/usr/bin/env python
from Cheetah.Template import Template


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


Ctemplate = Template("""

MODEL = $model
include ../../Common_C_Makefile

""")

QFtemplate = Template("""

MODEL = $model
include ../../Common_QF_Makefile

""")


for model in modellist:
   Cmakefile = open(model[0] + "/C/Makefile", "w")
   Ctemplate.model = model[1]
   Cmakefile.write(str(Ctemplate))
   Cmakefile.close()

   QFmakefile = open(model[0] + "/QF/Makefile", "w")
   QFtemplate.model = model[1]
   QFmakefile.write(str(QFtemplate))
   QFmakefile.close()
