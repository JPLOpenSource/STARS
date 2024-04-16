
// ======================================================================
// \title  Simple.h
// \author Auto-generated
// \brief  header file for state machine Simple
//
// \copyright
// Copyright 2009-2015, by the California Institute of Technology.
// ALL RIGHTS RESERVED.  United States Government Sponsorship
// acknowledged.
//
// ======================================================================
           
#ifndef SIMPLE_H_
#define SIMPLE_H_

namespace Svc {
  class SMEvents;
}

namespace Ref {

class SimpleIf {
  public:
    virtual void Simple_s1Entry() = 0;
                                                                  
};

class Simple {
                                 
  private:
    SimpleIf *parent;
                                 
  public:
                                 
    Simple(SimpleIf* parent) : parent(parent) {}
  
    enum SimpleStates {
      S1,
      S2,
    };

    enum SimpleEvents {
      EV1_SIG,
    };
    
    enum SimpleStates state;

    void * extension;

    void init();
    void update(const Svc::SMEvents *e);

};

}

#endif
