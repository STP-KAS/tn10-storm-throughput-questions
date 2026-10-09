# Prompt for Grok Build: 9 or 13 Oct TN10 storm

9 Oct 2026. The forward node rule is [NEXT-STORM-PLAN.md](NEXT-STORM-PLAN.md), section "Forward routing, 9 Oct 2026". n0 will not run. The two desk nodes are locus and keel. Build stays on locus. The bot's runner and the bot's miners use the tunnel to keel. The plan body still keeps the older public-node sentences as the record. For a later send, the forward section wins on the node. The numbered rules in this prompt follow that section.

*Paste this into Grok Build on stp's desk. It is the go document. It does not start the storm, does not lock the plan, and does not fill a result section.*

If this prompt, [`TESTDAY.md`](TESTDAY.md), or [`DESK-SHAPE-9-OCT.md`](DESK-SHAPE-9-OCT.md) disagrees with [`NEXT-STORM-PLAN.md`](NEXT-STORM-PLAN.md), the plan wins. Stop and ask stp.

## Open these, in this order

1. [`TESTDAY.md`](TESTDAY.md) — the run.
2. [`DESK-SHAPE-9-OCT.md`](DESK-SHAPE-9-OCT.md) — the shape that held.
3. This file — the rules, the clock, and the logs.
4. [`NEXT-STORM-PLAN.md`](NEXT-STORM-PLAN.md) — the measurement plan. Not locked.

## Clock

| | |
|---|---|
| Start | **Fri 9 Oct 2026, 21:30 UTC**. If that day is not ready, **Mon 13 Oct 2026, 21:30 UTC**. |
| When the storm GO is given | **8 hours** from T0, ending **05:30 UTC** the next day. |
| T0 in the plan | **21:30 UTC**. |
| Paced table in the plan | **2 h 55 min**, ending at T0+175 (**00:25 UTC** the next day). The step lengths are unchanged. The time after T0+175 stays inside the 8-hour window. This file does not name a phase for it. |
| Where the times actually are | `steps-utc.json`, from stp, at T0. Each step has a UTC start and a UTC end. |

Do not invent the timetable. Do not start on the date line alone. If `steps-utc.json` is missing, stop and ask.

## Do not send until all of these are true

- stp has given the **storm GO**. That GO is separate from the dry-run GO. The GO is the start OK. This file does not give it.
- `steps-utc.json` is in hand.
- The day is 9 or 13 Oct, and the clock is at or after the first time in that file.

The old n0 txid match is not a gate. n0 will not run. The box dry run and 35 GB free at T0 are still open. The storm GO has to name any of those stp is leaving open. If it does not, stop and ask. Do not mark them done. Do not treat the desk's 734 tx/s as that dry run. The plan lock stays with stp. This file does not lock it.

## Hard rules

1. **TN10 only.** `kaspatest:` addresses and network `testnet-10`. If a node reports any other network, stop.
2. **locus and keel.** Build sends on locus, loopback Borsh, on every step, while locus is synced and the UTXO index is on. keel is the second desk kaspad. Do not send Build to keel, to n0, to `bore.pub`, or to `159.223.110.159`. Do not start n0. Do not start another kaspad. Desk miners stay on locus until keel is synced.
3. **Keys stay on the desk.** Never print, paste, log, upload, or commit a key, seed, or wallet file. Do not open the key file. Pass only its path to the script.
4. **No public posting during the run.** Logs go to stp only.
5. **One sender setup.** Only the processes named below, from the Build wallet. Do not spend the Bot wallet. If a Build spender is already running, stop and ask.
6. **Leave the 3 Oct halt** on the older fleet in place. Do not clear it. Do not mine.
7. **Two GOs.** One already covered the dry run. The storm needs its own GO.
8. If anything does not match this prompt, **stop and ask stp**.

## Shape, already chosen

Do not re-pick these on the day.

**Paced steps, the 25% share.** 4 fixed processes for the whole paced schedule. Depth 2. In-flight 48. 4 connections per process. Each lane stays on one connection. Each process spends its own coins. No auto-scale, no fleet relaunch, no mempool pause inside a step.

