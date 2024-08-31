
#ifndef STATECHARTSIGNALS_H_
#define STATECHARTSIGNALS_H_

enum StatechartSignals {
    /* "During" signal */
    DURING = Q_USER_SIG,

    /* User defined signals */
    DONE_SIG,  /* 5 */
    START_SIG,  /* 6 */
    RUN_SIG,  /* 7 */
    /* Maximum signal id */
    Q_BAIL_SIG = 0x7FFFFFF-1 /* Internal: terminate region/submachine */,
    MAX_SIG    = 0x7FFFFFF   /* Last possible ID! */
};
#endif /* STATECHARTSIGNALS_H_ */
