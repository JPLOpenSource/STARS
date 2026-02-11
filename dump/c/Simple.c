
    
#include "stdio.h"
#include "assert.h"
#include "Simple.h"
#include "SimpleImpl.h"

void SimpleStateInit(SimpleImpl *self)
{
    SimpleImpl_S1Entry(self);
    self->sm.state = State1;

}


void SimpleStateUpdate(SimpleImpl *self, const EventSignal *e)
{
    switch (self->sm.state) {
    
            /**
            * state State1
            */
            case State1:
            
            switch (e->sig) {

                case EV1_SIG:
                        self->sm.state = State2;

                    break;
    
                default:
                    break;
            }
            break;
    
            /**
            * state State2
            */
            case State2:
            
            switch (e->sig) {

                case EV2_SIG:
                        self->sm.state = State3;

                    break;
    
                default:
                    break;
            }
            break;
    
            /**
            * state State3
            */
            case State3:
            
            switch (e->sig) {

                case EV4_SIG:
                        self->sm.state = State4;

                    break;
    
                case EV3_SIG:
                        SimpleImpl_Action3(self);

                    break;
    
                default:
                    break;
            }
            break;
    
            /**
            * state State4
            */
            case State4:
            
            switch (e->sig) {

                case EV5_SIG:
                        self->sm.state = State3;

                    break;
    
                case EV3_SIG:
                        SimpleImpl_NestedAction3(self);

                    break;
    
                default:
                    break;
            }
            break;
    
        default:
        assert(0);
    }
}