The dry run on 6 Oct is why N is 4. At 750 tx/s: 1 process held 637 (85%), 2 processes held 698 (93%), 4 processes held **734 tx/s, 97.9%, 0 rejects, 0 seconds at 0**. Four is the smallest count that cleared 95%. The steps at 25, 100, 225, and 475 tx/s each hit the target on every second.

**Long hold, and the uncapped max.** Two lane signers on each physical machine. Depth 2. In-flight 64. 4 connections. Fee frozen at **200 and 300** sompi/gram. Plus the synced desk node, on its own coins, when the sender's own check says that node is synced. On the morning of 7 Oct 2026 the six hostnames were three machines: vector-10 one, muon-10 one, and one server for proton-10, electron-10, quark-10, and neutrino-10. Recheck before counting them. Do not add a third signer on a machine whose lanes are already two deep.

That public-node shape held **2,210 tx/s submit and 2,207 tx/s seen accepted** from 2026-10-06T23:53:27.326Z to 2026-10-07T05:54:53.185Z. The first minute was about 2,500, then it settled. Use the six-hour figure.

**Fee cap 600.** A 10-hour window at 400 and 600, from 2026-10-07T06:39:01.356Z to 2026-10-07T16:38:59.632Z, was **668 tx/s submit and 273 tx/s seen accepted**. Seen accepted is 0 after 08:05Z. It does not beat 2,207. The storm fee stays 200 and 300. Do not switch the storm to 400.

**Ordered stream.** Its own process, its own coins, on proton-10. 2 per second at each tier (4 tx/s). Depth 1. It counts inside the share. It is never mixed into a lane process.

**Do not repeat.** Depth 8. A 45-second burst as the measurement. A fee of 2,000. Ten processes for a few seconds (about 9,100 submit-OK and 28,617 orphans). Two processes on one coin file.

## What to send

Follow `steps-utc.json`. Nothing in the list below is a guess at the clock.

**Off, send nothing:** B0 (first 10 min), B1 (last 10 min), and the two 5-min settles. No lanes and no ordered stream.

**Phases:** B0 → 2× → settle (miners off) → 2× miners-off control → settle (miners on) → 5× → 10× → 20× → 30× → max → B1.

**Each load step:** 15 min at a fixed target, then 5 min of drain at 0. The max step drains for 10 min. Inside a step, do not change the rate, the fees, the depth, or the number of processes.

**Miners-off control:** send exactly what the 2× step sends. stp turns the desk miners off and on. Log the desk miner count at each phase start. Do not switch them.

**Share:** default 25% of each step's added load. The numbers are in `steps-utc.json`, capped at what the dry run held. The max step is uncapped for both senders.

**Sender-limited:** submit-OK stays under 95% of target. Report that. Do not hide it.

**Fees, paced steps.** At step start, read the public node's normal estimate.

- If that quote is the idle floor of 100 sompi/gram, freeze **200 and 300**. A step that freezes at 100 spends the rest of the step under the quote its own traffic creates.
- If the quote is already above 200, freeze that quote and its 1.5×.
- Half the lanes at each tier. A lane keeps its tier for the whole step. Log the quote you read.
- If 1.5× would pass **600**, stop and ask. Do not raise the cap.
- If the sender cannot split fees, use one fee, log it, and tell stp before the run. Those transactions stay out of the 1× vs 1.5× comparison.

**Fees, long hold and uncapped max.** Frozen at **200 and 300**, unless the step-start quote is already above 200. Same 600 cap. Same stop.

**Coins.** Mature coins of at least 2 tKAS that all six public nodes return. Each process has its own file. Two processes never share a coin. For the long hold, split each node's coins by line into two files. Do not use `part i/2` on a host file. Stop and let the mempools drain before a new split.

**Parents.** A sender started inside a short-lived shell dies when that shell closes. Keep the parent alive until the step ends.

## What to log

All times are **UTC, ISO 8601, milliseconds, `Z`**. Example: `2026-10-09T21:30:00.123Z`.

**Per transaction**, one JSON line, in `build-tx-<date>-p<i>.jsonl`. The ordered stream uses `-order`.

