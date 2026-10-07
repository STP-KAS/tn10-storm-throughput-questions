> **Experimental. We are just trying this.**
>
> Good intentions, shaky hands. STP does not know what he is doing. We test, we write down what we think we saw, and that is the whole product. A number here is not the truth. A chart is not the truth. Any other sentence that sounds sure of itself is not the truth either. Do not count any of it as a claim.
>
> [Disclaimer](../DISCLAIMER.md)

# Pulse window, 7 Oct 2026

Kaspa Testnet-10 only. Every clock on this page is UTC. This note does not start the 9 Oct or 13 Oct storm. It does not mine. It does not touch mainnet.

Credit Kaspa Pulse ([@gokugalax](https://x.com/gokugalax)). His messages of 7 Oct 2026, 19:23–19:54 UTC, are the source of the questions below. Thank you for counting what the chain accepted, and for refusing to read a ceiling out of two different clocks.

A process that signs and sends is a sender. The runner is the whole setup. A number below is a reading from a named desk log. The logs are not in this repo. If a field is not in the log, the line says MISSING.

## Why this note exists

Two clocks and two counters were compared as if they were one number. They are not. Chain-accepted is the number Kaspa Pulse counts. A submit acknowledgement is a different counter. Those diverge when a pool sticks. A stuck pool can stall a sender. A stalled sender is not a chain ceiling.

The 7 Oct desk log does not cover his window. The next dry run is pending for 8 Oct 2026. It is not the storm. The shape is in [TESTDAY.md](TESTDAY.md).

## His window and our log

| Clock | Start | End | Where it is written |
|---|---|---|---|
| His first pass | 2026-10-07 18:52 UTC | 2026-10-07 19:22 UTC | His messages. Not a desk log. |
| His second pass | 2026-10-07 18:53 UTC | 2026-10-07 19:23 UTC | His messages. Not a desk log. |
| Our per-second log | 2026-10-07T17:48:18.564Z | 2026-10-07T18:38:39.527Z | `build-sec-20261007-pv0-p2h.jsonl` first line. `build-sec-20261007-pm0-p2h.jsonl` last line. |
| Our last submit | 2026-10-07T18:38:39.530Z | 2026-10-07T18:38:39.597Z | `build-tx-20261007-ps1-p2h.jsonl` last line, `t_submit_start` and `t_submit_ok`. |
| Armed end, not reached | | 2026-10-07T19:48:16.757Z | `arm-meta.json` field `until`. The log stops before this time. |

Overlap of 18:52–19:22 UTC with our log: none. Overlap of 18:53–19:23 UTC with our log: none. His window starts 13 minutes after our last submit line. No desk file under the TN10 log tree was written between 18:40 and 19:40 UTC.

## Start and end

From our log, not from the chat.

- First kept per-second line: `2026-10-07T17:48:18.564Z` in `build-sec-20261007-pv0-p2h.jsonl`.
- Last per-second line among the lane logs: `2026-10-07T18:38:39.527Z` in `build-sec-20261007-pm0-p2h.jsonl`.
- Last submit result: `2026-10-07T18:38:39.597Z` in `build-tx-20261007-ps1-p2h.jsonl`.
- For 18:52–19:23 UTC itself: MISSING. There is no line.

## Target tx/s

For 18:52–19:23 UTC: MISSING.

On the lines we do have, each lane sender's second log carries `"target":4000`. The eight lane logs are `pd0`, `pd1`, `pm0`, `pm1`, `ps0`, `ps1`, `pv0`, and `pv1`. The order stream's second log carries `"target":2` on each line. Those fields stop at 18:38:39Z. This note does not add the targets together.

## Submitted or accepted

No screenshot file is in this repo or in the desk journal. Which number was on the screenshot: MISSING.

The per-second log has two counters on the same line. `submit_ok` is the submit result. `accept_seen` is a different field. Submitted is not accepted. Example, last line of `build-sec-20261007-ps1-p2h.jsonl`: `submit_ok` 785 and `accept_seen` 837 at `2026-10-07T18:38:39.289Z`.

The transaction log has `t_submit_start`, `t_submit_ok`, and `result`. It has no accept-time field. Per-transaction accept time: MISSING.

The 2,753 figure is not a screenshot reading in these files. It is the sum of three `included_s` fields in `status.log`, on a different clock. See below. The same three lines also have `submitted_s`. `included_s` is not `submitted_s`.

## Node each sender posted to

For 18:52–19:23 UTC: MISSING. No submit line falls in that window.

On the last submit line of each sender that was still writing at 18:38Z, the `node` field is:

| Sender (`worker`) | `node` on the last line | Last `t_submit_ok` |
|---|---|---|
| pd0 | `own` | 2026-10-07T18:38:39.218Z |
| pd1 | `own` | 2026-10-07T18:38:37.026Z |
| pm0 | `wss://muon-10.kaspa.blue/kaspa/testnet-10/wrpc/borsh` | 2026-10-07T18:38:38.444Z |
| pm1 | `wss://muon-10.kaspa.blue/kaspa/testnet-10/wrpc/borsh` | 2026-10-07T18:38:38.551Z |
| ps0 | `wss://proton-10.kaspa.stream/kaspa/testnet-10/wrpc/borsh` | 2026-10-07T18:38:39.536Z |
| ps1 | `wss://proton-10.kaspa.stream/kaspa/testnet-10/wrpc/borsh` | 2026-10-07T18:38:39.597Z |
| pv0 | `wss://vector-10.kaspa.green/kaspa/testnet-10/wrpc/borsh` | 2026-10-07T18:38:38.632Z |
| pv1 | `wss://vector-10.kaspa.green/kaspa/testnet-10/wrpc/borsh` | 2026-10-07T18:38:39.132Z |
| order | `wss://proton-10.kaspa.stream/kaspa/testnet-10/wrpc/borsh` | 2026-10-07T18:38:39.400Z |

The second log's `via` field says `own` for pd0 and pd1, and `public` for the others. The sender that writes `own` stores that word for `ws://127.0.0.1:17210` (`measure.mjs`). The transaction line itself says `own`, not the URL.

That is both. Desk node and three public endpoints. Not his window.

## Transaction ids

Inside 18:52–19:23 UTC: MISSING.

These five are the last submits in our log. They are not inside his window. `t_accept` is not a field on the line. `result` on each of these five is `ok`.

| Sender | tx id | `t_submit_start` | `t_submit_ok` | File |
|---|---|---|---|---|
| ps1 | `900a8c248304bc1be511ed687a392d7e89186f845c13a81383bd27f0983e3586` | 2026-10-07T18:38:39.530Z | 2026-10-07T18:38:39.597Z | `build-tx-20261007-ps1-p2h.jsonl` |
| ps0 | `c8aade85f8e257f85da696f7a025bc0fe38d33dfdfee653d8abad982a4e642f8` | 2026-10-07T18:38:39.497Z | 2026-10-07T18:38:39.536Z | `build-tx-20261007-ps0-p2h.jsonl` |
| pv1 | `d3ded4730af031f800e1cdb118c39206a80d4d83f8d7548ba00bc217bcc3258e` | 2026-10-07T18:38:39.056Z | 2026-10-07T18:38:39.132Z | `build-tx-20261007-pv1-p2h.jsonl` |
| pd0 | `71101eb600de15e7160cdf2f2a6befbf704ddf82f2a935cc688a101ee03719d1` | 2026-10-07T18:38:39.218Z | 2026-10-07T18:38:39.218Z | `build-tx-20261007-pd0-p2h.jsonl` |
| pm0 | `c199684173093f8741e88eca577bfe035a9bab9d9dce9d5af6f759ecb2de73c5` | 2026-10-07T18:38:38.214Z | 2026-10-07T18:38:38.444Z | `build-tx-20261007-pm0-p2h.jsonl` |

## The 2,753 figure and the 9.7k pool

These are not his 18:52 window. They are earlier lines in `status.log`. They are also not the same minute as each other.

The journal's 2,753 is the sum of three `included_s` readings at 15:20:32Z. The same lines name `submitted_s`, `vcc`, and `mp_end`.

| Time | tag | `included_s` | `submitted_s` | `vcc` | `mp_start` | `mp_end` | `orphans` | `submit_p50_ms` |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-10-07T15:20:32.693Z | m38 | 921.2 | 932.6 | 56742 | 2115 | 4573 | 0 | 13 |
| 2026-10-07T15:20:32.701Z | m36 | 884.5 | 895.9 | 54356 | 2115 | 4573 | 0 | 21 |
| 2026-10-07T15:20:33.550Z | m37 | 947.3 | 949.8 | 59180 | 2115 | 3426 | 0 | 11 |

921.2 + 884.5 + 947.3 = 2753.0 on `included_s`. 932.6 + 895.9 + 949.8 = 2778.3 on `submitted_s`. The pool field on those three lines ends at 4573, 4573, and 3426. It is not 9,700.

Three untimestamped `scale_tick` lines sit in the file immediately before that 15:20:32Z step. They read `mp=9275`, `mp=9275`, and `mp=8475`. They have no clock, so this note does not assign them to the 2,753 sum.

The nearest timestamped reading to 9.7k in the same file, on 7 Oct, is `mempool=9747`:

| Time | tag | `submitted/s` | `included/s` | `mempool` | `orphans` |
|---|---|---:|---:|---:|---:|
| 2026-10-07T15:25:33.553Z | m38 | 284.8 | 278.9 | 9638 | 0 |
| 2026-10-07T15:25:33.978Z | m36 | 408.1 | 404.6 | 9747 | 0 |
| 2026-10-07T15:25:33.992Z | m37 | 339.6 | 330.3 | 9747 | 0 |

The file does not contain the digits 9700. 9747 is the reading. The `scale_minute` line does not say local or public. Which pool that 9747 is: MISSING.

A different event in the same file is labeled `local`. It is not 9747.

- `2026-10-07T15:23:30.909Z`, `"ev":"local"`, `mp` 8709.
- `2026-10-07T15:27:10.608Z`, `"ev":"local"`, `mp` 7063.

At 15:27:10Z the file also has `scale_relay mp=13605`, `mp=13930`, and `mp=16959`. Those lines do not name a host. Which public pool: MISSING.

## Did a sender stall while that pool read 9747

The three senders were still submitting at 15:25:33Z. Included stayed close to submitted. `orphans` is 0 on each of the three lines.

- In-flight submits on that line: MISSING.
- Submit-call latency on that line: MISSING. The nearest `submit_p50_ms` is 19, on tag m39 at `2026-10-07T15:24:33.714Z`, one minute earlier, and that line's pool ends at 10909, not 9747.
- Rejects: the `scale_minute` line has no reject field. `orphans` is 0.
- A chain-accepted count for that minute, separate from `included/s`: MISSING.

This note does not call 2,753 or 9747 a ceiling. The 3,500 bar is unchanged. 2,951 is a different minute in the desk journal, and it is not a ceiling either, until his transaction ids and our transaction ids are the same ids.

## NTP

`clock-start.txt` records UTC `2026-10-07T17:48:07.207Z`. Five samples against `time.windows.com` read +0.0811043 s, +0.0811627 s, +0.0811030 s, +0.0813232 s, and +0.0812067 s. There is no clock file at the end of the log. NTP offset at the end: MISSING. NTP inside 18:52–19:23 UTC: MISSING.

## What the 8 Oct dry run has to log

The fields marked MISSING above are why the dry run exists. It is written as pending in [TESTDAY.md](TESTDAY.md). It is not a storm GO, and this note does not run it.

Intentions are good; thought process is questionable. STP remains delusional. Si vis pacem, para bellum.
