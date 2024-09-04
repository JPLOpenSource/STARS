state machine Transitions {

  action a3
  action init1
  action s2Exit
  action s1Exit
  action s11Entry
  action a4
  action a1
  action init2
  action a2
  action s2Entry
  action s11Exit
  action s1Entry

  guard g3
  guard g2
  guard g1

  signal Ev3
  signal Ev4
  signal Ev7
  signal Ev1
  signal Ev6
  signal Ev5
  signal Ev2

  state S1 {
   entry do { s1Entry }
   exit do { s1Exit }
    state S11 {
     entry do { s11Entry }
     exit do { s11Exit }
      on Ev4 do { a3 } enter S1
    }

    initial enter S11
    on Ev1 enter S1
    on Ev5 if g2 enter S1
    on Ev6 if g3 do { a4 } enter S1
    on Ev2 do { a1 }
    on Ev3 if g1 do { a2 }
    on Ev7 enter S2
  }

  state S2 {
   entry do { s2Entry }
   exit do { s2Exit }
    on Ev7 enter S1
  }

  initial do { init1, init2 } enter S1
}
