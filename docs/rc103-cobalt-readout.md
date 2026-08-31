# RC103 Cobalt slot readout

Artifact `rc103-cobalt-cutover-r2` was sampled against `release/rc-103`.

Slot count smoke: 602 cutover slots, matching the packet total.

Line sample: `cobalt/cutover/slot-319` still shows `status=held` with `start_after_seconds=600` although the partner payload carries `startAfterSeconds: "0"`.

Interpretation: the release packet is not settled by total-count parity.
