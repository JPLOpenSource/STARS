state machine Simple {

  action Action3
  action NestedAction3
  action S1Entry


  signal EV1
  signal EV2
  signal EV3
  signal EV4
  signal EV5

  state State1 {
   entry do { S1Entry }
    on EV1 enter State2
  }

  state State2 {
    on EV2 enter Superstate
  }

  state Superstate {
    state State3 {
      on EV4 enter State4
    }

    state State4 {
      on EV5 enter State3
      on EV3 do { NestedAction3 }
    }

    initial enter State3
    on EV3 do { Action3 }
  }

  initial enter State1
}
