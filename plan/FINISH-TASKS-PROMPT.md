# Prompt for Grok Build: finish the pre-storm tasks

9 Oct 2026. n0 will not run. Do not start it to close a task. The forward node rule is [NEXT-STORM-PLAN.md](NEXT-STORM-PLAN.md), section "Forward routing, 9 Oct 2026". Build uses locus. The bot uses the tunnel to keel.

*Paste this into Grok Build on stp's desk. It closes the desk side of the seven tasks in the README section "Tasks for stp (before the storm)". It does not start the storm.*

If this prompt disagrees with [`NEXT-STORM-PLAN.md`](NEXT-STORM-PLAN.md), the plan wins. Stop and ask stp.

The storm prompt is [`GROK-BUILD-PROMPT.md`](GROK-BUILD-PROMPT.md). The test-day run is [`TESTDAY.md`](TESTDAY.md). Do not use those files for this pass. This pass ends when the seven task lines are updated from measurements, or left open with the one fact that is still missing.

## Hard stops

1. **Do not start the storm.** No storm GO. Do not write `steps-utc.json`. Do not give the final OK on the start time. The start is **Fri 9 Oct 2026, 21:30 UTC, for 8 hours, ending Sat 10 Oct 2026, 05:30 UTC**, otherwise **Mon 13 Oct 2026, 21:30 UTC, ending Tue 14 Oct 2026, 05:30 UTC**.
2. **Do not lock the plan.** Do not commit a "locked" SHA. The lock stays with stp before T0.
3. **Do not run the miner switch.** Desk miners stay **0**. Do not start `kaspa-miner`.
4. **One spender family.** The fee-400 signers have exited. Do not start them again. Do not start `build-storm2`, `p2w.mjs`, `storm-sender`, or a second `measure.mjs` sender. The halt file `C:\Users\Remco\kaspa-tn10\build-storm2\STOP` stays. Its text is `halt`. Do not delete it.
5. **Keys stay on the desk.** Do not print, paste, log, upload, or commit a key, seed, wallet file, address, or txid. Pass a key path only. Public text uses the name Fermi.
6. **TN10 only.** `testnet-10` and `kaspatest` only. Do not send to n0, `bore.pub`, or `159.223.110.159`. This checklist does not send. Do not arm `loc0`–`loc3` or any later signer. Those coin files stay spent. The storm's long hold may use the synced desk node. That permission is in [`GROK-BUILD-PROMPT.md`](GROK-BUILD-PROMPT.md), not here.
7. If a number was not read in this pass, write **not measured**. Do not invent a balance, a disk figure, a usage counter, or an n0 match.

## What already ran

The trial clock has ended. A partial score was taken at 2026-10-07T07:31:43 UTC. The full public score is in tn10-build-desk-tps. Nothing in this list is still sending.

- Twelve public signers plus the order stream. Step `long10-f400`. Depth 2, in-flight 64, fee 400 and 600, cap 600. Parent `long10-f400b.ps1`. The clock ended at **2026-10-07T16:38:59 UTC**. The signers have exited.
- A 90-second slice, 07:30:00 UTC to 07:31:39 UTC, was 2,284 tx/s submit and 2,283 tx/s seen accepted, 0 rejects. The whole public window is now scored in tn10-build-desk-tps: 668 tx/s submit and 273 tx/s seen accepted, and seen accepted is 0 after 08:05 UTC. That does not beat the six-hour **2,207**. 9 Oct stays on **200 and 300** and on **two signers**.
- Desk clock against `time.windows.com`: about **+72 ms** (five samples, +71.5 to +72.0 ms). Miners **0**.
- The desk node was later synced and used for the included-rate tries in tn10-build-desk-tps-3500. This checklist does not start it, stop it, or send through it. The storm's long hold may use it. That permission is in [`GROK-BUILD-PROMPT.md`](GROK-BUILD-PROMPT.md), not here.
- Build wallet at 23:00 UTC on 6 Oct: **3,612,867 tKAS**, **15,944** coins of at least 2 tKAS. The signers have exited. Do not read UTXOs in a documentation pass. A balance re-read stays a separate task.

Do not write a new GO for the fee-400 family.

## The seven tasks

Do them in this order. Update the README task table only with a figure this pass measured. Do not push unless stp says push.

### 1. Dry-run gate

Already passed on the desk: 4 processes, 734 tx/s, 97.9% of 750, 3 minutes, 0 rejects, 0 seconds at 0. The steps at 25, 100, 225, and 475 tx/s each hit the target on every second. Do not repeat the dry run.

The n0 txid match is not a gate. n0 will not run. Do not start it to close this task.

- Confirm the per-transaction logs for that run are still on the desk.
- Write a private manifest next to those logs: path, byte size, SHA-256, UTC window, submit-OK count, reject count. No txids in the manifest. No copy of the logs in the git repo.
- Leave the task open with the line: logs ready on the desk. The n0 match is closed because n0 will not run.
- Do not mark task 1 closed.

### 2. Enough tKAS

The fee-trial signers have exited. A balance re-read is still open, and it is not part of ordering these notes. When stp asks for it: one read, `measure.mjs --mode check`, on a public node. Record `balance_tkas` and `coins_2tkas` and the UTC time. Do not print the address.

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

Leave it **not given**. Do not write a start time. Do not create `steps-utc.json`. Repeat the start: Fri 9 Oct 2026, 21:30 UTC, for 8 hours, ending Sat 10 Oct 2026, 05:30 UTC, otherwise Mon 13 Oct 2026, 21:30 UTC, ending Tue 14 Oct 2026, 05:30 UTC.

## 8. Score the fee trial when its clock ends

This is not an eighth README task. It is what task 5 is waiting on.

- The trial ran to 2026-10-07T16:38:59 UTC. It was not stopped to sample. No signer was added.
- Scored from the twelve public per-second logs, 2026-10-07T06:39:01.356Z to 2026-10-07T16:38:59.632Z: 24,040,746 submits, 9,812,395 seen accepts, 23,942 rejects. That is 668 tx/s submit and 273 tx/s seen accepted. Seen accepted is 0 after 08:05Z. The order stream and the desk-node logs are not in that total.
- 273 is not above **2,207**. The figure is in the desk TPS note. 9 Oct stays on 200 and 300.
- Do not put txids in either repo.

## Done

Reply with the seven task lines, the fee-trial score if the clock has ended, and the list of anything left for stp or the box. The storm is still the later GO.
