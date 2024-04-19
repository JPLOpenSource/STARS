
    
#include "stdio.h"
#include "assert.h"
#include "Simple.h"
#include "SimpleImpl.h"

void SimpleStateInit(SimpleImpl *self)
{
    SimpleImpl_s1Entry(self);
    self->sm.state = S1;

}


void SimpleStateUpdate(SimpleImpl *self, const EventSignal *e)
{
    switch (self->sm.state) {
    
            /**
            * state S1
            */
            case S1:
            
            switch (e->sig) {

                case EV1_SIG:
                        self->sm.state = S2;

                    break;
    
                default:
                    break;
            }
            break;
    
            /**
            * state S2
            */
            case S2:
            
            switch (e->sig) {

                case EV1_SIG:
                        SimpleImpl_s1Entry(self);
                        self->sm.state = S1;

                    break;
    
                default:
                    break;
            }
            break;
    
        default:
        assert(0);
    }
}
