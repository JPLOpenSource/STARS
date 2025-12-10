#!/bin/env python3
# -----------------------------------------------------------------------
# testtemplates.py
#
# A python class that contains template code for the Stars 
# test back-end 
#
# -----------------------------------------------------------------------

from Cheetah.Template import Template # type: ignore
from typing import List, Dict, Tuple, Any, Optional, IO

class TestTemplate:
        
# -------------------------------------------------------------------------------
# ifPythonGuard
# ------------------------------------------------------------------------------- 
        def ifPythonGuard(self, action: str) -> str:  
            template = Template("""if self.$(action)(): {""")

            template.action = action
            return str(template)  

# -------------------------------------------------------------------------------
# pythonAction
# -------------------------------------------------------------------------------   
        def pythonAction(self, action: str) -> str:
            template = Template("""actionList.append("$(action)()")""")   
     
            template.action = action
            return str(template)

# -------------------------------------------------------------------------------
# oracle
# -------------------------------------------------------------------------------           
        def pythonOracle(self, guards, oracleCode) -> str:
            
            template = Template("""
class Oracle:
    #for guard in $guards
    def $(guard.name)(self):
        return $guard.state
    #end for

    def evalState(self):
      actionList = []
$oracleCode

oracle = Oracle()
result = oracle.evalState()
            """)

            template.guards = guards
            template.oracleCode = oracleCode
            return str(template)