| Field | Meaning |
|---|---|
| `seq` | Send sequence, monotonic per process, assigned when the submit starts |
| `txid` | Transaction id |
| `t_submit_start` | UTC time the submit started |
| `t_submit_ok` | UTC time the node answered. Empty if rejected |
| `result` | `ok`, or the reject reason as the node gave it |
| `tier` | `1x` or `1.5x` |
| `feerate` | sompi/gram actually paid |
| `step` | Step name from `steps-utc.json` |
| `stream` | `lane` or `order` |
| `lane` | Lane id, for lane transactions |
| `worker` | Worker or process id |
| `node` | Node used |

**Per second**, one JSON line, in `build-sec-<date>-p<i>.jsonl`: `t`, `step`, `tier`, `target`, `achieved` (submit-OK that second), `submit_ok`, rejects by reason, seen accepted, depth, active workers, active lanes, `cpu_pct` of this process.

**Once per run**, in `build-run-meta-<date>.json`: script file names and their SHA-256, version string, Node and SDK versions, node URLs, F1 per step, NTP offset at the start and at the end, N, each process's coin count (no keys), the fixed desk miner count, the wallet's public address only.

**Clock, before the first transaction and after the last:**

```powershell
w32tm /query /status
w32tm /stripchart /computer:time.windows.com /samples:5 /dataonly
```

Save both outputs, with the UTC time you ran them. If the offset is above 100 ms, tell stp before the run. Resync only if stp says so. If a start or end offset is missing, confirmation times are flagged as uncorrected.

**Where.** The sender's logs folder, the same place the 6–7 Oct holds used. One file set per run date. After the run, zip only these files and give them to stp. Nothing else leaves the desk.

The box matches txids against what n0 sees accepted. Every txid has to be in the log. Per-transaction logs stay **on** for the storm. The pre-run turned them off to save disk.

**During a step.** If the virtual-chain feed goes quiet and depth stays full, that is the failure from 2026-10-06T23:08:02.667Z to 2026-10-06T23:11:51.851Z. Do not let it sit. The sender opens one hop after 15 quiet seconds and resubscribes after 20.

## Dry run

The desk part has passed. Do not repeat N = 1, 2, 4 on storm day unless stp asks for a new gate.

Still required before a storm that claims the gate: the box finds these txids in n0's accepted ids, and the box dry run and the free-disk check are done. Those are not this desk. If a GO leaves one of them open and does not say so, stop and ask.

A repeated dry run, if stp orders one, uses the same script, wallet path, miner count, and process setup as the storm:

1. Ordered stream for 5 min. 2 per second at each tier. Public nodes only.
2. A short `steps-utc.json` from stp. Processes start and stop on those UTC times.
3. Report achieved against target. The paced N stays 4 unless that repeat fails the 95% line.
4. Pass line: mean achieved at least 95% of target at every step, no second at 0, every log field present, `seq` monotonic, both fee tiers present, start and end clock offsets present, txids found on n0.

## Stop rules

- stp says STOP, or a box STOP is relayed: stop at once. Write out the txids still pending.
- Step end: drain at 0. Do not carry load into the next step.
- B0, B1, and the settles: off.
- A node reports a network other than `testnet-10`: stop.
- 1.5× above 600 sompi/gram: stop and ask.
- Wallet running low: stop and tell stp.
- Any error not covered here: stop and ask.
- Do not restart or change settings mid-step. If it happens, log the UTC time and the reason.

## Why the last storm could not be scored

Build's last storm logs had submit-OK counts and no chain inclusion, no time per transaction, and no script version. Several sender paths ran, partly at the same time. The v2 sender added or removed a worker every 90 s, relaunched the fleet on each change, and paused when a mempool was above 80,000. Runners did not hold 100% of target. This run holds the target, uses one shape, and logs the fields above.

## After the run

Write Build's reading in this repo's Build result section, and the same run in [tn10-build-desk-tps](https://github.com/STP-KAS/tn10-build-desk-tps). Exact first and last log times for every step. The bot writes its own section. A figure enters the [challenge repo](https://github.com/STP-KAS/tn10-storm-build-bot-challenge) only when both sides name the same file and recompute the same figure.

Do not fill those sections before the storm.
