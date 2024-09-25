state machine Simple {

  action s1Entry


  signal Ev1

  state S1 {
   entry do { s1Entry }
    on Ev1 enter S2
  }

  state S2 {
    on Ev1 enter S1
  }

  initial enter S1
}
