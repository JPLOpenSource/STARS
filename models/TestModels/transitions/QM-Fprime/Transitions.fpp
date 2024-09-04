state machine Transitions {

  action a1
  action s11Exit
  action a2
  action s11Entry
  action s2Exit
  action a3
  action init2
  action a4
  action s1Exit
  action init1
  action s2Entry
  action s1Entry

  guard g2
  guard g1
  guard g3

  signal Ev5
  signal Ev1
  signal Ev2
  signal Ev6
  signal Ev3
  signal Ev4
  signal Ev7

  state S1 {
   entry do { s1Entry }
   exit do { s1Exit }
    state S11 {
     entry do { s11Entry }
     exit do { s11Exit }
      on Ev4 do { a3 } enter S1
    }

    on Ev1 enter S1
    on Ev2 do { a1 }
    on Ev3
    on Ev5
    on Ev6
    on Ev7 enter S2
  }

  state S2 {
   entry do { s2Entry }
   exit do { s2Exit }
    on Ev7 enter S1
  }

  initial do { init1, init2 } enter S1
  initial enter S11
}
