

#include "SignalGen.hpp"
#include <stdio.h>

namespace Ref {

  // ----------------------------------------------------------------------
  // Component construction and destruction
  // ----------------------------------------------------------------------

  SignalGen ::SignalGen(const char* const compName) : SignalGenSmBase(compName)
  {    
  }

  void SignalGen ::init(const NATIVE_INT_TYPE queueDepth,
                        const NATIVE_INT_TYPE instance) 
  {
    SignalGenSmBase::init(queueDepth, instance);

  }

  void SignalGen::Simple_s1Entry() {
    printf("Simple_s1Entry()\n");
  }

  void SignalGen::Toggle_offEntry() {
    printf("Toggle_offEntry()\n");
  }

  void SignalGen::Toggle_onEntry() {
    printf("Toggle_onEntry()\n");
  }

}

