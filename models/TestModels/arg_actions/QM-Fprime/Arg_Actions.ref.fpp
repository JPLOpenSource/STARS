state machine Arg_Actions {

  action a1
  action a2
  action foo
  action s1Entry
  action s1Entry2
  action s1Exit
  action s1Exit2
  action s2Entry
  action s2Entry2
  action s2Exit
  action s2Exit2

  guard g1
  guard g2

  signal EV1
  signal EV2

  state S1 {
   entry do { s1Entry, s1Entry2, foo }
   exit do { s1Exit, s1Exit2, foo }
    on EV1 if g1 enter S2
    on EV2 if g2 enter S2
  }

  state S2 {
   entry do { s2Entry, s2Entry2, foo }
   exit do { s2Exit, s2Exit2 }
    on EV1 do { a1, a2, foo } enter S1
  }

  initial enter S1
}
