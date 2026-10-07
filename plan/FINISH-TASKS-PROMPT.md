# Prompt for Grok Build: finish the pre-storm tasks

*Paste this into Grok Build on stp's desk. It closes the desk side of the seven tasks in the README section "Tasks for stp (before the storm)". It does not start the storm.*

If this prompt disagrees with [`NEXT-STORM-PLAN.md`](NEXT-STORM-PLAN.md), the plan wins. Stop and ask stp.

The storm prompt is [`GROK-BUILD-PROMPT.md`](GROK-BUILD-PROMPT.md). The test-day run is [`TESTDAY.md`](TESTDAY.md). Do not use those files for this pass. This pass ends when the seven task lines are updated from measurements, or left open with the one fact that is still missing.

## Hard stops

1. **Do not start the storm.** No storm GO. Do not write `steps-utc.json`. Do not give the final OK on the start time. Earliest start remains **Fri 9 Oct 2026, 18:00 UTC**, otherwise **13 Oct, from 18:00 UTC**.
2. **Do not lock the plan.** Do not commit a "locked" SHA. The lock stays with stp before T0.
3. **Do not run the miner switch.** Desk miners stay **0**. Do not start `kaspa-miner`.
4. **One spender family.** The fee trial already running is that family. Do not start `build-storm2`, `p2w.mjs`, `storm-sender`, or a second `measure.mjs` sender. The halt file `C:\Users\Remco\kaspa-tn10\build-storm2\STOP` stays. Its text is `halt`. Do not delete it.
5. **Keys stay on the desk.** Do not print, paste, log, upload, or commit a key, seed, wallet file, address, or txid. Pass a key path only. Public text uses the name Fermi.
6. **TN10 only.** `testnet-10` and `kaspatest` only. Do not send to n0, `bore.pub`, or `159.223.110.159`. The desk node at `127.0.0.1:17210` takes no traffic until `measure.mjs --mode check --via own` exits 0, and only the waiter `long10-local.ps1` may arm `loc0`–`loc3`. Do not arm them by hand.
7. If a number was not read in this pass, write **not measured**. Do not invent a balance, a disk figure, a usage counter, or an n0 match.

## What is already running

Leave it running. Scored at 2026-10-07T07:31:43 UTC.

- Twelve public signers plus the order stream. Step `long10-f400`. Depth 2, in-flight 64, fee 400 and 600, cap 600. Parent `long10-f400b.ps1`. Until **2026-10-07T16:38:59 UTC**.
- A 90-second slice, 07:30:00 UTC to 07:31:39 UTC, was 2,284 tx/s submit and 2,283 tx/s seen accepted, 0 rejects. That slice does not replace the six-hour **2,207**. 9 Oct stays on **200 and 300** and on **two signers** until the whole window is scored.
- Desk clock against `time.windows.com`: about **+72 ms** (five samples, +71.5 to +72.0 ms). Miners **0**.
- Local kaspad was in IBD, about 69%, and was not taking traffic.
- Build wallet at 23:00 UTC on 6 Oct: **3,612,867 tKAS**, **15,944** coins of at least 2 tKAS. Do not read UTXOs again while those signers are spending.

Do not delete the `GO` file while those signers are alive. After they exit, do not write a new GO.

## The seven tasks

Do them in this order. Update the README task table only with a figure this pass measured. Do not push unless stp says push.

### 1. Dry-run gate

Already passed on the desk: 4 processes, 734 tx/s, 97.9% of 750, 3 minutes, 0 rejects, 0 seconds at 0. The steps at 25, 100, 225, and 475 tx/s each hit the target on every second. Do not repeat the dry run.

The open part is the **n0 txid match**. This desk is not n0.

- Confirm the per-transaction logs for that run are still on the desk.
- Write a private manifest next to those logs: path, byte size, SHA-256, UTC window, submit-OK count, reject count. No txids in the manifest. No copy of the logs in the git repo.
- Leave the task open with the line: logs ready for the box, n0 match not done.
- Do not mark task 1 closed.

### 2. Enough tKAS

Wait until the fee-trial signers have exited after 16:38:59 UTC. Then one read, `measure.mjs --mode check`, on a public node. Record `balance_tkas` and `coins_2tkas` and the UTC time. Do not print the address.

The Bot wallet stays **OK on stp's word**. Do not spend it. The box balance stays unread unless this desk has a box shell stp already uses. If it does not, write "box balance not measured".

### 3. Usage resets

Already **OK**, per stp on 7 Oct 2026. Do not invent a counter read. Leave the line as it is.

### 4. Box dry run, and 35 GB free at T0

This is the box. If this desk has no shell on the box, leave the task **not done** and say so in one line. Do not guess the free disk. Do not run a dry run on the desk and call it the box dry run.

### 5. Share, then the plan lock

The measured share still fits: **25%**, **4** fixed processes, **734 tx/s** held. Say that in the task line.

Do not lock the plan. Do not change [`NEXT-STORM-PLAN.md`](NEXT-STORM-PLAN.md) into a locked file. After task 8 below, if the full fee-trial window beats 2,207 seen accepted, write that rate into [`DESK-SHAPE-9-OCT.md`](DESK-SHAPE-9-OCT.md) and only then ask stp whether 9 Oct moves off 200 and 300. A short slice is not that window.

### 6. Desk clock, and the miner switch

At the end of this pass, run both and record the UTC time:

- `w32tm /query /status`
- `w32tm /stripchart /computer:time.windows.com /samples:5 /dataonly`

Write the stripchart offset in milliseconds. Count `kaspa-miner` processes. The pre-storm count is **0**. Append one line to `C:\Users\Remco\kaspa-tn10\build-measure\logs\long10-events.log` with the offset and the miner count.

The miner switch is a test-day step. It runs only from [`TESTDAY.md`](TESTDAY.md), at the UTC times in `steps-utc.json`. That file does not exist. Do not switch miners in this pass.

### 7. Final OK on the start time

Leave it **not given**. Do not write a start time. Do not create `steps-utc.json`. Repeat the earliest start: Fri 9 Oct 2026, 18:00 UTC, otherwise 13 Oct, from 18:00 UTC.

## 8. Score the fee trial when its clock ends

This is not an eighth README task. It is what task 5 is waiting on.

- Let the trial run until 2026-10-07T16:38:59 UTC. Do not stop it to sample. Do not add a signer. Lanes that are already two deep stay at two signers. The desk node and the three-machine note are already in DESK-SHAPE. Do not remove them. The fee still waits for the full window.
- When the signers have exited, score the whole window from the per-second logs: submit-OK per second, seen accepted per second, rejects, seconds at 0, UTC start, UTC end.
- If that seen-accepted rate is above **2,207**, write it into [`DESK-SHAPE-9-OCT.md`](DESK-SHAPE-9-OCT.md) as the long-window figure and say the 9 Oct pair can move. If it is not above 2,207, write the figure in the desk TPS note and leave 9 Oct on 200 and 300.
- Do not put txids in either repo.

## Done

Reply with the seven task lines, the fee-trial score if the clock has ended, and the list of anything left for stp or the box. The storm is still the later GO.
