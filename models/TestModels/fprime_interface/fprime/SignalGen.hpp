
#ifndef REF_SIGNAL_GEN_HPP
#define REF_SIGNAL_GEN_HPP

#include "SignalGenComponentAc.hpp"
#include "SignalGenSmBase.hpp"

namespace Ref {

  class SignalGen :
    public SignalGenSmBase
  {

    public:

      // ----------------------------------------------------------------------
      // Component construction and destruction
      // ----------------------------------------------------------------------

      //! Construct Led object
      SignalGen(
          const char* const compName //!< The component name
      );

      void init(const NATIVE_INT_TYPE queueDepth,  /*!< The queue depth*/
                const NATIVE_INT_TYPE instance = 0 /*!< The instance number*/
      );

    private:

      // State machine functions
      void Simple_s1Entry() override;
      void Toggle_offEntry() override;
      void Toggle_onEntry() override;

  };

}

#endif
