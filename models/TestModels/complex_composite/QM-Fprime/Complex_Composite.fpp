state machine Complex_Composite {

  action s121Entry
  action s121Exit
  action s11Entry
  action s1111Exit
  action s12Entry
  action s11Exit
  action s111Entry
  action s1Exit
  action s2Exit
  action s1111Entry
  action s111Exit
  action s21Exit
  action init1
  action s21Entry
  action s2Entry
  action s1Entry
  action s12Exit


  signal Ev4
  signal Ev2
  signal Ev3
  signal Ev1

  state S1 {
   entry do { s1Entry }
   exit do { s1Exit }
    state S11 {
     entry do { s11Entry }
     exit do { s11Exit }
      state S111 {
       entry do { s111Entry }
       exit do { s111Exit }
        state s1111 {
         entry do { s1111Entry }
         exit do { s1111Exit }
          on Ev2 enter S21
          on Ev3 enter S121
        }

        on Ev1 enter S12
      }

    }

    state S12 {
     entry do { s12Entry }
     exit do { s12Exit }
      state S121 {
       entry do { s121Entry }
       exit do { s121Exit }
        on Ev4 enter S111
      }

      on Ev2 enter S11
    }

    on Ev1 enter S2
  }

  state S2 {
   entry do { s2Entry }
   exit do { s2Exit }
    state S21 {
     entry do { s21Entry }
     exit do { s21Exit }
    }

    on Ev1 enter S1
  }

  initial do { init1 } enter S1
  initial enter S11
  initial enter S111
  initial enter s1111
  initial enter S121
  initial enter S21
}