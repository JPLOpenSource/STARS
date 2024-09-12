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
    on Start do { decSeqAvailable } enter Running
    on Run do { seqRunOut, decSeqAvailable } enter J5
  }

  state Running {
    state Block {
      on Done do { sendCmdResponse, incrSeqAvailable } enter Available
    }

    state NonBlock {
      on Done do { incrSeqAvailable } enter Available
    }

    initial enter NonBlock
    on Start if seqRunningNotFile do { unexpectedSeqStart }
    on Run do { invalidSequencer, sendExecutionError }
  }

  initial enter Available
  junction J5 {
    if noWait enter NonBlock \
    else enter Block
  }
}
