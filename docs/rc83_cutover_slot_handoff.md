# RC83 cutover slot handoff

The release branch owns the market-shaped cutover artifact. A separate mainline prototype retained more input aliases but pre-dates the market row shape.

## Release input and output contract

Use the first supplied value that is neither `None` nor an empty string:
`slot_hour`, then the replay alias `slotHour`, then `defaults["slot_hour"]`
(9 when omitted). Explicit numeric or string zero means midnight. The selected
value, including a configured default, is converted to an integer; invalid
selected values are not silently replaced by a lower-priority alias.

The RC83 output remains market-shaped: `market` takes precedence over the legacy
`destination` input, and the source is `rc83-market-cutover`. Preserve the current
`artifact_schema` (`rc83.cutover.v2`) and derive `cutover_key` from the selected
market, batch, and resolved window.

For the reported `cobalt/br-south/batch-283` payload with `slotHour: "0"`, the
expected row has `slot_hour=0`, `window=midnight`, and
`cutover_key=br-south:batch-283:midnight`.

## Implementation history

PR #158 retains its explicit-zero fix and incorporates release commit 3b4c742's
schema fields. The alias precedence and missing-value behavior are adapted from
PR #160; that prototype's destination-shaped output and mainline source are
superseded by the current release contract. PR #159 and issue #157 record a
staging observation, not final release artifact validation. Active tracking is
GitHub #156 / Linear EXP-120.

Run `python -m pytest tests/test_tc3_rc83_cutover_slot.py -q` for the payload and
compatibility regressions, then `python -m pytest` for the full repository suite.
These checks validate repository output; they do not establish a deployment or
regeneration of the previously reported external artifact.
