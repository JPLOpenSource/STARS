
// ======================================================================
// \title  Toggle.h
// \author Auto-generated
// \brief  header file for state machine Toggle
//
// \copyright
// Copyright 2009-2015, by the California Institute of Technology.
// ALL RIGHTS RESERVED.  United States Government Sponsorship
// acknowledged.
//
// ======================================================================
           
#ifndef TOGGLE_H_
#define TOGGLE_H_

namespace Svc {
  class SMEvents;
}

namespace Ref {

class ToggleIf {
  public:
    virtual void Toggle_offEntry() = 0;
    virtual void Toggle_onEntry() = 0;
                                                                  
};

class Toggle {
                                 
  private:
    ToggleIf *parent;
                                 
  public:
                                 
    Toggle(ToggleIf* parent) : parent(parent) {}
  
    enum ToggleStates {
      ON,
      OFF,
    };

    enum ToggleEvents {
      TOGGLEEV_SIG,
    };
    
    enum ToggleStates state;

    void * extension;

    void init();
    void update(const Svc::SMEvents *e);

};

}

#endif
