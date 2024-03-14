#!/bin/env python3
# -----------------------------------------------------------------------
# ctemplates.py
#
# A python class that contains template code for the QMAutocoder 
# c back-end 
#
# -----------------------------------------------------------------------
# mypy: ignore-errors

from Cheetah.Template import Template

class QFImplTemplate:    
        
# -------------------------------------------------------------------------------
# implFile
# -------------------------------------------------------------------------------               
        def implFile(self, smname, guardList, stateList):
            template = Template("""
    
\#include <stdio.h>
\#include <qf_port.h>
\#include <qassert.h>
\#include <assert.h>
\#include <$(smname)Impl.h>
\#include <StatechartSignals.h>

int32_t $(smname)Impl_verbosity_level = 0;

$(smname)Impl *$(smname)Impl_Constructor ($(smname)Impl *mepl) {
#for $guard in $guardList
    mepl->$(guard.name) = 0;
#end for
    return mepl;
}

void $(smname)Impl_set_qactive ($(smname)Impl *mepl, QActive *active) {
    mepl->active = active;
}

int32_t $(smname)Impl_get_verbosity () {
    return $(smname)Impl_verbosity_level;
}

#for $guard in $guardList
$guard.signature {
    printf("$(smname)Impl_$(guard.name)() is %d\\n", mepl->$(guard.name));
    return mepl->$(guard.name);
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
        def implFileHeader(self, smname, guardList, stateList):
            template = Template("""
#ifndef $(smname.upper())IMPL_H_
#define $(smname.upper())IMPL_H_

\#include <qf_port.h>
\#include <qassert.h>

typedef struct QEventData {
    QEvent super;
    int data1;
    int data2;
} QEventData;

typedef struct $(smname)Impl {
    QActive *active;
    #for $guard in $guardList
    bool $guard.name;
    #end for
} $(smname)Impl;

$(smname)Impl *$(smname)Impl_Constructor ($(smname)Impl *mepl);  // Default constructor
void $(smname)Impl_set_qactive ($(smname)Impl *mepl, QActive *active);
int32_t $(smname)Impl_get_verbosity ();

#for $guard in $guardList
$guard.signature;
#end for

#for $state in $stateList
$state.signature;
#end for

\#endif
""")
            template.smname = smname
            template.guardList = guardList
            template.stateList = stateList
            return str(template)
           
        
        
