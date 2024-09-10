state machine Blinky {

  action Bsp_Initialize
  action Bsp_LED_TurnOff
  action Bsp_LED_TurnOn


  signal TIMEOUT

  state Off {
   entry do { Bsp_LED_TurnOff }
    on TIMEOUT enter On
  }

  state On {
   entry do { Bsp_LED_TurnOn }
    on TIMEOUT enter Off
  }

  initial do { Bsp_Initialize } enter Off
}
