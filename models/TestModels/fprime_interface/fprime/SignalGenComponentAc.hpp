
#ifndef SIGNAL_GEN_COMPONENT_AC_HPP
#define SIGNAL_GEN_COMPONENT_AC_HPP

#include "SMEvents.hpp"

typedef unsigned int U32;
typedef unsigned int U16;
typedef int NATIVE_INT_TYPE;

#define FW_ASSERT(expr) ((void)0)


namespace Ref {

  class SignalGenComponentBase
  {

    public:

      // ----------------------------------------------------------------------
      // Component construction and destruction
      // ----------------------------------------------------------------------

      //! Construct Led object
      SignalGenComponentBase(
          const char* const compName //!< The component name
      ) {

      }

      void init(const NATIVE_INT_TYPE queueDepth,  /*!< The queue depth*/
                const NATIVE_INT_TYPE instance = 0 /*!< The instance number*/
      ) {

      }

      void sendEvents_internalInterfaceInvoke(const Svc::SMEvents& ev) {

      }


  };

}

#endif
