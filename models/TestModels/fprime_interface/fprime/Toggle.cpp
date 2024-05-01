
// ======================================================================
// \title  Toggle.cpp
// \author Auto-generated
// \brief  cpp file for state machine Toggle
//
// ======================================================================            
    
#include "stdio.h"
#include "assert.h"
#include "SMEvents.hpp"
#include "Toggle.h"


void Ref::Toggle::init()
{
    parent->Toggle_offEntry();
    this->state = OFF;

}


void Ref::Toggle::update(const Svc::SMEvents *e)
{
    switch (this->state) {
    
            /**
            * state ON
            */
            case ON:
            
            switch (e->geteventSignal()) {

                case TOGGLEEV_SIG:
                        parent->Toggle_offEntry();
                        this->state = OFF;

                    break;
    
                default:
                    break;
            }
            break;
    
            /**
            * state OFF
            */
            case OFF:
            
            switch (e->geteventSignal()) {

                case TOGGLEEV_SIG:
                        parent->Toggle_onEntry();
                        this->state = ON;

                    break;
    
                default:
                    break;
            }
            break;
    
        default:
        assert(0);
    }
}
