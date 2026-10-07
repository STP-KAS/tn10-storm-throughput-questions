# Next TN10 storm: measurement plan

**Early run: no earlier than Fri 9 Oct 2026, 20:00 CEST** (waiting on usage resets for the bots and Build, and enough tKAS). **If the 9th isn't ready, 13 Oct 2026 (evening CEST) stays the target.** The 6 Oct early run is cancelled. Either date runs only after the instrumentation passes its dry run.

**Not a one-off.** This is a series, not a single run. There is no deadline. Each run is published with its own locked plan and raw data, and the changes between runs are listed.

**Kaspa Pulse, 7 Oct 2026:** "Weekly runs sound good. I'd rather see one clean run first and go through those numbers properly before we stack more. Send me the results when it's done and we'll take it from there."

So: one clean run first. Go through those numbers properly. Send him the results when that run is done. Weekly repeats wait until that pass. Nothing else is stacked on top before then.

Questions and guidance from Kaspa Pulse ([@gokugalax](https://x.com/gokugalax)), including the sequencing point, his review of this plan with four tightenings, and the 7 Oct note above (thank you for all three). Plan by TN10 ops, stp's AI operator bot for his TN10 stack.
Kaspa Testnet-10 (TN10) only. Deliberate load stays on TN10 by design; mainnet comparisons and mainnet costing are out of scope, as Kaspa Pulse asked.

Status: **draft until locked** (see §1). Labels as in the [README](../README.md#labels-used-in-this-readme): **Claim (measured on TN10)**, **Not sure / open for debate**, **Needs more testing**.

## What: Kaspa Pulse's four questions + sequencing are the measured goals

**Headline: not just how many transactions land, but whether order holds under load.** A reorder or a stall would break a dapp that expects its transactions in order.

| # | Question (Kaspa Pulse) | What we log (UTC) | What we chart / report |
|---|---|---|---|
| 1 | Accepted tx/s vs submitted over the whole storm, and where acceptance flattens | Per second: submitted / accepted / offered for the box and for Build, by fee tier; network-wide unique accepted (counts Build's and everyone's transactions); rejects by reason (§4) | Submitted vs accepted per second and per step; accepted vs step target; **saturation onset by the fixed rule (§3c)**; each plateau labelled box-bound / network-bound / unclear (§6a); sender-limited steps marked |
| 2 | Confirmation time at each load step (median and worst), normal fee vs 1.5× | Per transaction: send sequence number, submit and accept times, fee tier; 1× / 1.5× lane split (box and Build) plus probes every 2 s at 1×, 1.2×, 1.5×, 2× (§4, §5) | n and p50 / p95 / p99 / worst per step and tier, with intervals (~450 per tier per step; ~2,250 for 1× and 1.5×); share > 30 s and > 60 s; send vs accept order |
| 3 | Does the indexer freeze, at what sustained tps, and for how long | api-tn10 health every 30 s; once a minute, the time until one of our transactions is visible (§6) | Per freeze: step, minutes into the step, sustained tx/s (ours and network), length, recovery |
| 4 | Mempool depth over time | n0 mempool every 1 s; fee estimate every 10 s (§6) | Mempool per second against the steps |
| 5 | Send order vs accept order: does order hold under load? | Per-sender send sequence numbers, UTC submit times, accept position on n0 (event index + position); a dapp-like ordered stream at 1× and 1.5× (§4a) | Per step and tier, **as counts and percentages with n and a 95% interval**: reorder rate, out-of-order accepts, stalls (count, longest); ties and fee-driven overtakes reported separately; **miners-off control vs the same step with miners on (§3b)** |

The two headline comparisons are **1× vs 1.5× fee** (does paying more buy inclusion under load?) and **order under load** (does it hold, and does 1.5× keep it when 1× doesn't?).

**Participants (both measured):**
- **TN10 ops** (stp's AI operator bot), sending from stp's box through its own node n0;
- **Grok Build**, sending from stp's desk PC through public TN10 nodes (§3a).

The sections below are the **Method**: Kaspa Pulse's six process points (§1–§4, §7, §8), plus fee tiers (§5), indexer and mempool (§6) and box limits (§9).

## Up front: what the results will and won't describe

- Our own miners made **50–63% of TN10 blocks** while they ran in earlier storms. That is a **Claim (measured on TN10)** from the storm 2 public report (`block_share_legs.csv`, `block_share_sampler2.csv`). We'll measure and publish the **exact share for this run, per step** (§7).
- So the results describe **TN10, with our miners and Build's desk load on it, measured through one node on one small box**. We'll say so again in the results.

## Kaspa Pulse's four tightenings (review of 5 Oct, before the lock)

| # | Tightening | Where in this plan |
|---|---|---|
| 1 | **Miners-off control in the main run.** One fixed step with all our miners off, at a load the remaining miners can absorb, matched to the same step with miners on. It separates "the network reorders" from "our block templates reorder". Mining share published per step | §3b, §7 |
| 2 | **Separate the box from the chain.** Everything goes through n0 (real flags stated). Log n0 CPU, mempool-cap hits, evictions and reject reasons, plus the runners' CPU. Every plateau is labelled box-bound, network-bound or unclear, by fixed criteria | §6a |
| 3 | **Synced clocks.** NTP offset logged on the box and the desk at start and end. Cross-machine confirmation times are corrected for the offset, or flagged | §4 |
| 4 | **Saturation defined before T0**: our accepted below 95% of our submitted, sustained for 60 s (exact rule in §3c). Reorder rates as counts and percentages with n and a 95% interval. Probe n raised from ~90 to ~450 per tier per step (~2,250 for 1× and 1.5× with the ordered stream) | §3c, §4a, §5 |

## 1. The plan is written down and locked before the run

- This file is the plan. Before T0 we take the SHA of the last commit that changed it (`git log -1 --format=%H -- plan/NEXT-STORM-PLAN.md`) and write it in the run log at T0.
- The results sections of the README cite that SHA, with a link to this file at that commit.
- After the lock the plan is not edited. Anything we do differently on the night goes in a **"Deviations from the locked plan"** section of the results, with the time and the reason.
- The results are published next to this plan, in this repo. Build's result and the bot's result each keep their own section.
- Once both of those sections are filled, the check of one against the other is [tn10-storm-build-bot-challenge](https://github.com/STP-KAS/tn10-storm-build-bot-challenge). That page stays empty until then. It does not replace the two result sections.

## 2. Baseline first

- **B0, 10 min of normal TN10 traffic** before any load step. Both our senders (box runners and Build) are off. Everything else runs exactly as during the steps: the samplers, the fee probes (4 small transactions every 2 s, 2 tx/s), the box ordered stream (4 tx/s), the indexer probe, the mining-share counter, and the same miner state (miners on).
- From B0 we compute the **baseline load B** = median network-wide unique accepted tx/s over the 10 minutes, **minus our own probe and stream transactions** (known by txid), and the baseline confirmation times per fee tier.
- **B1, a 10-min after-load baseline** at the end, after the final drain, with the same measurements. It shows whether things went back to normal.
- For scale: before the 1 Oct storm, n0's "Processed" counter showed ~100 tx/s (mean 99.8 over 1 Oct 18:41–20:10 CEST, `host.jsonl`). That counter overstates unique transactions, so B is likely somewhat lower *(estimate)*.

## 3. Fixed steps, not one blast

- Steps are **multiples of the measured baseline B**: **2×, 5×, 10×, 20×, 30×**, then **max**. At step m, our two senders together add (m − 1) × B tx/s on top of normal traffic.
  - If B ≈ 100 tx/s, that's roughly +100, +400, +900, +1,900, +2,900 tx/s from us, about the same range as the October storm.
  - **Fallback:** if B is below 50 or above 200 tx/s, we use the absolute steps from the first draft instead (500, 1,000, 1,500, 2,000, 2,500, 3,000 tx/s, then max) and report each one as a multiple of B.
  - Every step is reported both ways: as a multiple of B, and in absolute tx/s.
- **Each step is 15 min at a fixed target, followed by 5 min of drain** (runners at 0, all measurements still on). The max step uses 7 runners, no cap, and a 10-min drain.
- **Within a step nothing changes:** target rate, fee tiers, pace band, runner count and miner state are all fixed. The scaler and the automatic fee daemon are off.
- **Timetable (fixed; times relative to T0):**

| # | Phase | Load | Our miners | Length | Ends at |
|---|---|---|---|---|---|
| 1 | B0 baseline | senders off | on | 10 min | T0+10 |
| 2 | **2×** (also the miners-on half of the control pair) | 2× B | on | 15 + 5 drain | T0+30 |
| 3 | Settle, miners off | senders off | **off** | 5 min | T0+35 |
| 4 | **2× miners-off control** (§3b) | same target as row 2 | **off** | 15 + 5 drain | T0+55 |
| 5 | Settle, miners back on | senders off | on | 5 min | T0+60 |
| 6–9 | **5×, 10×, 20×, 30×** | m × B | on | 4 × (15 + 5) | T0+140 |
| 10 | **max** | 7 runners, uncapped | on | 15 + 10 drain | T0+165 |
| 11 | B1 after-load baseline | senders off | on | 10 min | T0+175 |

  Total **2 h 55 min**. Start no earlier than 20:00 CEST; T0 ≈ 20:15 CEST (after the 19:05–20:10 pruning-window slowdown), so it ends ≈ 23:10 CEST, well before 01:00. Probes, the box ordered stream and all samplers run through every phase.
- Workers: 6 runners × 4 wRPC connections, a 7th only for the max step. Never 8; it collapsed throughput on 2 Oct.
- **Box and Build follow the same UTC timetable.** Step start times are fixed in UTC at T0 and given to both.

### 3b. Miners-off control step (part of the main run)
- **Purpose:** our miners made 50–63% of TN10 blocks, so a reorder could come from **our own block templates** rather than from the network. One step with **all our miners off** (box and desk), compared with the same step with them on, separates the two.
- **Load: matched and low, so it measures order, not backlog.**
  - **Claim (measured on TN10):** in storm 2, after our box miners stopped (Fri 01:31:50), our inclusion fell to **~300 tx/s** for five hours, while n0's mempool sat at a median of 71,498 (max 99,992). That's a backlog, not a reorder signal (storm 2 public report, L1 and mempool tables).
  - So the control runs at the **2× step's target** (≈ 200 tx/s total if B ≈ 100, of which ≈ +100 from us), well under that ~300 tx/s. If 2× B would exceed **250 tx/s total**, both halves of the pair (rows 2 and 4) run at 250 tx/s total instead, and that is recorded.
  - Same split as the 2× step: box and Build shares, fee tiers, probes and ordered stream unchanged. Only the miners change.
- **Backlog check:** if the control step hits saturation (§3c) at any point, it is flagged **"backlog-bound"** and its reorder numbers are **not used as a control**. They are still published.
- **Miner switching:** box miners are stopped and restarted by the scheduler. stp switches the desk miners at the same UTC times. Both are logged. The 5-min settle phases are at zero load, with probes on.
- **Not sure / open for debate: this is an imperfect control.**
  - When ~half the hashrate stops, TN10's block rate drops until difficulty adjusts. It rises again when our miners come back. We log blocks per second and difficulty in every phase and report them next to the result.
  - The other miners' templates, software and hashrate are not ours to fix. They can change between the two halves of the pair.
  - A low load may hide reordering that only appears at high load.
  - So a difference between the two halves is evidence, not proof, of where reordering comes from.

### 3c. Saturation rule (fixed before T0)
- For every second *t* of a load step, from 60 s after the step start to the end of the step:
  - **S60(t)** = our submit-OK count in the window (t − 60 s, t]: box lanes, Build (all processes), ordered streams and probes;
  - **A60(t)** = how many of **our** transactions were accepted on n0's virtual chain in the same window, by accept time (Build matched by txid).
- The step is **saturated** from the first second *t* at which **A60 < 0.95 × S60 holds for 60 consecutive seconds**. That *t* is the **saturation onset**.
- We report, per step: saturated yes/no, the onset (UTC and minutes into the step), A60/S60 at onset and at the step end, and whether the drain cleared the backlog.
- The **saturation point** of the run is the lowest step target at which saturation occurs. The same rule is also reported per sender (box, Build) as a breakdown.

### 3a. Grok Build as a participant
- Build sends from stp's desk PC through public TN10 nodes, alongside the box runners. It is off in B0 and B1.
- **Per-step share:** Build's target is a fixed share of each step's added load, written into the locked plan before T0 (default **25%**, capped at what its sender sustains in a pre-run test). The box sends the rest. The max step has both senders uncapped. Actual rates are measured for both.
- **Fees:** the same two tiers, 1× and 1.5× of its node's normal fee estimate, split across Build's lanes and fixed per step. If its sender can't split, its single fee is logged and its transactions are left out of the 1× vs 1.5× comparison.
- **Steady rate:** last storm Build's runners did not run at 100% of their target (stp's observation). Build fixes that before the storm. Its runners hold the step target for the whole step, and the shortfall, if any, is visible per second.
- **Ordered stream (desk):** during the steps (not B0/B1), Build also sends a small ordered stream under the §4a rules (independent self-transfers, 2 per second per tier at 1× and 1.5×, from a pre-split coin pool), inside its share. That way order is also measured for transactions sent through public nodes.
- **Logging (desk):** per second (UTC): **target and achieved send rate**, submit-OK and rejects by reason; per transaction: txid, send sequence number, UTC submit start and submit-OK times, submit result, fee tier, fee rate, step and stream. Once per run: script names with SHA-256 and versions, node URLs, F1 per step. The desk clock's offset from UTC is recorded at T0.
- **Process setup (live storm):** Build runs a **fixed number N of sender processes** for the whole storm. There is no auto-scaling, no fleet relaunch and no mempool pause within a step.
  - Each process has its own disjoint coin set and its own log files, merged by UTC.
  - Each process has 3–4 connections to public nodes and gets target ÷ N.
  - The ordered stream runs in a separate process.
  - The desk miner count is fixed and logged.
  - N is picked in the dry run.
- **Go/no-go gate: no storm until Build's dry run passes.** Before the storm, Build:
  - sends a small ordered, fee-split stream;
  - compares N = 1, 2 and 4 (and 6 if needed) at its top planned share;
  - then runs short steps at each planned Build target with the chosen N.

  It passes only if:
  - at every step, mean achieved is ≥ 95% of target (default margin; agreed before the lock), with no zero seconds;
  - the per-transaction and per-second logs are complete;
  - its txids are matched against n0's accepted ids;
  - starts and stops follow the UTC timetable.

  If it fails or isn't done in time for 9 Oct, the storm waits for 13 Oct. Build's storm cap is the rate it held.
- **Prompt:** [`GROK-BUILD-PROMPT.md`](GROK-BUILD-PROMPT.md).
- **Acceptance:** Build's txids are matched against the transaction ids n0 sees accepted on the chain. n0 sees every accepted transaction, whichever node it was sent to. So Build's accepted count and confirmation times are measured on the same clock as the box's, and they count in the network-wide unique total.
- No keys or wallet files leave the desk. Only public txids and timestamps are shared.

- A step counts as **sender-limited** if our submit-OK rate stays below 95% of its target. We report that separately from "the network stopped accepting".

## 4. Per-second logs in UTC, and send order vs accept order

- **All timestamps are UTC**, ISO 8601 with milliseconds (`2026-10-09T18:15:00.123Z`). Summaries also show CEST.
- **Clocks (tightening 3):**
  - **Box:** the box is a container on a cloud VM. It has no NTP daemon of its own; its clock comes from the host. We log its offset against two public NTP servers (`pool.ntp.org`, `time.cloudflare.com`, SNTP query) at T0, every 10 min and at the end. Checked Mon 5 Oct, ~21:15 CEST: −9 ms and −8 ms.
  - **Desk:** Windows Time. Build logs `w32tm /query /status` and the offset from `w32tm /stripchart /computer:time.windows.com /samples:5 /dataonly` at start and end (exact commands confirmed on the desk).
  - **Box-only confirmation times** (box runners, box probes, box stream) use the box clock at both ends, so the offset cancels. Only drift matters, and it is logged.
  - **Build's confirmation times** are t_accept (box clock) − t_submit (desk clock), **corrected** by (desk offset − box offset), interpolated linearly between start and end. If either offset is missing, or the desk offset moved by more than 50 ms between start and end, Build's confirmation times are **flagged** and reported separately as uncorrected.
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
  - **Reorder rate:** same-sender, same-tier transaction pairs sent ≥ 1 s apart that were accepted in reverse order. Consecutive pairs and all pairs are both reported, **always as a count and a percentage, with n and a 95% interval** (Wilson). Example of the format, not a result: "23 of 449 consecutive pairs (5.1%, 95% CI 3.4–7.6%)".
  - **Out-of-order accepts:** the count and share of transactions accepted before at least one earlier-sent transaction of the same sender and tier.
  - **Stalls:** a transaction still not accepted 30 s after a later-sent transaction of the same sender and tier was accepted. We report the count, the longest stall, and anything never accepted by the end of the step's drain.
  - **Fee-driven overtakes:** 1.5× transactions accepted before an earlier-sent 1× transaction. That's expected priority, reported separately from reorders within a tier.
- **Lanes:** box and Build lanes are chained, so order inside a lane is forced and excluded. Cross-lane pairs from the sampled lanes are included.
- **Prior data:** the 25 Sep probes (30 s apart) already show 2.6–10.4% of consecutive 1×/1.2× probes accepted out of order, and none at 2× and above in step B ([README Q5](../README.md#q5-send-order-vs-accept-order-sequencing)).
- **Pending at stop:** anything not accepted when the run stops is listed with its tier and step. Runners are not restarted mid-step; if one is, that is logged.

## 5. Fee tiers (the 1× vs 1.5× question)

- At each step start we read n0's normal fee estimate → **F1** (floor 100 sompi/gram) and set **F1.5 = 1.5 × F1**. Both are frozen for the step. Build applies the same rule with its public node's estimate, and that value is logged.
- In every runner, even lanes pay F1 and odd lanes pay F1.5: same runner, connections, transaction shape (643-gram hops) and moment. A lane keeps its tier for the whole step.
- **Probes:** a separate process sends one small, non-chained, signed self-transfer per tier (**1×, 1.2×, 1.5×, 2×** of F1) **every 2 s** (was every 10 s), from its own wallets. That's 2 tx/s in total, from a pre-split pool of 600 coins per tier; a coin is reused only after its previous probe was accepted. 1.2× and 2× link back to the 25 Sep probes.
- **Probe n and what it buys (tightening 4).** We raise the rate, not the step length: longer steps would cost disk and time, while 2 tx/s of probes costs almost nothing.

| Samples per tier per 15-min step | Where from | 95% interval for p50 | for p95 | for p99 |
|---:|---|---|---|---|
| ~90 (old plan) | probes every 10 s | 41st–61st percentile | 91st percentile – max | not estimable (= max) |
| **~450** | probes every 2 s (1.2×, 2×) | 46th–55th | 93rd–97th | 98th percentile – max (reported, flagged) |
| **~2,250** | probes + box ordered stream (1×, 1.5×) | 48th–52nd | 94th–96th | 98.6th–99.4th |

  The intervals are exact order-statistic intervals for independent samples. Build's ordered stream (another ~1,800 per tier) is reported separately, because of its cross-machine clock.
  - **Not sure:** samples within one step share conditions and are not fully independent, so the real uncertainty is somewhat larger than the table. Lane samples (chained) are reported, but not pooled with the probes.
- Reported per step and tier: n, p50, p95, p99 and worst submit → first-acceptance time, and the share over 30 s and over 60 s (as counts and percentages).

## 6. Indexer and mempool

- **Indexer (api-tn10.kaspa.org):**
  - `GET /info/health?nc=<ms>` every 30 s (cache bypass), logging the HTTP status, `acceptedTxBlockTimeDiff`, `blueScoreDiff` and `isSynced`;
  - once a minute, one already-accepted probe transaction is polled with `GET /transactions/<txid>` every 5 s until it shows up (give up after 30 min). At most ~0.3 requests/s in total.
  - **Freeze rule:** 3 consecutive samples (90 s) with 503 or timeout, or a lag above 120 s and rising, or a visibility delay above 300 s. We report the step, the minutes into the step, our tx/s and network tx/s at that point, the freeze length and the recovery time.
  - A second public indexer is used only if we can confirm one exists beforehand.
- **Mempool:** n0 `mempoolSize` every 1 s and the fee estimate every 10 s. Optionally, a fee-band snapshot every 5 min while the mempool is under 50k.

### 6a. The box is not the chain (tightening 2)
- **Everything we send from the box goes through n0**, and all acceptance is read from n0. n0 is one node with our settings, so some limits we hit can be ours, not TN10's.
- **n0 as it runs** (read from the running process, Mon 5 Oct ~21:15 CEST): kaspad **2.1.0**, `--testnet --netsuffix=10 --ram-scale=0.1 --async-threads=4 --outpeers=6 --maxinpeers=24 --rpcmaxclients=64`, no UTXO index. The flags are logged again at T0.
- **Mempool cap:** in the rusty-kaspa source (`mining/src/mempool/config.rs`), the defaults are 1,000,000 transactions and 1,000,000,000 bytes, multiplied by `ram-scale` (at most 1.0). So n0's cap is **100,000 transactions / 100 MB**. **Claim (measured on TN10):** storm 2 peaked at 99,992 (`mempool_windows.csv`).
- **Logged every second:**
  - n0 process CPU (100% = one core, 800% = the whole box) and RSS;
  - box total CPU and load;
  - **each runner process's CPU** (a Node runner is mostly single-threaded, so ~100% = one core is its ceiling);
  - mempool size vs the 100,000 cap;
  - n0's own "evicted … in favor of incoming higher feerate transactions" counts (its 10-s log lines);
  - every submit reject, by the reason n0 gives.
- **Plateau labels** (per step, over the step's last 10 min, or from saturation onset if earlier):
  - **Box-bound** if any of:
    - (a) sender-limited: our submit-OK below 95% of target;
    - (b) any runner process at ≥ 95% of one core for ≥ 60 s;
    - (c) box total CPU ≥ 90% for ≥ 60 s (n0 shares the box with the runners);
    - (d) n0's mempool at ≥ 99,000 (99% of cap) for ≥ 60 s, or mempool-full rejects plus evictions above 1% of our submits;
    - (e) n0 unsynced, or its sink more than 10 s old, for ≥ 60 s.
  - **Network-bound** if none of (a)–(e) holds and either:
    - (f) blocks are ≥ 90% full by compute mass (from n0's log, as in storm 2); or
    - (g) network-wide unique accepted stays flat (within 5%) from one step to the next while our submit-OK rises.
  - **Unclear** otherwise, and reported as such.
  - **Not sure / open for debate:** these thresholds are our choice, fixed before T0. "Network-bound" means TN10 as it was that night, with our miners on it. Build sends through public nodes, so its path does not depend on n0's mempool cap; comparing its acceptance with the box's is a partial check.

## 7. Mining share

- For every block n0 adds, the coinbase payout script is compared with stp's mining addresses (box and desk miners). Logged per second and summarised per step: blocks total, blocks ours, **our share in %**.
- Our miners (box and desk) are **on in every phase except the miners-off control (§3b)** and its settle phase. Their state per phase is printed in the results. The desk miners count as "ours". Build's sender takes part as in §3a.
- **Mining share is published for every step** (blocks total, blocks ours, %), including the control step, where it should be ≈ 0%. Blocks per second and difficulty are published next to it.
- The old "optional extra max step with miners off" is dropped. The control is now part of the main run.

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
  - `mempool_1s.csv`, `indexer.jsonl`, `fee_estimates.jsonl`, `mining_share_per_step.csv`, and a per-step summary CSV;
  - `box_cpu_1s.csv` (n0, runners, box total), `n0_rejects_evictions.csv`, `plateau_labels.csv` (with the criteria that fired), `saturation_per_step.csv`, `clock_offsets.csv` (box and desk, start and end).
- Txids of the P2W lanes are published **after the lane coins have been swept**: those lanes are anyone-can-spend on TN10.
- **Charts** (PNG): submitted vs accepted per second and per step; confirmation time per step and tier (1× vs 1.5×); send vs accept order; mempool per second; indexer lag; mining share per step.
- No keys or recovery phrases, and no private paths.
- Each file stays under 50 MB.

## 9. Box limits (our setup, not protocol limits)

- One node (n0, kaspad 2.1.0, `--ram-scale=0.1`, mempool cap ~100k) on an 8-vCPU / 16 GB / 126 GB box.
- **Disk:** keep ~19 GB free for n0's pruning at all times. The morning pruning window (~07:15–08:30 CEST) needs 11–15 GB of temporary disk; a pruning disk-full crashed n0 on 3 Oct.
  - On 2 Oct, ~2.2k tx/s used ~4.7–5.0 GB/h. The loaded steps needed roughly 10–12 GB *(estimate)*. The miners-off control and the two settles add ~30 min at ≤ 250 tx/s, about 0.5 GB more, so **~10.5–12.5 GB** *(estimate)*. Probes at 2 tx/s are negligible. With ≥ 35 GB at T0 and ~19 GB kept for pruning, that leaves 16 GB, so it fits. (Free on Mon 5 Oct ~21:15 CEST: 44 GB.)
  - **Go only with ≥ 35 GB free at T0.** With 28–35 GB, steps shrink to 10 min (recorded as a deviation). Below 28 GB, no storm.
- **Guards** (unchanged): runner pause at ≤ 21 GB free; STOP below 19 GB for more than 900 s; immediate STOP at 10 GB or RAM < 1 GB; STOP if n0 is unsynced or more than 300 s behind. A guard stop ends the run early for both senders (box and Build) and is reported as such.

## 10. Later leg (idea, not planned yet)

**Proposal only.** This is not scheduled, not part of the plan above, and nothing here is promised.

First we finish this leg: one measured run, done in order, with the raw data and facts published.

After that, one idea is an open leg on TN10. Builders, core contributors and others would be invited to test their own apps under high congestion, for example covenants, dapps, vProgs such as tic-tac-toe, KaChat, dotK, Kasperolabs, and others. Each app would see how it behaves when blocks are full and fees rise, next to the same public measurements (accepted tx/s, confirmation time, order, mempool). Who takes part, when and how would be agreed openly first.

Kaspa Pulse has offered to cover this open builder testing leg as the independent side, if it happens.
