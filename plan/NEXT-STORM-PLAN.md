# Next TN10 storm: measurement plan

**Early run: no earlier than Fri 9 Oct 2026, 20:00 CEST** (waiting on usage resets for the bots and Build, and enough tKAS). **If the 9th isn't ready, 13 Oct 2026 (evening CEST) stays the target.** The 6 Oct early run is cancelled. Either date runs only after the instrumentation passes its dry run.
Questions and guidance from Kaspa Pulse ([@gokugalax](https://x.com/gokugalax)), including the sequencing point (thank you). Plan by TN10 ops, stp's AI operator bot for his TN10 stack.
Kaspa Testnet-10 (TN10) only. Deliberate load stays on TN10 by design; mainnet comparisons and mainnet costing are out of scope, as Kaspa Pulse asked.

Status: **draft until locked** (see §1). Labels as in the [README](../README.md#labels-used-in-this-readme): **Claim (measured on TN10)**, **Not sure / open for debate**, **Needs more testing**.

## What: Kaspa Pulse's four questions + sequencing are the measured goals

**Headline: not just how many transactions land, but whether order holds under load.** A reorder or a stall would break a dapp that expects its transactions in order.

| # | Question (Kaspa Pulse) | What we log (UTC) | What we chart / report |
|---|---|---|---|
| 1 | Accepted tx/s vs submitted over the whole storm, and where acceptance flattens | Per second: submitted / accepted / offered for the box and for Build, by fee tier; network-wide unique accepted (counts Build's and everyone's transactions); rejects by reason (§4) | Submitted vs accepted per second and per step; accepted vs step target; sender-limited steps marked |
| 2 | Confirmation time at each load step (median and worst), normal fee vs 1.5× | Per transaction: send sequence number, submit and accept times, fee tier; 1× / 1.5× lane split (box and Build) plus probes at 1×, 1.2×, 1.5×, 2× (§4, §5) | p50 / p95 / p99 / worst per step and tier; share > 30 s and > 60 s; send vs accept order |
| 3 | Does the indexer freeze, at what sustained tps, and for how long | api-tn10 health every 30 s; once a minute, the time until one of our transactions is visible (§6) | Per freeze: step, minutes into the step, sustained tx/s (ours and network), length, recovery |
| 4 | Mempool depth over time | n0 mempool every 1 s; fee estimate every 10 s (§6) | Mempool per second against the steps |
| 5 | Send order vs accept order: does order hold under load? | Per-sender send sequence numbers, UTC submit times, accept position on n0 (event index + position); a dapp-like ordered stream at 1× and 1.5× (§4a) | Per step and tier: reorder rate, out-of-order accepts, stalls (count, longest); ties and fee-driven overtakes reported separately |

The two headline comparisons are **1× vs 1.5× fee** (does paying more buy inclusion under load?) and **order under load** (does it hold, and does 1.5× keep it when 1× doesn't?).

**Participants (both measured):**
- **TN10 ops** (stp's AI operator bot), sending from stp's box through its own node n0;
- **Grok Build**, sending from stp's desk PC through public TN10 nodes (§3a).

The sections below are the **Method**: Kaspa Pulse's six process points (§1–§4, §7, §8), plus fee tiers (§5), indexer and mempool (§6) and box limits (§9).

## Up front: what the results will and won't describe

- Our own miners made **50–63% of TN10 blocks** while they ran in earlier storms. That is a **Claim (measured on TN10)** from the storm 2 public report (`block_share_legs.csv`, `block_share_sampler2.csv`). We'll measure and publish the **exact share for this run, per step** (§7).
- So the results describe **TN10, with our miners and Build's desk load on it, measured through one node on one small box**. We'll say so again in the results.

## 1. The plan is written down and locked before the run

- This file is the plan. Before T0 we take the SHA of the last commit that changed it (`git log -1 --format=%H -- plan/NEXT-STORM-PLAN.md`) and write it in the run log at T0.
- The results README cites that SHA at the top, with a link to this file at that commit.
- After the lock the plan is not edited. Anything we do differently on the night goes in a **"Deviations from the locked plan"** section of the results, with the time and the reason.
- The results are published next to this plan, in this repo.

## 2. Baseline first

- **B0, 10 min of normal TN10 traffic** before any load step. Both our senders (box runners and Build) are off. Everything else runs exactly as during the steps: the samplers, the fee probes (4 small transactions every 10 s, ~0.4 tx/s), the indexer probe, the mining-share counter, and the same miner state.
- From B0 we compute the **baseline load B** = median network-wide unique accepted tx/s over the 10 minutes, and the baseline confirmation times per fee tier.
- **B1, a 10-min after-load baseline** at the end, after the final drain, with the same measurements. It shows whether things went back to normal.
- For scale: before the 1 Oct storm, n0's "Processed" counter showed ~100 tx/s (mean 99.8 over 1 Oct 18:41–20:10 CEST, `host.jsonl`). That counter overstates unique transactions, so B is likely somewhat lower *(estimate)*.

## 3. Fixed steps, not one blast

- Steps are **multiples of the measured baseline B**: **2×, 5×, 10×, 20×, 30×**, then **max**. At step m, our two senders together add (m − 1) × B tx/s on top of normal traffic.
  - If B ≈ 100 tx/s, that's roughly +100, +400, +900, +1,900, +2,900 tx/s from us, about the same range as the October storm.
  - **Fallback:** if B is below 50 or above 200 tx/s, we use the absolute steps from the first draft instead (500, 1,000, 1,500, 2,000, 2,500, 3,000 tx/s, then max) and report each one as a multiple of B.
  - Every step is reported both ways: as a multiple of B, and in absolute tx/s.
- **Each step is 15 min at a fixed target, followed by 5 min of drain** (runners at 0, all measurements still on). The max step uses 7 runners, no cap, and a 10-min drain.
- **Within a step nothing changes:** target rate, fee tiers, pace band, runner count and miner state are all fixed. The scaler and the automatic fee daemon are off.
- Timeline: B0 10 min + 6 steps × 20 min + 5 extra drain minutes + B1 10 min ≈ **2 h 25 min**. Start no earlier than 20:00 CEST; T0 ≈ 20:15 CEST (after the 19:05–20:10 pruning-window slowdown), and finish well before 01:00.
- Workers: 6 runners × 4 wRPC connections, a 7th only for the max step. Never 8; it collapsed throughput on 2 Oct.
- **Box and Build follow the same UTC timetable.** Step start times are fixed in UTC at T0 and given to both.

### 3a. Grok Build as a participant
- Build sends from stp's desk PC through public TN10 nodes, alongside the box runners. It is off in B0 and B1.
- **Per-step share:** Build's target is a fixed share of each step's added load, written into the locked plan before T0 (default **25%**, capped at what its sender sustains in a pre-run test). The box sends the rest. The max step has both senders uncapped. Actual rates are measured for both.
- **Fees:** the same two tiers, 1× and 1.5× of its node's normal fee estimate, split across Build's lanes and fixed per step. If its sender can't split, its single fee is logged and its transactions are left out of the 1× vs 1.5× comparison.
- **Logging (desk):** per second (UTC), submit-OK and rejects by reason; per transaction, txid, send sequence number, UTC submit time and fee tier. The desk clock's offset from UTC is recorded at T0.
- **Acceptance:** Build's txids are matched against the transaction ids n0 sees accepted on the chain. n0 sees every accepted transaction, whichever node it was sent to. So Build's accepted count and confirmation times are measured on the same clock as the box's, and they count in the network-wide unique total.
- No keys or wallet files leave the desk. Only public txids and timestamps are shared.

- A step counts as **sender-limited** if our submit-OK rate stays below 95% of its target. We report that separately from "the network stopped accepting".

## 4. Per-second logs in UTC, and send order vs accept order

- **All timestamps are UTC**, ISO 8601 with milliseconds (`2026-10-09T18:15:00.123Z`), from the box clock. NTP status is recorded at T0. Summaries also show CEST.
- **Per second**, each box runner and Build's sender log: submitted (submit-OK), rejected by reason, offered (rate-limiter tokens granted), and accepted, split by fee tier. Accepted is counted twice: by the second it was accepted, and by the second it was submitted.
- **Per second**, network-wide: unique accepted transactions, counted from the transaction ids in n0's `virtual-chain-changed` notifications (this replaces the double-counting "Processed" counter); n0's mempool size; blocks added, and how many of them were ours.
- **Per transaction** (lanes in a fixed 1-in-10 sample; all probes), we record:
  - a **send sequence number** `seq`, monotonic per runner and assigned when the submit starts;
  - `t_submit_start`, `t_submit_ok` and `t_accept`;
  - the acceptance position: the index of the `virtual-chain-changed` event, plus the transaction's position inside it;
  - the fee tier, step, runner and lane.
- **Ordering:** see §4a. It is a first-class metric, reported per step next to the four questions.

### 4a. Sequencing: does order hold under load?
- **Send order:** every sender (each box runner, Build's sender, the probe process, the ordered stream) assigns a monotonic **send sequence number** when a submit starts, logged with the UTC time.
- **Accept order:** the position in n0's `virtual-chain-changed` stream (event index, then position inside the event's accepted ids). Transactions in the same event are **ties**, reported separately, not counted as reorders.
- **Dapp-like ordered stream:** a dedicated process sends independent (not chained) self-transfers in sequence, **2 per second per tier at 1× and 1.5×**, from a pool of pre-split coins. A coin is reused only after its previous transaction was accepted, so no stream transaction depends on another one in the mempool. It runs through B0, every step and B1. This is the closest stand-in for an app that sends a series of transactions and expects them in order.
- **Metrics per step and tier:**
  - **Reorder rate:** the share of same-sender, same-tier transaction pairs sent ≥ 1 s apart that were accepted in reverse order. Consecutive pairs and all pairs are both reported.
  - **Out-of-order accepts:** the count and share of transactions accepted before at least one earlier-sent transaction of the same sender and tier.
  - **Stalls:** a transaction still not accepted 30 s after a later-sent transaction of the same sender and tier was accepted. We report the count, the longest stall, and anything never accepted by the end of the step's drain.
  - **Fee-driven overtakes:** 1.5× transactions accepted before an earlier-sent 1× transaction. That's expected priority, reported separately from reorders within a tier.
- **Lanes:** box and Build lanes are chained, so order inside a lane is forced and excluded. Cross-lane pairs from the sampled lanes are included.
- **Prior data:** the 25 Sep probes (30 s apart) already show 2.6–10.4% of consecutive 1×/1.2× probes accepted out of order, and none at 2× and above in step B ([README Q5](../README.md#q5-send-order-vs-accept-order-sequencing)).
- **Pending at stop:** anything not accepted when the run stops is listed with its tier and step. Runners are not restarted mid-step; if one is, that is logged.

## 5. Fee tiers (the 1× vs 1.5× question)

- At each step start we read n0's normal fee estimate → **F1** (floor 100 sompi/gram) and set **F1.5 = 1.5 × F1**. Both are frozen for the step. Build applies the same rule with its public node's estimate, and that value is logged.
- In every runner, even lanes pay F1 and odd lanes pay F1.5: same runner, connections, transaction shape (643-gram hops) and moment. A lane keeps its tier for the whole step.
- **Probes:** a separate process sends one small, non-chained, signed self-transfer per tier (**1×, 1.2×, 1.5×, 2×** of F1) every 10 s, from its own wallets. That's ~90 probes per tier per 15-min step. 1.2× and 2× link back to the 25 Sep probes.
- Reported per step and tier: count, p50, p95, p99 and worst submit → first-acceptance time, and the share over 30 s and over 60 s.

## 6. Indexer and mempool

- **Indexer (api-tn10.kaspa.org):**
  - `GET /info/health?nc=<ms>` every 30 s (cache bypass), logging the HTTP status, `acceptedTxBlockTimeDiff`, `blueScoreDiff` and `isSynced`;
  - once a minute, one already-accepted probe transaction is polled with `GET /transactions/<txid>` every 5 s until it shows up (give up after 30 min). At most ~0.3 requests/s in total.
  - **Freeze rule:** 3 consecutive samples (90 s) with 503 or timeout, or a lag above 120 s and rising, or a visibility delay above 300 s. We report the step, the minutes into the step, our tx/s and network tx/s at that point, the freeze length and the recovery time.
  - A second public indexer is used only if we can confirm one exists beforehand.
- **Mempool:** n0 `mempoolSize` every 1 s and the fee estimate every 10 s. Optionally, a fee-band snapshot every 5 min while the mempool is under 50k.

## 7. Mining share

- For every block n0 adds, the coinbase payout script is compared with stp's mining addresses (box and desk miners). Logged per second and summarised per step: blocks total, blocks ours, **our share in %**.
- The box miners' on/off state is fixed for the whole run and printed in the results. The desk miners count as "ours". Build's sender takes part as in §3a.
- Optional, if disk allows after B1: one extra 15-min max step with our box miners off, to show how much our hashrate mattered. It runs after the main plan and is marked as an extra.

## 8. Publication: raw data next to the summary

The results go into this repo:
- **`data/`, raw and per-second files** (CSV / JSONL, UTC):
  - `steps.jsonl`: step boundaries, targets, B, F1/F1.5, runner count, miner state;
  - `per_second.csv`: submitted, accepted and offered per tier, network unique accepted, mempool, blocks and our blocks;
  - `probes.csv`: every probe, with txid;
  - `ordered_stream.csv`: the dapp-like ordered stream, with send sequence, UTC submit time and accept position;
  - `order_per_step.csv`: reorder rate, out-of-order accepts, stalls and ties per step and tier;
  - `build_per_second.csv` and `build_tx_sample.csv.gz`: Build's per-second counters and per-transaction sample, with acceptance matched on n0;
  - `tx_sample.csv.gz`: per-transaction sample with `seq` and timestamps (1-in-100 lanes in the repo; the 1-in-10 file on request if too large for GitHub);
  - `mempool_1s.csv`, `indexer.jsonl`, `fee_estimates.jsonl`, `mining_share_per_step.csv`, and a per-step summary CSV.
- Txids of the P2W lanes are published **after the lane coins have been swept**: those lanes are anyone-can-spend on TN10.
- **Charts** (PNG): submitted vs accepted per second and per step; confirmation time per step and tier (1× vs 1.5×); send vs accept order; mempool per second; indexer lag; mining share per step.
- No keys or recovery phrases, and no private paths.
- Each file stays under 50 MB.

## 9. Box limits (our setup, not protocol limits)

- One node (n0, kaspad 2.1.0, `--ram-scale=0.1`, mempool cap ~100k) on an 8-vCPU / 16 GB / 126 GB box.
- **Disk:** keep ~19 GB free for n0's pruning at all times. The morning pruning window (~07:15–08:30 CEST) needs 11–15 GB of temporary disk; a pruning disk-full crashed n0 on 3 Oct.
  - On 2 Oct, ~2.2k tx/s used ~4.7–5.0 GB/h, so this schedule needs roughly 10–12 GB *(estimate)*.
  - **Go only with ≥ 35 GB free at T0.** With 28–35 GB, steps shrink to 10 min (recorded as a deviation). Below 28 GB, no storm.
- **Guards** (unchanged): runner pause at ≤ 21 GB free; STOP below 19 GB for more than 900 s; immediate STOP at 10 GB or RAM < 1 GB; STOP if n0 is unsynced or more than 300 s behind. A guard stop ends the run early for both senders (box and Build) and is reported as such.

## 10. Later leg (idea, not planned yet)

**Proposal only.** This is not scheduled, not part of the plan above, and nothing here is promised.

First we finish this leg: one measured run, done in order, with the raw data and facts published.

After that, one idea is an open leg on TN10. Builders, core contributors and others would be invited to test their own apps under high congestion, for example covenants, dapps, vProgs such as tic-tac-toe, KaChat, dotK, Kasperolabs, and others. Each app would see how it behaves when blocks are full and fees rise, next to the same public measurements (accepted tx/s, confirmation time, order, mempool). Who takes part, when and how would be agreed openly first.
