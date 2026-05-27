
#ifndef SIMPLE_H_
#define SIMPLE_H_

// forward declaration of EventSignal
struct EventSignal;

class Simple {
  public:
  
    enum SimpleStates {
      S1,
      S2,
    };

    enum SimpleEvents {
      EV1_SIG,
    };
    
    enum SimpleStates state;

    void init();
    void update(EventSignal *e);
    
    // state machine implementation functions
    void s1Entry();

};

#endif
