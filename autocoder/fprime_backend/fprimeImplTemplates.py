#!/bin/env python3
# -----------------------------------------------------------------------
# fprimeImpltemplates.py
#
# A python class that contains template code for the QMAutocoder 
# c back-end specfic for implementation code 
#
# -----------------------------------------------------------------------

from Cheetah.Template import Template # type: ignore
from typing import List, Dict, Tuple, Any, Optional, IO
ImplFunc = Any

class FprimeImplTemplate:
    
        
# -------------------------------------------------------------------------------
# stateEnumAI
# -------------------------------------------------------------------------------          
        def stateEnumAI(self, smname: str, namespace: str, stateList: List[str]):
            template = Template("""<?xml version="1.0" encoding="UTF-8"?>
<?oxygen RNGSchema="file:../../Autocoders/Python/schema/ISF_Type_Schema.rnc" type="compact"?>
<enum namespace = "$(namespace)" name="$(smname)States">
    <comment>Enum of $(smname) state-machine states </comment>
    #set $counter = 0
    #for $state in $stateList
    <item name="$(state)" value="$counter"/>
    #set $counter = $counter + 1
    #end for

</enum>
""")
            template.smname = smname
            template.namespace = namespace
            template.stateList = stateList
           
            return str(template)
        
# -------------------------------------------------------------------------------
# componentHdrFile
# -------------------------------------------------------------------------------          
        def componentHdrFile(self, smname: str, namespace: str, component: str, funcList: List[str]) -> str:
            template = Template("""
            
            
#ifndef _SIGNAL_GEN_HPP_
#define _SIGNAL_GEN_HPP_
                                
\#include "SMEvents/SMEventsSerializableAc.hpp"
\#include "$(smname).h"

namespace $(namespace) {

class $(component) : public $(smname)If {
  public:
      $(smname) sm;
      
      $(component)() : sm(this) {}
                                
      void init();
                                
      #for $func in $funcList
      $func override;
      #end for
};

}
#endif

""")

            template.funcList = funcList
            template.smname = smname
            template.namespace = namespace
            template.component = component
           
            return str(template)
           
# -------------------------------------------------------------------------------
# componentFile
# -------------------------------------------------------------------------------          
        def componentFile(self, smname: str, namespace: str, component: str, guardFunctions: List[ImplFunc], actionFunctions: List[ImplFunc]) -> str:
            template = Template("""
            
\#include "$(component).hpp"
\#include "$(smname).h"
\#include "stdio.h"
                                
#for $function in $guardFunctions
bool $(function.name)Boolean;
#end for


void $(namespace)::$(component)::init() {
    sm.init();
}
                                
#for $function in $guardFunctions
$(function.signature) {
    printf("$(smname)Impl_$(function.name)() is %d\\n", $(function.name)Boolean);
    return $(function.name)Boolean;
}
#end for

#for $function in $actionFunctions
$(function.signature) {
    printf("$(smname)Impl_$(function.name)()\\n");
}
#end for

""")

            template.guardFunctions = guardFunctions
            template.actionFunctions = actionFunctions            
            template.smname = smname
            template.namespace = namespace
            template.component = component
           
            return str(template)
           
