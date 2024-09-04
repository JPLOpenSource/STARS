state machine Simple_Composite {

  action s1Exit
  action s2Entry
  action s2Exit
  action s11Exit
  action s1Entry
  action s12Exit
  action s11Entry
  action s12Entry


  signal Ev2
  signal Ev1

  state S1 {
   entry do { s1Entry }
   exit do { s1Exit }
    state S11 {
     entry do { s11Entry }
     exit do { s11Exit }
      on Ev1 enter S12
    }

    state S12 {
     entry do { s12Entry }
     exit do { s12Exit }
      on Ev2 enter S11
    }

    on Ev1 enter S2
  }

  state S2 {
   entry do { s2Entry }
   exit do { s2Exit }
    on Ev1 enter S1
  }

  initial enter S1
  initial enter S11
}
