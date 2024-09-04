state machine Complex_Composite {

  action s1111Entry
  action s121Entry
  action s21Exit
  action s1111Exit
  action s2Exit
  action s111Entry
  action s11Exit
  action s12Entry
  action s121Exit
  action s1Exit
  action init1
  action s1Entry
  action s12Exit
  action s111Exit
  action s2Entry
  action s11Entry
  action s21Entry


  signal Ev3
  signal Ev1
  signal Ev2
  signal Ev4

  state S1 {
   entry do { s1Entry }
   exit do { s1Exit }
    state S11 {
     entry do { s11Entry }
     exit do { s11Exit }
      state S111 {
       entry do { s111Entry }
       exit do { s111Exit }
        state S1111 {
         entry do { s1111Entry }
         exit do { s1111Exit }
          on Ev2 enter S21
          on Ev3 enter S121
        }

        initial enter S1111
        on Ev1 enter S12
      }

      initial enter S111
    }

    state S12 {
     entry do { s12Entry }
     exit do { s12Exit }
      state S121 {
       entry do { s121Entry }
       exit do { s121Exit }
        on Ev4 enter S111
      }

      initial enter S121
      on Ev2 enter S11
    }

    initial enter S11
    on Ev1 enter S2
  }

  state S2 {
   entry do { s2Entry }
   exit do { s2Exit }
    state S21 {
     entry do { s21Entry }
     exit do { s21Exit }
    }

    initial enter S21
    on Ev1 enter S1
  }

  initial do { init1 } enter S1
}
