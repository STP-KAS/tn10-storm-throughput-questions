# Prompt for Grok Build: next TN10 storm (desk sender)

*Paste-in prompt for Grok Build on stp's desk PC. It follows [`plan/NEXT-STORM-PLAN.md`](https://github.com/STP-KAS/tn10-storm-throughput-questions/blob/main/plan/NEXT-STORM-PLAN.md) (§3a, §4, §4a, §5). If this prompt and the plan disagree, the plan wins. Stop and ask stp.*

**Storm date:** early run no earlier than **Fri 9 Oct 2026, 18:00 UTC**. If the 9th isn't ready, **13 Oct, from 18:00 UTC**. Exact step times come from stp at T0.

**Hard gate: no storm until your dry run passes** (see "Dry run" below). If it hasn't passed in time for the 9th, the storm waits for the 13th.

## Why this time is different

In the last storm your part wasn't measured well:
- your logs had only submit-OK counts, with no inclusion on chain;
- there was no timing per transaction;
- nobody knows which script versions ran;
- your runners did not run at 100% of their target (stp's observation);
- several sender paths ran, partly at the same time;
- the v2 sender was built to add or remove a worker every 90 s and to relaunch the whole fleet with a 10 s gap on each change. Its workers paused whenever the node's mempool was above 80k.

So we could not say how much of your load actually landed, or how fast. This time, follow the plan exactly, hold your target rate, and log what is listed below. If you can't do something, say so before the run. Don't improvise during it.

## Hard rules

1. **TN10 only.** Use only `kaspatest:` addresses and network `testnet-10`. If a node reports any other network, stop.
2. **Public TN10 nodes only.** Never send to stp's node n0 (or `bore.pub`, `127.0.0.1`, `localhost`).
3. **Keys stay on the desk.** Never print, paste, log, upload or commit a key, seed or wallet file. Don't open the key file. Pass only its path to the script.
4. **No public posting.** Don't post or publish anything (X, GitHub, chats). Logs go to stp only.
5. **One sender setup.** Run only the N sender processes and the ordered stream process from this prompt. No other sender from the same wallet. Stop an old one only if stp says so.
6. **No real transactions without stp's GO.** One GO for the dry run, a separate GO for the storm.
7. If anything doesn't match this prompt, **stop and ask stp**.

## Shape that held, for 9 Oct

On test day, start with [`TESTDAY.md`](TESTDAY.md). That file is the run. Do not ask stp to paste commands.

The 6–7 Oct desk pre-run is written in [`DESK-SHAPE-9-OCT.md`](DESK-SHAPE-9-OCT.md). Use that shape on 9 Oct. The six-hour hold, 2026-10-06T23:53:27.326 UTC to 2026-10-07T05:54:53.185 UTC, is the rate that survived: **2,207 tx/s seen accepted**.

- Paced steps, the 25% share: **4** fixed processes, depth **2**, in-flight **48**, the dry-run gate that held **734 tx/s**.
- The long hold and the uncapped max step: **two signers on each physical machine**, depth **2**, in-flight **64**, fee frozen at **200 and 300** sompi/gram, plus the synced desk node with its own coins. The rate that lasted on public nodes alone is **2,207 tx/s seen accepted**, from 2026-10-06T23:53:27.326 UTC to 2026-10-07T05:54:53.185 UTC. The first minutes were higher, about 2,450, and then it settled. On the morning of 7 Oct 2026 the six hostnames were three machines. Recheck before counting them.
- The one-signer depth-2 leg overlapped near 2,050–2,120. The second signer added about 50 tx/s on proton-10, electron-10, quark-10 and neutrino-10. Vector-10 and muon-10 went down. Do not add a third signer while every lane is already two deep.
- Fee cap stays **600**. Depth 8, a 45-second burst, and a fee of 2,000 did not hold.
- A 10-hour hold at **400 and 600**, same depth and the same two signers, started at 2026-10-07T06:38:59 UTC and runs until 2026-10-07T16:38:59 UTC. Its opening seconds were about 2,140 tx/s seen accepted, with the pipes full, so no third signer was added. From 2026-10-07T07:20:00 UTC to 2026-10-07T07:58:00 UTC it was 2,158 tx/s seen accepted, still under 2,207. At 2026-10-07T07:57:46 UTC a synced desk node started four signers and saw 1,538 tx/s accepted over the next minutes. The public feeds then went silent, so those public accepts are not added. At 2026-10-07T08:07 UTC blocks were on the mass ceiling, about 305 transactions and 498,000 of 500,000 compute mass. Until the whole window to 16:38:59 UTC is written down, **9 Oct stays on 200 and 300**. Do not switch the storm to 400 because the test was started. Do add the synced desk node on the long hold.

If that note and [`NEXT-STORM-PLAN.md`](NEXT-STORM-PLAN.md) disagree, the plan wins. Stop and ask stp.

## Process setup for the live storm (settle and test before the storm)

How many processes / PowerShell windows you run **during the storm** is decided in the dry run and then **fixed for the whole storm**.

**Rules:**
- **Fixed N sender processes.** No auto-scaling, no fleet relaunch, no mempool pause during a step. One PowerShell window per process is fine.
- **Separate coins per process:**
  - before the run, pre-split the wallet's coins and give each process its own disjoint set (`--part i/N` style);
  - two processes must never spend the same coin.
- **Split the target evenly:** each process gets the step target ÷ N.
  - Each process reads the same `steps-utc.json` and starts and stops by the UTC clock, not by hand.
- **Connections:** each process keeps 3–4 wRPC connections to public TN10 nodes, and each lane stays pinned to one connection.
  - Spread the processes over different public nodes where the resolver offers them.
  - Log the node per transaction.
- **Ordered stream:** runs in its **own separate process** with its own coin pool. It is never mixed into the lane processes.
- **Logs:**
  - each process writes its own files, with `-p<i>` in the name;
  - `seq` is monotonic per process;
  - the box merges all files by UTC time.
  - All processes are on one PC, so they share one clock.
- **CPU:** the desk also runs CPU miners. A miner keeper adds or removes miners to hold ~75% total CPU, which would change the miner count during a step.
  - For the dry run and the storm, use **one fixed desk miner count** (stp decides), log it, and leave cores for the senders. The one exception is the miners-off control step, when stp turns them off.
  - The keeper must not add or remove miners mid-step.

**Why (labels as in the README):**
- **Claim (measured on the box, as quoted in our v2 Build prompt, 2 Oct):** one Node process with 1 connection gave ~380 accepted tx/s. With 3–4 connections it gave ~1,046.
  - So one process is near its limit at about 1,000 tx/s.
  - Your top planned share is about 725–750 tx/s: 25% of +2,900 tx/s at 30× if the baseline is ~100 tx/s, or of 3,000 in the fallback. One process would have little headroom to hold that steadily.
- **Claim (from our prompts and logs):** your last-storm v2 sender was already multi-process: a coordinator with child workers, each with 4 connections and 250 lanes. One status line showed 24 workers alive.
- **Not sure (inference, not measured):** the shortfall more likely came from the changing worker count, the fleet relaunches and the mempool pauses than from one process vs many. Hence a **fixed** N.
- **Not sure:** how much a desk-to-public-node path sustains per process. That figure (~1,046) is box-to-own-node.
  - Public nodes may rate-limit or lag, so spreading over several nodes may help or may not.
  - Also not sure whether the CPU miners starve the senders.
- **Needs testing:** the best N. The dry run compares **1 vs 2 vs 4 processes**, plus 6 if 4 still falls short, at your top planned share. **Recommendation:** pick the smallest N that holds the target. We expect 2–4.

**Desk setup:** **confirm on the desk** which script you will use, how it splits coins per process, and that it has a fixed-N mode with auto-scaling and mempool-pause off.

## What to send

- **Timetable:** at T0 stp gives you `steps-utc.json`. It holds each step's start and end in UTC, your target per step and the fee rule. Use those UTC times exactly.
- **Baselines and settles:** **off** in B0 (the first 10 min), B1 (the last 10 min) and the two 5-min settle phases around the miners-off control. Send nothing at all.
- **Phases** (all in `steps-utc.json`): B0 → 2× → settle (miners off) → **2× miners-off control** → settle (miners on) → 5× → 10× → 20× → 30× → max → B1. 2 h 55 min in total.
- **Miners-off control:** in that step you send **exactly the same as in the 2× step** (same target, fees and ordered stream). The only change is that all of stp's miners are off, box and desk. stp switches the desk miners off and on at the UTC times; you don't touch them. Log the desk miner count at each phase start.
- **Your share:** a fixed share of each step's *added* load, **default 25%**. The exact numbers are in `steps-utc.json`, capped at what you held in the dry run. The max step is uncapped for both senders.
- **Hold the target rate for the whole step.** Every step runs **15 min at a fixed target**, then **5 min of drain** at 0 (the max step drains for 10 min). Within a step, nothing changes:
  - same rate;
  - same fees;
  - same number of lanes and workers.
- **Fix the shortfall from last time before the storm:**
  - find why your runners didn't reach 100% (pacing, lanes, workers, connections, CPU or the node; **confirm on the desk**) and fix it;
  - your rate must stay steady at the target, not spike and dip.
  - A step counts as **sender-limited** if your submit-OK rate stays below **95% of target**. Report that, don't hide it.
- **Fees:** at each step start, read your public node's normal fee estimate → **F1** (floor 100 sompi/gram), **F1.5 = 1.5 × F1**.
  - Freeze both for the step.
  - Half your lanes pay F1 and half pay F1.5. A lane keeps its tier for the whole step.
  - Log the F1 you read.
  - If your sender can't split fees, use one fee, log it, and tell stp before the run. Your transactions then stay out of the 1× vs 1.5× comparison.
  - If F1.5 is above your sender's fee cap (600 sompi/gram in the earlier scripts; **confirm on the desk**), stop and tell stp. Don't raise the cap.
- **Small ordered stream (sequencing):** same rules as the box stream in plan §4a, during the steps only.
  - Send independent (not chained) self-transfers in sequence, **2 per second per tier at F1 and F1.5**.
  - Use a pool of pre-split coins. Reuse a coin only after its previous transaction was accepted.
  - This stream counts inside your share.
  - Whether your sender can do non-chained sends from a coin pool: **confirm on the desk**.

## What to log

All times are **UTC, ISO 8601 with milliseconds and `Z`** (e.g. `2026-10-09T18:15:00.123Z`).

**Per transaction**, one JSON line each, in `build-tx-<date>-p<i>.jsonl` (one file per process; the ordered stream process uses `-order`):

| Field | Meaning |
|---|---|
| `seq` | Send sequence number, monotonic per sender process, assigned when the submit starts |
| `txid` | Transaction id |
| `t_submit_start` | UTC time the submit started |
| `t_submit_ok` | UTC time the node answered (empty if rejected) |
| `result` | `ok`, or the reject reason as the node gave it |
| `tier` | `1x` or `1.5x` |
| `feerate` | sompi/gram actually paid |
| `step` | Step name from `steps-utc.json` |
| `stream` | `lane` or `order` |
| `lane` | Lane id (for `lane` transactions) |
| `worker` | Worker / process id |
| `node` | Public node URL used |

**Per second**, one JSON line each, in `build-sec-<date>-p<i>.jsonl`:
- `t`, `step`, `tier`;
- **`target`** (tx/s you were told to send) and **`achieved`** (submit-OK that second), so any shortfall shows up second by second;
- `submit_ok`, rejects by reason, and the number of active workers and lanes;
- `cpu_pct` of this process, so a desk-side limit shows up next to any shortfall.

**Once per run**, in `build-run-meta-<date>.json`:
- the script file names and their **SHA-256**, plus the version string;
- Node and SDK versions;
- the node URLs used;
- the F1 per step;
- the desk clock's NTP offset **at the start and at the end** (see "Clock" below);
- the number of sender processes N, and each process's coin set (count of coins, no keys);
- the fixed desk miner count;
- the wallet address (public address only).

**Clock (NTP), at the start and at the end** (**confirm on the desk**: exact commands, and whether the time service is running):
```powershell
w32tm /query /status
w32tm /stripchart /computer:time.windows.com /samples:5 /dataonly
```
- Save both outputs, with the UTC time you ran them, into `build-run-meta-<date>.json`: once before your first transaction, and again after your last.
- If the offset is above 100 ms, tell stp before the run. A resync (`w32tm /resync`, needs admin) is done only if stp says so.
- Your confirmation times are corrected by this offset on the box. If the start or end offset is missing, they are flagged as uncorrected.

**Where:**
- save everything in the sender's `logs` folder (earlier prompts used `%USERPROFILE%\kaspa-tn10\build-storm\logs\`; **confirm on the desk**);
- one file set per run date;
- after the run, zip only these files and give them to stp, who copies them to the box.
- Nothing else leaves the desk.

We match your txids against the transactions n0 sees accepted on the chain. So you don't need to check inclusion yourself, but every txid must be in the log.

## Dry run first: the go/no-go gate (before the storm, after stp's GO)

**No storm until this passes.** If it fails or can't be done in time for Fri 9 Oct, the storm waits for **13 Oct**, and the dry run is repeated before then.

Use the same script, wallet path, miner count and process setup you will use in the storm.

1. **Fee split and order:** run the ordered stream process for **5 min**: 2 per second at F1 and 2 per second at F1.5, through public nodes only.
2. **Mini-timetable:** follow a short `steps-utc.json` from stp, with UTC starts and stops (for example 2 min on, 1 min off, 2 min on). All processes must start and stop on the UTC times.
3. **Process count:** at your top planned share (stp gives the number, ~750 tx/s unless told otherwise), run **3 min each with N = 1, 2 and 4 processes**, and 6 if 4 is still short.
   - Report achieved vs target per second for each N.
   - Pick the smallest N that passes rule 5.
4. **Steps:** with that N, run short steps (2 min each) at each planned Build step target (stp gives the list), plus 1 min at 0 between steps.
5. **Pass criteria.** The box checks all of these:
   - **rate:** at every step, mean `achieved` ≥ **95% of `target`** (the plan's sender-limited line; stp can set another margin before the plan lock), and no seconds at 0;
   - **logs:** every field present, `seq` monotonic per process, all times UTC `Z`, one file set per process;
   - **txid matching:** your txids are found in n0's accepted ids;
   - **timetable:** your starts and stops are within a few seconds of the UTC times (clock offset recorded);
   - **fees:** both tiers present, with F1 logged;
   - **clock:** start and end offsets present in the meta file.
6. If any check fails, fix it and repeat the dry run. Your storm cap is the rate held in step 4, with the N chosen in step 3.

## Stop rules

- **stp says STOP, or a box STOP is relayed:** stop at once (Ctrl+C, or the script's STOP file; all processes watch the same STOP file). Write out the txids still pending.
- **Step end:** go to 0 for the drain. Don't carry load over.
- **B0 and B1:** off.
- A node reports a network other than `testnet-10` → stop.
- F1.5 above your fee cap → stop and ask.
- Wallet running low → stop and tell stp (amount **confirm on the desk**).
- Any error not covered here → stop and ask stp.
- Never restart or change settings mid-step without telling stp. If it happens, log the time and the reason.
