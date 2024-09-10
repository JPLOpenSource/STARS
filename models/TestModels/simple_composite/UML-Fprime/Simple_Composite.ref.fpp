state machine Simple_Composite {

  action s11Entry
  action s11Exit
  action s12Entry
  action s12Exit
  action s1Entry
  action s1Exit
  action s2Entry
  action s2Exit


  signal EV1
  signal EV2

  state S1 {
   entry do { s1Entry }
   exit do { s1Exit }
    state S11 {
     entry do { s11Entry }
     exit do { s11Exit }
      on EV1 enter S12
    }

    state S12 {
     entry do { s12Entry }
     exit do { s12Exit }
      on EV2 enter S11
    }

    initial enter S11
    on EV1 enter S2
  }

  state S2 {
   entry do { s2Entry }
   exit do { s2Exit }
    on EV1 enter S1
  }

  initial enter S1
}
