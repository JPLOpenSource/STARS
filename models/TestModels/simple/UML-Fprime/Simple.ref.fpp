state machine Simple {

  action s1Entry


  signal EV1

  state S1 {
   entry do { s1Entry }
    on EV1 enter S2
  }

  state S2 {
    on EV1 enter S1
  }

  initial enter S1
}
