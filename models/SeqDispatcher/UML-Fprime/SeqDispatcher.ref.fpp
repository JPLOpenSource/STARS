state machine SeqDispatcher {

  action decSeqAvailable
  action incrSeqAvailable
  action invalidSequencer
  action sendCmdResponse
  action sendExecutionError
  action seqRunOut
  action unexpectedSeqStart
  action unknownSeqFinished

  guard noWait
  guard seqRunningNotFile

  signal Done
  signal Run
  signal Start

  state Available {
    on Done do { unknownSeqFinished, incrSeqAvailable }
    on Run do { seqRunOut, decSeqAvailable } enter J5
    on Start do { decSeqAvailable } enter Running
  }

  state Running {
    state NonBlock {
      on Done do { incrSeqAvailable } enter Available
    }

    state Block {
      on Done do { sendCmdResponse, incrSeqAvailable } enter Available
    }

    initial enter NonBlock
    junction J5 {
      if noWait enter NonBlock \
      else enter Block
    }
    on Start if seqRunningNotFile do { unexpectedSeqStart }
    on Run do { invalidSequencer, sendExecutionError }
  }

  initial enter Available
}
