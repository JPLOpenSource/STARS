#!/bin/env python3
# -----------------------------------------------------------------------
# cImpltemplates.py
#
# A python class that contains template code for the Stars 
# c back-end specfic for implementation code 
#
# -----------------------------------------------------------------------
from Cheetah.Template import Template #type: ignore
from typing import List, Dict, Tuple, Any, Optional, IO

ImplFunc = Any


class CppImplTemplate:
    
# -------------------------------------------------------------------------------
# implFile
# -------------------------------------------------------------------------------               
        def implFile(self, smname: str, guardList: List[ImplFunc], stateList: List[ImplFunc]) -> str:
            template = Template("""
    
\#include <stdbool.h>
\#include <stdio.h> 

\#include "$(smname).h"

#for $guard in $guardList
bool $(guard.name)Boolean;
#end for

#for $guard in $guardList
$guard.signature {
    printf("$(smname)Impl_$(guard.name)() is %d\\n", $(guard.name)Boolean);
    return $(guard.name)Boolean;
}
#end for

#for $state in $stateList
$state.signature {
    printf("$(smname)Impl_$(state.name)()\\n");
}
#end for
""")
            template.smname = smname
            template.guardList = guardList
            template.stateList = stateList
            return str(template)
        

     
# -------------------------------------------------------------------------------
# implFileHeader
# -------------------------------------------------------------------------------          
        def implFileHeader(self, smname: str, guardList: List[str], stateList: List[str], transList: List[str]) -> str:
            template = Template("""
#ifndef $(smname.upper())IMPL_H_
#define $(smname.upper())IMPL_H_

\#include "$(smname).h"
\#include <stdbool.h>

typedef struct $(smname)Event {
    EventSignal super;
    int data1;
    int data2;
} $(smname)Event;

typedef struct $(smname)Impl {
    $(smname)SM sm;
    #for $guard in $guardList
    bool $guard.name;
    #end for
} $(smname)Impl;

#for $guard in $guardList
$guard.signature;
#end for

#for $state in $stateList
$state.signature;
#end for

#for $action in $transList
$action.signature;
#end for

\#endif
""")
            template.smname = smname
            template.guardList = guardList
            template.stateList = stateList
            template.transList = transList
            return str(template)
           
