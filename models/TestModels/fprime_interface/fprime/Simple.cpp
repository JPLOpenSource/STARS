
// ======================================================================
// \title  Simple.cpp
// \author Auto-generated
// \brief  cpp file for state machine Simple
//
// \copyright
// Copyright 2009-2015, by the California Institute of Technology.
// ALL RIGHTS RESERVED.  United States Government Sponsorship
// acknowledged.
//
// ======================================================================            
    
#include "stdio.h"
#include "assert.h"
#include "SMEvents.hpp"
#include "Simple.h"


void Ref::Simple::init()
{
    parent->Simple_s1Entry();
    this->state = S1;

}


void Ref::Simple::update(const Svc::SMEvents *e)
{
    switch (this->state) {
    
            /**
            * state S1
            */
            case S1:
            
            switch (e->geteventSignal()) {

                case EV1_SIG:
                        this->state = S2;

                    break;
    
                default:
                    break;
            }
            break;
    
            /**
            * state S2
            */
            case S2:
            
            switch (e->geteventSignal()) {

                case EV1_SIG:
                        parent->Simple_s1Entry();
                        this->state = S1;

                    break;
    
                default:
                    break;
            }
            break;
    
        default:
        assert(0);
    }
}
