# TN10 storms: throughput, confirmation time, order, indexer and mempool — answers from our data

**Questions and guidance from Kaspa Pulse ([@gokugalax](https://x.com/gokugalax)). Thank you for the questions, and for the guidance on how to run and publish the next test. Both shaped the plan below. And thank you for the sequencing point: not just how many transactions land, but whether order holds under load. It is now a first-class metric. Thank you also for your pass on the plan and its four tightenings, now built in below. After the run we'll send you the results and go through them together.**
Analysis, charts and write-up by TN10 ops, stp's AI operator bot for his TN10 stack. Storm runs by stp's TN10 setup (TN10 ops on its own node, plus Build on stp's desk PC). Written Sun 4 Oct 2026, 23:00–23:59 CEST.

Kaspa **Testnet-10 (TN10) only**. All times are **CEST (UTC+2)**.

**Note:** deliberate load stays on TN10 by design, and mainnet comparisons and mainnet costing are out of scope, as Kaspa Pulse asked.

**Up front:** in our storms, our own miners made **50–63% of TN10 blocks** while they ran (storm 2 public report, `block_share_legs.csv`). Everything here describes **TN10 with our miners on it**, through one node on one small box.
Every number names the file it came from. The CSVs in [`data/`](data/) are small extracts of our raw logs. The scripts in [`scripts/`](scripts/) rebuild those CSVs and every chart. Where something was **not logged**, this README says so.

## Tasks for stp (before the storm)

1. **Hard go/no-go gate: the Grok Build dry run must pass. No storm until it does.** If it hasn't passed in time for Fri 9 Oct, the storm waits for 13 Oct.
   - **Settle Build's process setup first:** how many sender processes / PowerShell windows it runs **during the storm**. The count is fixed for the whole run (no auto-scaling), each process has its own coins, the miner count is fixed, and Build's runners hold 100% of target.
   - **Dry run from the desk:** Build sends a small ordered, fee-split stream (1× and 1.5×), compares 1 vs 2 vs 4 processes at its top planned share, then runs short steps at its planned targets with the chosen count. It passes when:
     - **at every step, achieved is ≥ 95% of target** (default margin; agree it before the plan lock). Last storm Build's runners did not run at 100% (stp's observation). Build logs achieved vs target every second, so any shortfall is visible;
     - its per-transaction logs are complete;
     - its txids match what n0 sees accepted;
     - it follows the UTC timetable.
   - Prompt: [`plan/GROK-BUILD-PROMPT.md`](plan/GROK-BUILD-PROMPT.md).
2. **Enough tKAS** in Build's wallet and on the box for the full schedule (amounts to confirm).
3. **Usage resets** for the bots and Build before the run.
4. **Box dry run passes** (plan checklist), and **≥ 35 GB free disk** at T0.
5. **Set Build's share** (default 25%, capped at what it held in its dry run), then **lock the plan by commit SHA** before T0.
6. **Desk clock and desk miners:** the desk clock is synced by NTP (offset logged at start and end), and stp switches the desk miners off and back on at the UTC times of the miners-off control step.
7. **Final OK on the start time:** Fri 9 Oct, 20:00 CEST at the earliest, otherwise 13 Oct.

## Contents
- [Tasks for stp (before the storm)](#tasks-for-stp-before-the-storm)
- [Next storm (early run Fri 9 Oct at the earliest; target 13 Oct if not ready)](#next-storm-early-run-fri-9-oct-at-the-earliest-target-13-oct-if-not-ready): What / Why / Method
- [Short plan list (for Kaspa Pulse)](#short-plan-list-for-kaspa-pulse)
- [Later leg (idea, not planned yet)](#later-leg-idea-not-planned-yet)
- [Prompt for Grok Build (`plan/GROK-BUILD-PROMPT.md`)](plan/GROK-BUILD-PROMPT.md)
- [Labels used in this README](#labels-used-in-this-readme)
- [Past storms: what our existing data shows](#past-storms-what-our-existing-data-shows)
  - [Short answer](#short-answer)
  - [Did our earlier storm repos already cover this?](#did-our-earlier-storm-repos-already-cover-this)
  - [Q1. Accepted vs submitted tx/s over the whole storm](#q1-accepted-vs-submitted-txs-over-the-whole-storm)
  - [Q2. Confirmation time per load step, normal fee vs 1.5×](#q2-confirmation-time-per-load-step-normal-fee-vs-15)
  - [Q3. Does the indexer freeze?](#q3-does-the-indexer-freeze)
  - [Q4. Mempool depth over time](#q4-mempool-depth-over-time)
  - [Q5. Send order vs accept order (sequencing)](#q5-send-order-vs-accept-order-sequencing)
  - [How the TPS was reached](#how-the-tps-was-reached)
- [Files](#files) · [Sources](#sources) · [Limits](#limits)

---

## Next storm (early run Fri 9 Oct at the earliest; target 13 Oct if not ready)

The early run is **no earlier than Fri 9 Oct, 20:00 CEST**. It waits on usage resets for the bots and Build, and on enough tKAS. If the 9th isn't ready, **13 Oct (evening CEST)** stays the target. The 6 Oct early run is **cancelled**. Either date uses the same plan, and only after the instrumentation passes its dry run. The full plan is in **[`plan/NEXT-STORM-PLAN.md`](plan/NEXT-STORM-PLAN.md)**.

**Who sends load.** Two participants, both measured:
- **TN10 ops** (stp's AI operator bot), on stp's box through its own node n0;
- **Grok Build**, on stp's desk PC through public TN10 nodes.

### What: Kaspa Pulse's four questions + sequencing are the measured goals

**Headline: not just how many transactions land, but whether order holds under load.**

| # | Question (Kaspa Pulse) | What we log (UTC) | What we chart / report |
|---|---|---|---|
| 1 | **Accepted tx/s vs submitted over the whole storm, and where acceptance flattens** | Per second: submitted, accepted and offered for the box and for Build, split by fee tier; **network-wide unique accepted** from n0's `virtual-chain-changed` notifications (this counts Build's and everyone's transactions); rejects by reason | Submitted vs accepted per second and per step; accepted vs step target (the flattening point); **saturation onset by a rule fixed before T0** (our accepted < 95% of our submitted for 60 s); each plateau labelled **box-bound, network-bound or unclear**; steps marked "sender-limited" where our own sender couldn't keep up |
| 2 | **Confirmation time at each load step (median and worst), normal fee vs 1.5×** | Per transaction: send sequence number, submit and accept times, fee tier. In every step, half the lanes (box and Build) pay **1×** the node's normal fee estimate and half pay **1.5×**, fixed for the step. Probes **every 2 s** at 1×, 1.2×, 1.5×, 2× | n and p50 / p95 / p99 / worst per step and tier, with 95% intervals: ~450 samples per tier per step, ~2,250 for 1× and 1.5× (probes plus ordered stream); share over 30 s and 60 s; send order vs accept order |
| 3 | **Does the indexer freeze, at what sustained tps, and for how long** | api-tn10 `/info/health` every 30 s (cache bypass); once a minute, the time until one of our accepted transactions shows up there | For every freeze: step, minutes into the step, sustained tx/s (ours and network-wide) at that point, length, recovery time |
| 4 | **Mempool depth over time** | n0 mempool size every second; fee estimate every 10 s | Mempool per second against the steps, so the backlog is visible, not just throughput |
| 5 | **Send order vs accept order: does order hold under load?** (Kaspa Pulse's sequencing point) | Per transaction: a send sequence number per sender (box runners, Build, probes), UTC submit time, and the accept position on n0 (event index + position in the event). Plus a **dapp-like ordered stream**: independent (not chained) transactions sent in sequence, 2 per second per tier, at 1× and 1.5× | Per step and tier: **reorder rate** (share of same-sender pairs sent ≥ 1 s apart that were accepted in reverse order), **out-of-order accepts** (accepted before an earlier-sent transaction of the same sender and tier), **stalls** (a transaction still unaccepted 30 s after a later-sent one of the same sender and tier landed; count and longest). Same-event ties are reported separately. Fee-driven overtakes (1.5× passing an earlier 1×) are reported separately from reorders within a tier. **All as counts and percentages, with n and a 95% interval.** Plus the **miners-off control** vs the same step with miners on |

The 1× vs 1.5× fee comparison is the one Kaspa Pulse finds most interesting: does paying more buy inclusion under load? The other headline is order: does paying 1.5× also keep transactions in order when the 1× tier starts to reorder or stall?

### Why
The October storm answered these questions only partly (see Q1–Q5 below):
- submitted vs accepted came from a closed-loop sender, with no network-wide unique count;
- confirmation time was cumulative, at one fee per runner;
- indexer freezes were seen but never tied to a held load;
- send vs accept order was seen only coarsely (probes 30 s apart, Q5) and never across senders or per step;
- Build's desk load was logged only as submit-OK;
- our own miners (50–63% of blocks) and our own node's limits could not be separated from the chain.

The next storm is built to answer all five directly, with both senders counted, our miners switched off for one control step, and box limits logged separately from chain limits.

### Method: Kaspa Pulse's six process points

| # | Guidance | In the plan |
|---|---|---|
| 1 | Write the plan down before the run and publish it with the results | Public now, locked by commit SHA before T0. The results cite the SHA and list any deviations (plan §1) |
| 2 | Baseline first | **B0: 10 min of normal TN10 traffic**, with both our senders off and all measurements on. B1: 10 min after the load (plan §2) |
| 3 | Fixed steps instead of one blast | **2×, 5×, 10×, 20×, 30× the measured baseline**, then max, plus a **2× miners-off control** right after the 2× step. 15 min at a fixed target plus 5 min of drain, also shown in absolute tx/s; 2 h 55 min in total. Box and Build follow the same UTC timetable. Fallback: absolute steps of 500–3,000 tx/s if the baseline is below 50 or above 200 tx/s (plan §3) |
| 4 | Log submitted and accepted per second, UTC; send order vs accept order | Per-second UTC counters for the box, Build and the whole network. Per-transaction send sequence numbers and acceptance positions, giving reorder rate, out-of-order accepts and stalls per step (plan §4) |
| 5 | State mining share up front | **~50–63% in earlier storms.** The exact share for this run is measured and **published for every step**, including the miners-off control (≈ 0%). The results describe **TN10 with our miners and Build on it** (plan §7) |
| 6 | Publish raw data next to the summary | Per-second CSV, per-step summary, every probe, per-transaction samples (box and Build), mempool, indexer and mining-share files in `data/` (plan §8) |

#### Method: Kaspa Pulse's four tightenings (from his review, before the lock)
1. **Miners-off control, in the main run.** One fixed step with all our miners off (box and desk), right after the 2× step and at the **same load**, so the two can be compared. The control asks: is it the network that reorders, or our own block templates?
   - **Claim (measured on TN10):** last storm, with our box miners off, our inclusion fell to ~300 tx/s while n0's mempool backed up (median 71,498). So the control runs at the 2× target (≈ 200 tx/s total if the baseline is ~100), and never above 250 tx/s total.
   - If it saturates anyway, it is flagged backlog-bound and not used as a control.
   - **Not sure / open for debate:** this is an imperfect control. Other miners' templates and hashrate can change too, and TN10's block rate drops until difficulty adjusts. We log both and report them next to the result.
2. **The box is not the chain.**
   - Everything from the box goes through n0: kaspad 2.1.0, `--ram-scale=0.1`, `--async-threads=4`, `--outpeers=6`, `--maxinpeers=24`, `--rpcmaxclients=64`, no UTXO index (read from the running process). Its mempool cap is 100,000 transactions / 100 MB (rusty-kaspa source).
   - We log n0's CPU, mempool-cap hits, evictions and reject reasons, plus each runner's CPU, every second.
   - Each plateau is labelled **box-bound**, **network-bound** or **unclear** by criteria fixed before T0 (plan §6a).
3. **Synced clocks.** The box and desk offsets against NTP are logged at start and end; the box offset was −8 to −9 ms on Mon 5 Oct. Box-only confirmation times use one clock. Build's cross-machine times are corrected for the offset, or flagged if it is missing or drifted.
4. **Saturation and sample size, defined before T0.**
   - **Saturated** = our accepted < 95% of our submitted, over a rolling 60-s window, for 60 consecutive seconds (exact rule in plan §3c).
   - Reorder rates are given as **counts and percentages** with n and a 95% interval.
   - Probes go from every 10 s to **every 2 s**: ~450 per tier per step instead of ~90. For 1× and 1.5×, the ordered stream adds ~1,800, for ~2,250. That narrows the 95% interval on p95 from "91st percentile to the max" to the 94th–96th, and makes p99 estimable for 1× and 1.5× (plan §5).

#### Method: how Build takes part
- Build sends from the desk through public TN10 nodes, alongside the box runners, on the **same UTC step timetable**. In B0 and B1 it is off. Its instructions: [`plan/GROK-BUILD-PROMPT.md`](plan/GROK-BUILD-PROMPT.md).
- **Steady rate:** last storm Build's runners did not run at 100% (stp's observation). This time they must hold the step target for the whole step, and Build logs achieved vs target send rate every second.
- **Process setup:** a fixed number of sender processes for the whole storm (no auto-scaling or fleet restarts). Each process has its own coins and log files, merged by UTC. A separate process runs the ordered stream. The count is picked in the dry run (1 vs 2 vs 4).
- **Go/no-go gate:** no storm until Build's dry run passes (achieved ≥ 95% of target at each step, logs complete, txids matched, UTC timetable followed). If it fails, the storm waits for 13 Oct.
- **Per-step target:** a fixed share of each step's added load, written into the locked plan before T0 (default 25%, capped at what its sender sustains in a pre-run test). The box sends the rest. Both actual rates are measured, not assumed.
- **Fees:** Build uses the same two tiers, 1× and 1.5× of its node's normal fee estimate, split across its lanes and fixed per step. If its sender can't split, its single fee is logged and its transactions are left out of the 1× vs 1.5× comparison.
- **Logging:** Build logs per second (UTC) target and achieved send rate, submit-OK and rejects by reason, plus per transaction the txid, a send sequence number, its UTC submit time and its fee tier. The desk clock's offset from UTC is recorded at T0.
- **Acceptance:** Build's transactions are matched by txid against the transactions n0 sees accepted on the chain. n0 sees every accepted transaction, whichever node it was sent to, so Build's accepted count and confirmation times are measured on the same clock as the box's. They also count in the network-wide unique total.

### Box limits
- **Runners:** 6 runners × 4 connections on the box, a 7th only at max, never 8.
- **Disk:** keep ~19 GB free for n0's pruning.
  - Go only with ≥ 35 GB free at T0. With 28–35 GB, steps shrink to 10 min. Below 28 GB, no storm.
  - The schedule (2 h 55 min, including the miners-off control) should need ~10.5–12.5 GB *(estimate)*, which fits within ≥ 35 GB free at T0 minus the ~19 GB pruning reserve. Step targets are the combined load of box and Build, so the estimate already covers Build's transactions. The run starts no earlier than 20:00 CEST (T0 ≈ 20:15 CEST, after the evening pruning slowdown), well away from the morning pruning window.
- **Guards:** unchanged; a guard stop ends the run early (box and Build both stop) and is reported.

## Short plan list (for Kaspa Pulse)

Next TN10 storm: early run no earlier than Fri 9 Oct, 20:00 CEST (waiting on usage resets for the bots and Build, and enough tKAS). If the 9th isn't ready, 13 Oct stays the target. The 6 Oct early run is cancelled. Go/no-go: the storm runs only after Build's dry run passes (it holds its target rate, logs complete, txids matched); otherwise it waits for 13 Oct. The load comes from two places, and both are measured:
- **TN10 ops**: stp's AI operator bot, sending from stp's box through his own TN10 node (n0).
- **Grok Build**: sending from stp's desk PC through public TN10 nodes.

The load stays on TN10 by design. No mainnet comparisons or costing.

**Headline: not just how many transactions land, but whether order holds under load.**

**What we'll measure (your four questions + sequencing)**
1. **Accepted vs submitted tx/s over the whole storm, and where acceptance flattens.**
   - Logged per second in UTC: submitted and accepted for the box, submitted and accepted for Build, and network-wide unique accepted. That last one counts Build's transactions and everyone else's.
   - Charted per step.
2. **Confirmation time at each load step (median and worst), normal fee vs 1.5×.**
   - In every step, half of our lanes (box and Build) pay 1× the node's normal fee estimate and half pay 1.5×, fixed for the step.
   - Probe transactions every 2 s at 1×, 1.2×, 1.5× and 2×: ~450 per tier per step, ~2,250 for 1× and 1.5× with the ordered stream.
   - We report n, p50, p95, p99 and worst per step and tier, with 95% intervals.
3. **Does the indexer freeze, at what sustained tps, for how long.**
   - api-tn10 health every 30 s, plus the time until it shows one of our transactions, checked every minute.
   - For each freeze: start, length, recovery, and the sustained tx/s at that point.
4. **Mempool depth over time.**
   - n0's mempool every second, charted against the steps.
5. **Send order vs accept order (your sequencing point).**
   - Every transaction gets a send sequence number. Its accept position is read from the node.
   - Per step and fee tier we report:
     - the reorder rate;
     - out-of-order accepts;
     - stalls (a transaction stuck while later ones from the same sender land).
   - A dapp-like ordered stream of independent transactions at 1× and 1.5× shows whether order would hold for an app that expects it.

**Method (your six points)**
1. **Plan:** published before the run, locked by commit SHA, and that SHA is cited in the results.
2. **Baseline:** 10 min of normal TN10 traffic first, with our senders off and the same measurements. Another 10 min after the load.
3. **Fixed steps:** 2×, 5×, 10×, 20× and 30× the measured baseline, then max.
   - 15 min per step plus 5 min of drain, plus a 2× step with all our miners off. 2 h 55 min in total.
   - Each step is also given in absolute tx/s (the baseline was ≈ 100 tx/s before our last storm).
   - Box and Build follow the same UTC timetable.
4. **Logs:** per second in UTC, plus a send sequence number and accept position for each transaction.
5. **Mining share, up front:** our miners made ~50–63% of TN10 blocks in earlier storms. We'll publish the exact share for every step, including the miners-off control. The results describe TN10 with our miners and Build on it.
6. **Raw data:** CSV/JSONL published next to the charts.

**Your four tightenings (now in the plan, before the lock)**
1. **Miners-off control in the main run.** One 2× step with all our miners off, right after the same 2× step with them on, at the same low load. With our miners off last time, our inclusion was only ~300 tx/s, so the control stays under 250 tx/s total and measures order, not backlog.
   - This shows whether reordering comes from the network or from our own block templates.
   - It's an imperfect control: other miners' templates and hashrate change too.
   - Mining share is published for every step.
2. **Box vs chain.**
   - Everything from the box goes through n0: kaspad 2.1.0, `--ram-scale=0.1` (mempool cap 100,000 tx), `--async-threads=4`, `--outpeers=6`, `--maxinpeers=24`, `--rpcmaxclients=64`.
   - We log n0's CPU, mempool-cap hits, evictions and reject reasons, plus the runners' CPU.
   - Each plateau is labelled box-bound, network-bound or unclear, by stated criteria.
3. **Clocks.** NTP offset on the box and the desk, logged at start and end. Cross-machine confirmation times are corrected for it, or flagged.
4. **Saturation and sample size.**
   - **Saturated** = our accepted below 95% of our submitted, for 60 s (rolling 60-s window), with the exact rule fixed before T0.
   - Reorder rates are given as counts and percentages, with n and a 95% interval.
   - Probes go from every 10 s to every 2 s: ~450 per tier per step, ~2,250 for 1× and 1.5× with the ordered stream. The p95 interval narrows to about the 94th–96th percentile.

Thank you for the pass on the plan. After the run we'll send you the results and go through them together.

Full plan: [`plan/NEXT-STORM-PLAN.md`](plan/NEXT-STORM-PLAN.md)

## Later leg (idea, not planned yet)

**Proposal only.** This is not scheduled, not part of the plan above, and nothing here is promised.

First we finish this leg: one measured run, done in order, with the raw data and facts published.

After that, one idea is an open leg on TN10. Builders, core contributors and others would be invited to test their own apps under high congestion, for example covenants, dapps, vProgs such as tic-tac-toe, KaChat, dotK, Kasperolabs, and others. Each app would see how it behaves when blocks are full and fees rise, next to the same public measurements (accepted tx/s, confirmation time, order, mempool). Who takes part, when and how would be agreed openly first.

Kaspa Pulse has offered to cover this open builder testing leg as the independent side, if it happens.

---

## Labels used in this README

| Label | Meaning |
|---|---|
| **Claim (measured on TN10)** | We measured it on TN10. The number and its source file are given. It holds for the conditions stated. |
| **Not sure / open for debate** | Reasonable, but we're not sure. The reason it might be wrong or might not carry over is given. |
| **Needs more testing** | We don't know. The test that would settle it is named. |

## Past storms: what our existing data shows

The sections below answer the same questions from the 25 Sep storm (storm 1) and the 1–3 Oct storm (storm 2), using only data we already had. They are why the plan above looks the way it does.

## Short answer

| # | Question | Status | In one line |
|---|---|---|---|
| 1 | Accepted vs submitted tx/s, where acceptance flattens | **Partly answered** | Logged per runner every 10 s. Our box's acceptance flattened at about **2,200–2,600 tx/s** (median per minute) once the runners were allowed more than ~3,000–4,000 tx/s. Best minute **4,253 tx/s**. Accepted stayed within 1% of submitted, because our sender throttles itself. What's missing is an open-loop offered rate and the other senders' submissions. |
| 2 | Confirmation time per load step, median and worst, 1× vs 1.5× fee | **Partly answered** | Measured per fee tier on 25 Sep at two load levels (1×, 1.2×, 2×, 5×, 10×, 100× the floor). **1.5× was not tested.** At ~6.5k "Processed" tx/s: 1× p50 **7.0 s** / max **105 s**; 2× p50 **3.1 s** / max **48 s**. The October storm logged latency at one fee per runner, with no A/B split. |
| 3 | Does the indexer freeze, at what tps, for how long | **Partly answered** | Yes. api-tn10 froze for **86 min** (Fri 2 Oct 22:01–23:27, lag up to **4,311 s**, HTTP 503) while our box sent **~2,435 tx/s** and n0 "Processed" **~6,546 tx/s**. Shorter stalls happened at lower loads. On 25 Sep it froze for **at least 3 d 15 h**. We have no load threshold and no cause. |
| 4 | Mempool depth over time | **Answered** | Sampled every 15 s for the whole storm. Peak **99,992** (Fri 2 Oct 01:35:47). A ~71k backlog sat for ~6 hours after our miners stopped. **486,140** evictions in L1. |
| 5 | Send order vs accept order: does order hold under load? | **Partly answered (coarse)** | From the 25 Sep fee probes, sent 30 s apart: at 1× and 1.2× the floor (at or below the storm's fee) **2.6–10.4%** of consecutive probes were accepted out of send order, and some waited behind later probes for up to **169 s**. At 2× the floor and above: at most 1 reversal in 116 pairs (step A), none in step B. The October storm did not log order. |

Kaspa Pulse is most interested in the 1× vs 1.5× fee question. The nearest thing we have is a 25 Sep probe at 1.2× (equal to the storm's own fee) and 2× (1.67× the storm's fee). Paying 1.67× the crowd's fee cut the median wait from **7.1 s to 3.1 s** and the worst case from **92 s to 48 s** ([Q2](#q2-confirmation-time-per-load-step-normal-fee-vs-15)). A real 1× vs 1.5× A/B split at each load step is the main item in the [next storm plan](#next-storm-early-run-fri-9-oct-at-the-earliest-target-13-oct-if-not-ready).

## Did our earlier storm repos already cover this?

"Storm 1" is the 25–26 Sep run. "Storm 2" is the 1–3 Oct run. "Build" is the Grok Build agent on stp's desk PC.

| Question | Storm 1 repos ([round1-public](https://github.com/STP-KAS/grok-bot-vprogs-round1-public), [round2](https://github.com/STP-KAS/grok-bot-vprogs-round2)) | Storm 2 ([public report](https://github.com/STP-KAS/tn10-storm-2026-10-public-report)) | Build ([build opinion](https://github.com/STP-KAS/tn10-vprogs-build-opinion), desk logs read in the public report) |
|---|---|---|---|
| 1. Accepted vs submitted | Network "Processed" tx/s and supervisor totals. No submitted vs accepted series over time | Leg totals and peaks (submitted 59,137,819 / included 58,905,910), and a 5-min included tx/s series (`data/box_5min.csv`). **No submitted vs accepted over time, no flattening view, no charts** | The desk sender logged **submit-OK**, not inclusion. Its local P2W meter counted virtual-chain inclusions, peak 2,795.6/min. No submitted vs accepted series |
| 2. Confirmation time by fee | **Yes, fee-tier probes** (1×–100×, 117 per tier), [`findings/overload-30m-summary.md`](https://github.com/STP-KAS/grok-bot-vprogs-round1-public/blob/main/findings/overload-30m-summary.md). First 57.5 min only. No 1.5× tier | Not covered | Not covered |
| 3. Indexer freeze | Not in these repos (the 25 Sep freeze is in a private working note, summarised in the storm 2 public repo) | **Yes**: stall windows, durations, box tps and n0 tps in each window (`data/api_windows_vs_load.csv`) | The build opinion notes the public health document stayed frozen. No timings of its own |
| 4. Mempool depth | Per-10-min medians/maxima in the overload summary | Per-window medians/p95/max and evictions (`data/mempool_windows.csv`). **No over-time chart** | Not covered |

So the pieces were mostly there, spread over several repos. This repo pulls them into one place, adds per-minute series and charts, and the second load step of the 25 Sep fee probes (22:47–23:50), which no earlier write-up had in full.

---

## Q1. Accepted vs submitted tx/s over the whole storm

**Status: partly answered.**

![Submitted vs accepted per minute](charts/1-submitted-vs-accepted-over-time.png)

![Where acceptance flattens](charts/1b-acceptance-flattening.png)

**What was logged.** Each box runner printed a report line every 10 s (`stress-tests/data/runner1-4.out`, `p2w1-8.out`) with cumulative counters:
- `submitted`: transactions the node accepted into its mempool (submit OK).
- `accepted`: our transactions whose id then appeared in n0's `virtual-chain-changed` notification, i.e. accepted by the selected chain. The engine code is `r5-engine.mjs` (class `Engine`).
- `rate`: the most that runner was allowed to send at that moment (its token-bucket cap).

[`scripts/extract.py`](scripts/extract.py) splits each runner's log into segments at restarts, spreads each 10-s increment evenly over its seconds and sums all runners per minute → [`data/oct_box_submitted_vs_accepted_1min.csv`](data/oct_box_submitted_vs_accepted_1min.csv) (1,801 minutes, Thu 1 Oct 20:00 → Sat 3 Oct 02:00). Check: the per-minute file sums to 59,149,806 submitted and 58,917,966 accepted. That matches the leg totals in [`data/oct_legs_from_public_report.csv`](data/oct_legs_from_public_report.csv) (59,137,819 / 58,905,910), except for a ~12k-tx smoke run before L1 (12,019 txs, Thu 20:14–20:16).

**What it shows**
- **Claim (measured on TN10):** **accepted tracked submitted closely in every leg**: L1 99.61%, L2 99.39%, L3 99.15%, L4 99.98% (`data/oct_legs_from_public_report.csv`). A transaction counts as "not accepted" when the runner that sent it never saw it on the chain. That includes transactions still in flight when a runner restarted, so the gap is not a count of dropped transactions.
- **Claim (measured on TN10):** **acceptance flattens.** Grouped by the runners' combined rate cap, minutes with no runner paused:

  | Rate cap (tx/s) | Minutes | Submitted, median | Accepted, median | Accepted, best minute | Mempool, median |
  |---|---:|---:|---:|---:|---:|
  | 0–999 | 311 | 297 | 297 | 1,244 | 71,528 |
  | 1,000–1,999 | 64 | 1,416 | 1,436 | 2,513 | 24,216 |
  | 2,000–2,999 | 76 | 2,017 | 2,031 | 2,988 | 19,040 |
  | 3,000–3,999 | 66 | 2,461 | 2,430 | 3,597 | 15,864 |
  | 4,000–4,999 | 52 | 2,492 | 2,559 | 4,227 | 3,191 |
  | 5,000–5,999 | 11 | 2,010 | 1,810 | 3,303 | 2,776 |
  | 6,000–6,999 | 23 | 2,266 | 2,269 | 3,518 | 3,445 |
  | 7,000–7,999 | 18 | 2,157 | 2,302 | 3,110 | 1,465 |
  | 8,000–8,999 | 21 | 2,227 | 2,235 | 3,063 | 2,811 |
  | 9,000–9,999 | 66 | 2,185 | 2,183 | 3,222 | 2,138 |

  (Computed from `data/oct_box_submitted_vs_accepted_1min.csv`. The 0–999 row is mostly the L1 night after our miners stopped, at ~300 tx/s with a ~71k backlog.) Up to a cap of about 3,000 tx/s, accepted rises with the cap. Above that, the median stays at about **2,200–2,600 tx/s**, however high the cap goes.
- **Claim (measured on TN10):** the knee test on Fri 2 Oct (L3): **6 runners 2,410 tx/s, 7 runners 2,383, 8 runners collapsed to 1,165**. At 8 runners the mempool went from 14k to 79k in 75 s and blocks were full by mass at 492k (public report README, L3 row; `build-brief-how-box-storm-works-2026-10-02.md` §7).
- **Claim (measured on TN10):** the best clock-aligned minute in our file is **4,227 accepted tx/s** (Fri 2 Oct 01:25). The best sliding 60 s is **4,252.8** (from 01:24:46), best 5 min **3,843**, best hour **2,517.6** (L4, from 21:57:12) (`data/oct_legs_from_public_report.csv`). Those peaks came with 7 runners, a 30× fee burst and our own miners making ~60% of blocks (see [How the TPS was reached](#how-the-tps-was-reached)).

**Why "partly":**
- **Submitted is not an open-loop offered rate.** A runner lane waits for each submit reply before building its next transaction, and runners pause themselves when the mempool is deep (>75k in the engine; storm-watch pauses everything at >80k). So when blocks are full, our sender slows down. The flattening shows up as **submit rate flattening** with acceptance following it, not as a growing gap between submitted and accepted. The rate cap is the best proxy for "offered" that we have.
- **Only our box's transactions.** The desk sender (Grok Build) logged submit-OK only. Other TN10 senders are unknown. n0's "Processed" counter (purple line) counts a transaction once for every block body that carries it, so it overstates unique transactions. On TN10 it ran about 1/3 high (round 7). Unique network-wide accepted tx/s per minute was not logged.
- **No stepped schedule.** The rate cap moved with the scaler, fee and guards, not in clean steps.

## Q2. Confirmation time per load step, normal fee vs 1.5×

**Status: partly answered.** "Confirmation" here means **submit → first acceptance on n0's selected chain** (not a depth of N blocks).

![Confirmation time by fee tier](charts/2-confirmation-time-by-fee-tier.png)

![Fee-tier probes over time](charts/2b-fee-tier-probes-over-time.png)

**What we have: fee-tier probes, 25 Sep 2026 (storm 1).** A probe script (`scripts/overload-probe.mjs` in [round1-public](https://github.com/STP-KAS/grok-bot-vprogs-round1-public)) sent one small self-transfer (mass 1,690) per fee tier every 30 s, and polled for its id among the chain's accepted transactions every 1 s. Fee tiers were multiples of the node's minimum relay feerate of 100 sompi/gram. Raw file: `tn10-break-test-2026-09-25/logs/overload/probes.jsonl` → [`data/sep_fee_tier_probes.csv`](data/sep_fee_tier_probes.csv) (one row per probe) and [`data/sep_fee_tier_summary.csv`](data/sep_fee_tier_summary.csv).

Two load levels ran back to back with the same probes. That gives two "load steps", though not a designed stepped schedule:

**Step A: 21:48:41–22:46:14.** The storm paid 120 sompi/g (1.2×). n0 "Processed" ~6,460 tx/s average ([`data/sep_network_processed_tx_s_1min.csv`](data/sep_network_processed_tx_s_1min.csv)). Mempool median ~63k, max 99,662.

| Tier | Feerate | vs storm fee | Probes | p50 | p90 | Worst | > 30 s |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1× | 100 | 0.83× | 117 | **7.0 s** | 29.8 s | **105 s** | 11 |
| 1.2× | 120 | 1.00× | 117 | **7.1 s** | 21.8 s | **92 s** | 6 |
| 2× | 200 | 1.67× | 117 | **3.1 s** | 9.5 s | **48 s** | 2 |
| 5× | 500 | 4.17× | 117 | 1.35 s | 2.3 s | 39 s | 1 |
| 10× | 1,000 | 8.33× | 117 | 1.2 s | 1.7 s | 3.7 s | 0 |
| 100× | 10,000 | 83× | 117 | 1.2 s | 1.7 s | 3.7 s | 0 |

**Step B: 22:47:26–23:50:41.** The storm paid 200 sompi/g (2×). n0 "Processed" ~7,420 tx/s average (this includes the stop at the end). Mempool median ~53k, max 80,781.

| Tier | Feerate | vs storm fee | Probes | p50 | p90 | Worst | > 30 s |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1× | 100 | 0.50× | 126 | **11.4 s** | 47.2 s | **208 s** | 28 |
| 1.2× | 120 | 0.60× | 126 | 9.5 s | 35.1 s | 93 s | 16 |
| 2× | 200 | 1.00× | 126 | **4.6 s** | 10.7 s | **29 s** | 0 |
| 5× | 500 | 2.50× | 126 | **1.8 s** | 2.8 s | **4.5 s** | 0 |
| 10× | 1,000 | 5.00× | 126 | 1.2 s | 1.8 s | 2.5 s | 0 |
| 100× | 10,000 | 50× | 126 | 1.2 s | 1.7 s | 2.1 s | 0 |

All 1,458 probes in the two steps were accepted. None was rejected or lost.

- **Claim (measured on TN10):** under load, **paying more bought faster inclusion**. Paying the same as the crowd gave a median of 4.6–7.1 s and a worst case of 29–92 s. Paying 1.67× the crowd (step A, 2× tier) roughly halved both. Paying 2.5× or more gave ~1–2 s medians and a worst case under 5 s (step B). 100× bought nothing over 10×.
- **Claim (measured on TN10):** **cheap transactions got worse when the load went up**. The 1× tier's median went from 7.0 s to 11.4 s and its worst case from 105 s to 208 s, as the storm's own fee moved further above it.
- **Not sure / open for debate:** whether **1.5×** behaves like our 1.2× or our 2× tier. It was not tested. 1.5× is between them, and our probes used the node's floor as "1×", not the node's "normal" estimate.
- **Not sure / open for debate:** these probes ran on one node with `--ram-scale=0.1` (mempool cap ~100k), under our own flood, with our miners making a large share of blocks, and with Grok Build's desk traffic possibly mixed in (round2 README, "Confounder").

**What the October storm logged.** The runners' `lat_p50` / `lat_p95` are **percentiles over every transaction that process saw accepted since it started**, not per 10-s interval (`r5-engine.mjs`, `pstats()` sorts the whole `lat` array). And each runner paid **one fee at a time**, so there was no 1× vs 1.5× split. The end-of-segment values are in [`data/oct_runner_latency_cumulative_by_segment.csv`](data/oct_runner_latency_cumulative_by_segment.csv), for example:
- L4 (Fri 21:57 → Sat 01:06, 200 sompi/g, ~2.5M txs per runner): p50 **6.0–7.1 s**, p95 **12.4–13.6 s**.
- L3 (Fri 11:52 → 16:50, 200–392 sompi/g, the six main runners): p50 **8.1–10.4 s**, p95 **16.4–20.7 s**.
- L1 night after our miners stopped (Fri 01:10 → 07:53; fee 6,000 → 200): p50 **~5 s** and p95 **893–953 s** for 6 of the 7 runners. The seventh shows p50 1.7 s / p95 101 s.

**Not logged in October: confirmation time per load step, and confirmation time by fee level.** We say this plainly. The next storm plan fixes both.

## Q3. Does the indexer freeze?

**Status: partly answered.** "Indexer" here is the public TN10 REST API **api-tn10.kaspa.org** (a kaspa-rest-server with its own database). It is not our node. We have no access to its logs.

![Indexer freeze windows vs tps](charts/3-indexer-freeze-windows-vs-tps.png)

**What was logged.** Every 120 s, `GET /info/health` → HTTP status and `acceptedTxBlockTimeDiff` (seconds the indexer's newest accepted transaction lags behind) (`stress-tests/data/api-health-min.jsonl` → [`data/oct_api_tn10_health_2min.csv`](data/oct_api_tn10_health_2min.csv), with our box's accepted tx/s and n0 "Processed" tx/s for the same minute). Stall windows come from the storm 2 public report: [`data/oct_api_tn10_stall_windows.csv`](data/oct_api_tn10_stall_windows.csv).

**Freezes and stalls, 1–3 Oct** (box tps and n0 tps are the averages inside each window):

| Window (CEST) | Length | What happened | Box accepted tx/s | n0 "Processed" tx/s | Back to normal |
|---|---:|---|---:|---:|---|
| Thu 22:29–23:31 | 62 min | lagging, not frozen: lag rose and fell between 137 and 704 s, intermittent 503 | 1,477 | 3,591 | Thu 23:33 |
| Thu 23:03–23:29 | 26 min | continuous 503 (inside the window above) | 951 | 2,705 | Thu 23:33 |
| Thu 23:53–Fri 00:09 | 16 min | stall + 503 again (our sampler then stopped for 51 min) | 2,421 | 4,217 | Fri 01:00 (our sampler was off 00:09–01:00) |
| Fri 01:22–01:30 | 8 min | 503 with slow (18 s) replies, then stall, during the 30× fee burst | 2,161 | 5,427 | Fri 01:32 |
| Fri 09:55–09:57 | 2 min | stall right after the L2 peak | 1,645 | 4,948 | Fri 09:59 |
| Fri 12:25–12:47 | 22 min | two 503s + intermittent stall, lag 22–170 s | 2,005 | 5,340 | Fri 12:49 |
| **Fri 22:01–23:27** | **86 min** | **full freeze**: 503 on every sample from 22:09 to 23:27; lag grew ~120 s per 120-s sample, max **4,311 s** at 23:21:49 | **2,435** | **6,546** | **Fri 23:29** |

- **Claim (measured on TN10):** **yes, it froze.** The longest freeze in the October storm was 86 minutes, while our box held ~2,435 accepted tx/s (best 5-min bin 3,238 at 23:15) and n0 "Processed" ~6,546 tx/s. Whenever our sampler was running, health came back within 2–4 minutes of the last bad sample.
- **Claim (measured on TN10):** **the chance of a bad health sample rose with n0's load** ([`data/oct_api_bad_samples_by_n0_processed_tps.csv`](data/oct_api_bad_samples_by_n0_processed_tps.csv)):

  | n0 "Processed" tx/s | Samples | Bad (non-200, timeout, or lag > 120 s) |
  |---|---:|---:|
  | 0–999 | 468 | 11% |
  | 1,000–2,999 | 138 | 10% |
  | 3,000–3,999 | 66 | 20% |
  | 4,000–4,999 | 63 | 38% |
  | 5,000–5,999 | 39 | 67% |
  | 6,000–6,999 | 28 | 79% |
  | 7,000+ | 15 | 100% |

  Samples inside one long freeze are not independent, and most 7,000+ minutes were inside the L4 freeze. Treat this as an association, not a threshold.
- **Claim (measured on TN10), storm 1:** on 25 Sep the indexer's accepted-transaction pointer froze at **21:55:38 CEST**, while our storm ran at about 6k "Processed" tx/s. It was still frozen (HTTP 503, lag 313,244 s ≈ 3 d 15 h) when we checked on 29 Sep at 12:56 CEST. We don't know when it recovered. Block ingestion kept going; only accepted-transaction processing was stuck. The earliest healthy sample we have after that is 1 Oct 18:27:39 CEST. (Our private working note on that freeze, summarised in the [storm 2 public report, §4](https://github.com/STP-KAS/tn10-storm-2026-10-public-report#4-public-api-api-tn10kaspaorg).)
- **Not sure / open for debate:** **cause.** Time correlation is not causation. The indexer is someone else's service. We don't know its hardware, its other users, or whether our own API calls mattered.
- **Needs more testing:** **"at what sustained tps does it freeze?"** We never held a fixed load long enough while watching it, and other stalls happened at loads where it was fine at other times. A stepped run with a 30-s health probe and a "can the indexer see my transaction yet" probe would settle it (see the plan).
- **Our own node did not freeze.** n0 stayed synced; sink age max 3.1 s in L1 (public report).

## Q4. Mempool depth over time

**Status: answered.**

![Mempool depth per minute](charts/4-mempool-depth-over-time.png)

**What was logged.** n0's `mempoolSize` every 15 s (`stress-tests/data/host.jsonl`). Storm-watch pause flags every 15 s (`stress-tests/data/storm-watch.jsonl`). Both are per minute (min / median / max) in [`data/oct_box_submitted_vs_accepted_1min.csv`](data/oct_box_submitted_vs_accepted_1min.csv). Per-window statistics and evictions from the storm 2 public report are in [`data/oct_mempool_windows_from_public_report.csv`](data/oct_mempool_windows_from_public_report.csv).

| Window | Median | p95 | Max | Evicted for higher feerate |
|---|---:|---:|---:|---:|
| L1, box miners on | 3,038 | 73,359 | 99,803 | 59,081 |
| L1, 30× fee burst Fri 01:10–01:30 | 64,992 | 75,560 | 77,480 | 0 |
| L1 night, box miners off | 71,498 | 84,142 | **99,992** | **427,059** |
| L2 | 2,176 | 59,180 | 96,293 | 0 |
| L3 loaded | 4,448 | 42,153 | 76,461 | 0 |
| L4 loaded | 17,140 | 25,993 | 30,826 | 0 |

- **Claim (measured on TN10):** peak **99,992** at Fri 2 Oct 01:35:47, just under n0's ~100k cap (`--ram-scale=0.1`). Storm-watch flagged a ">80k" pause in 50 of the 1,801 minutes.
- **Claim (measured on TN10):** **the backlog is the main story of the L1 night.** After our miners stopped at 01:31:50, a ~71k mempool sat for about six hours (02:00–07:30) while our inclusion fell to ~300 tx/s and blocks were only 11–26% full. Over that night n0 evicted 427,059 low-feerate transactions to make room for higher-feerate ones. L1 as a whole had **486,140** evictions.
- **Claim (measured on TN10):** in L4, at our highest sustained box rate (best hour 2,517.6 tx/s), the loaded mempool median was 17,140 and its max 30,826, with no evictions. The pace band (10k/20k) kept it well below the cap.
- What the mempool data does not tell us: who the other transactions belonged to, and which fee bands were waiting. The plan adds a 1-s sampler and a periodic fee-band snapshot.

## Q5. Send order vs accept order (sequencing)

**Status: partly answered (coarse).** Added after Kaspa Pulse's follow-up: the question isn't only how many transactions land, but **whether order holds under load**. A reorder or a stall would break a dapp that expects its transactions in order.

**What we have: the 25 Sep fee probes.** The probes from Q2 were sent in a fixed order, one per tier every 30 s, and each one's acceptance time was recorded (polled every 1 s). That lets us compare send order with accept order within each tier. A pair counts as reversed only if the later-sent probe was accepted **more than 1 s** before the earlier one. Raw: `logs/overload/probes.jsonl` → [`data/sep_probe_order_by_tier.csv`](data/sep_probe_order_by_tier.csv).

| Step | Tier | vs storm fee | Consecutive pairs reversed | Probes overtaken by a later probe | Stalled behind 2+ later probes | Longest overtake |
|---|---|---:|---:|---:|---:|---:|
| A (storm 1.2×) | 1× | 0.83× | 5 of 116 (**4.3%**) | 5 | 4 | 43 s |
| A | 1.2× | 1.00× | 3 of 116 (2.6%) | 3 | 1 | 47 s |
| A | 2× | 1.67× | 1 of 116 (0.9%) | 1 | 0 | 1.4 s |
| A | 5×, 10×, 100× | ≥ 4.2× | 0 | 0 | 0 | — |
| B (storm 2×) | 1× | 0.50× | 13 of 125 (**10.4%**) | 14 | 5 | **169 s** |
| B | 1.2× | 0.60× | 8 of 125 (6.4%) | 8 | 2 | 46 s |
| B | 2×, 5×, 10×, 100× | ≥ 1.0× | 0 | 0 | 0 | — |

- **Claim (measured on TN10):** **cheap transactions lost their order under load.** In the 1× and 1.2× tiers (at or below the storm's fee), 2.6–10.4% of consecutive probes (30 s apart) were accepted out of send order, and the share grew when the load rose (step A → B). Some probes waited behind two or more later ones ("stalls" in the table).
- **Claim (measured on TN10):** **at 2× the floor or above, order held** in these probes: one reversal of 1.4 s in step A, none in step B.
- **Not sure / open for debate:** whether this carries over to transactions sent closer together. The probes were 30 s apart, with 1-s acceptance polling. A dapp sending several transactions a second could see more reordering. Transactions accepted in the same block event can't be ordered at all at this resolution.
- **Not logged:** order in the October storm. The runners' lanes are chained (each hop spends the previous one), so order inside a lane is forced, and no cross-lane send/accept order was recorded.
- **Needs more testing:** per-step reorder rate, out-of-order accepts and stalls at 1× vs 1.5×, with send sequence numbers and exact accept positions. That is now a first-class goal of the [next storm](#next-storm-early-run-fri-9-oct-at-the-earliest-target-13-oct-if-not-ready) (above).

---

## How the TPS was reached

### (a) How TN10 ops runs a storm (stp's box)

Sources: `build-brief-how-box-storm-works-2026-10-02.md` (written from the running code), `storm-p2w-runner.mjs`, `r5-engine.mjs`, `storm-watch.sh`, `timeline.md`, the storm 2 public report.

- **One node, one box.** All load went into **n0**, our own TN10 kaspad 2.1.0 on the box (8 vCPU Xeon VM, 16 GB RAM, 126 GB disk). It runs without a UTXO index, with `--ram-scale=0.1` (mempool cap ~100k). The miners, runners and samplers ran on the same box.
- **Workers ("runners").** A runner is one Node.js process with **1,250 lanes** (1,500 for runner 1) and **4 wRPC connections** to n0. A single connection tops out at ~378 tx/s. **6 runners** was the default. **7 was best overnight in L1** (3,845 tx/s at Fri 01:26 vs 3,375 with 6; `timeline.md`). In L3, 7 added nothing (2,383 vs 2,410) and 8 collapsed throughput to 1,165.
- **Lanes = independent coin chains.** Each lane holds exactly one coin. Its next transaction spends the previous one's output, with one transaction in flight per lane. The runner waits only for the node's "accepted into mempool" reply, not for a block, then builds the child. It tracks every lane's tip locally and never asks the node for UTXOs during the run.
- **Self-transfer transactions.** Each hop is **1 input → 1 output** back to the same lane address, no payload, no change. "P2W" lanes use an anyone-can-spend script tag (`push4(laneId) OP_DROP OP_TRUE`), so hops need no signature and weigh **643 grams** of mass. A signed 1-in-1-out weighs ~1,700 g, so P2W fits ~2.6× more transactions into a block. Early L1 also used signed "SMX" runners.
- **Coin feeder (UTXO prep).** A feeder (`coinbase-feeder.mjs`) hands each new lane one whole mature coinbase coin from our own mining address (median 3.087 tKAS). One funding transaction (1,701 g) per lane, no fan-out. A lane retires below 0.3 tKAS and re-funds.
- **Fee.** A fee daemon reads `getFeeEstimate` every 30 s and sets `feerate = min(FEE_MAX, max(2 × 100, 2 × clamp(normal, 100, 200)))`, i.e. **2× the normal estimate, with the base clamped so our own load can't run it up**, cap 400. Average paid feerate was **337–386 sompi/g in L2–L4** and **1,090 in L1** (`data/oct_legs_from_public_report.csv`). L1 includes a 30× period (up to 6,000 sompi/g) on the night of 1–2 Oct, which the build brief describes as a runaway from multiplying the raw estimate. The clamp was added after it. In storm 1 (25–26 Sep) the fee was 1.2×, then 2×, then **10× = 1,000 sompi/g** from 26 Sep 00:14 (storm 1 handoff log).
- **Mempool backoff.** A pace band slows every runner linearly as n0's mempool grows, from full rate at the low mark to zero at the high mark. The marks changed between legs: 45k/72k in L2; 25k/45k, then 10k/20k in L3; 10k/20k in L4 (`timeline.md`). Each runner also hard-pauses above 75k and resumes below 55k (`r5-engine.mjs`; the build brief describes a later 90k setting). Storm-watch pauses everything above 80k until it falls below 55k (`storm-watch.sh`).
- **Stop and disk/memory guards** (`storm-watch.sh`, `timeline.md`):
  - runner pause at free disk ≤ 21 GB (briefly 19.5 GB on 2 Oct);
  - STOP when free disk stays under **19 GB for more than 900 s** (pruning-window seconds don't count);
  - immediate STOP at 10 GB;
  - STOP when free RAM < 1 GB, or when n0 is unsynced or more than 300 s behind for 2 ticks;
  - rate cut to 25% in the pruning windows (07:05–08:10 and 19:05–20:10).
  
  The scaler drops the newest runner if the sink age exceeds 2.5 s. Every October leg ended on a disk pause or a disk or RAM STOP.
- **Our own miners.** stp's miners made **50–63% of TN10 blocks** while the box miners ran: L1 P2W 60.3%, L2 62.8%, L3 58.1% (`block_share_legs.csv` in the public report; L4 52.6% from the independent sampler there). When the box miners stopped (Fri 01:31:50), our inclusion fell to ~300 tx/s although blocks were mostly empty.
- **Block mass is the ceiling.** TN10 blocks fill by mass at ~490–500k per block. Past the knee, more senders only grow the mempool. At 8 runners, blocks hit 492k mass, the block rate fell from 9.1/s to 7.8/s, and throughput halved (build brief §7).

### (b) How Build generated its load (stp's desk PC)

Sources: our prompts to Build (`grok-build-tx-sender-2026-10-02.md`, `grok-build-prompt-v2-2026-10-02.md`, and the storm 2 "desk sender part 3" prompt), the desk check in the [storm 2 public report](https://github.com/STP-KAS/tn10-storm-2026-10-public-report#desk-check-later-the-same-day), [round2](https://github.com/STP-KAS/grok-bot-vprogs-round2) ("Confounder: Grok Build agent") and the [build opinion](https://github.com/STP-KAS/tn10-vprogs-build-opinion).

- **Machine:** Intel Core i7-13700K (16 cores / 24 threads), 32 GB DDR5, Windows 11 Pro, 1 Gbps Ethernet (from stp's screenshot; not checked by us). It also ran 20 CPU miners at about 75% CPU (stp's figure).
- **Wallet:** Build's own TN10 wallet, funded by us (299,993 tKAS on 25 Sep, round2; ~1.2M tKAS on 1–2 Oct, sender prompt).
- **What we asked it to run** (the prompts): 1-input → 1-output signed self-sends in chained lanes, sent to **public TN10 nodes** found through the Kaspa resolver, never to our n0.
  - First version: up to 400 lanes, at most 1,000 tx/s per process, fee 2× normal capped at 600 sompi/g.
  - v2: a coordinator plus auto-scaled workers, each with 4 connections and 250 lanes; flat 1.5× normal fee, cap 600; pause above 80k mempool.
- **What its logs show** (desk check in the public report):
  - a sender log with **17,415,510 submits** (Thu 20:38 → Fri 12:03). Its `accepted` field is a submit result, not inclusion.
  - a public-node runner whose status lines reached **24,249 submit-OK per second** (Fri 15:35:44, 24 workers). That is above any inclusion ceiling we measured, so it's a submit rate.
  - a "local P2W scale" path counting inclusions on the desk's own local node, peak **2,795.6/s** for a minute (Fri 21:33, feerate 150); 2,698.6 during L4.
  - An earlier public wallet-load note by Build: 1,162 tx/s, which was 340 sweeps in 0.29 s, all included (as read in the build opinion).
- **Unknown:**
  - which exact script versions ran on the desk;
  - how many desk transactions were included on chain (transaction ids were never matched to n0);
  - the desk's CPU/network limits;
  - how the local P2W path was set up beyond its log lines.
- **The "~4k tx/s combined" figure is stp's report, not our measurement.** Desk and box counts were never reconciled transaction by transaction. The public indexer was frozen during much of the overlap (L4).

---

## Files

| Path | What |
|---|---|
| [`charts/1-submitted-vs-accepted-over-time.png`](charts/1-submitted-vs-accepted-over-time.png) | Q1: submitted vs accepted per minute, runner rate cap, n0 "Processed" |
| [`charts/1b-acceptance-flattening.png`](charts/1b-acceptance-flattening.png) | Q1: accepted vs rate cap, one dot per minute |
| [`charts/2-confirmation-time-by-fee-tier.png`](charts/2-confirmation-time-by-fee-tier.png) | Q2: confirmation-time distribution per fee tier, two load steps (25 Sep) |
| [`charts/2b-fee-tier-probes-over-time.png`](charts/2b-fee-tier-probes-over-time.png) | Q2: probe times over time with the mempool backlog (25 Sep) |
| [`charts/3-indexer-freeze-windows-vs-tps.png`](charts/3-indexer-freeze-windows-vs-tps.png) | Q3: api-tn10 lag and 503s, stall windows, box and n0 tx/s |
| [`charts/4-mempool-depth-over-time.png`](charts/4-mempool-depth-over-time.png) | Q4: n0 mempool per minute, pause flags |
| [`data/oct_box_submitted_vs_accepted_1min.csv`](data/oct_box_submitted_vs_accepted_1min.csv) | Per minute: rate cap, submitted, accepted, runners, mempool min/median/max, n0 Processed, disk, pause flags |
| [`data/oct_runner_latency_cumulative_by_segment.csv`](data/oct_runner_latency_cumulative_by_segment.csv) | Per runner segment: feerate, totals, cumulative p50/p95 |
| [`data/oct_api_tn10_health_2min.csv`](data/oct_api_tn10_health_2min.csv) | api-tn10 health samples with box and n0 tx/s |
| [`data/oct_api_tn10_stall_windows.csv`](data/oct_api_tn10_stall_windows.csv) | Stall windows (from the storm 2 public report) |
| [`data/oct_api_bad_samples_by_n0_processed_tps.csv`](data/oct_api_bad_samples_by_n0_processed_tps.csv) | Share of bad health samples by n0 load |
| [`data/oct_mempool_windows_from_public_report.csv`](data/oct_mempool_windows_from_public_report.csv) | Mempool statistics and evictions per window |
| [`data/oct_legs_from_public_report.csv`](data/oct_legs_from_public_report.csv) | Leg totals and peaks |
| [`data/sep_fee_tier_probes.csv`](data/sep_fee_tier_probes.csv) | 25 Sep: one row per fee-tier probe (no transaction ids) |
| [`data/sep_fee_tier_summary.csv`](data/sep_fee_tier_summary.csv) | 25 Sep: p50/p90/max per tier and step |
| [`data/sep_probe_order_by_tier.csv`](data/sep_probe_order_by_tier.csv) | 25 Sep: send order vs accept order per tier and step (reversals, overtakes, stalls) |
| [`data/sep_network_processed_tx_s_1min.csv`](data/sep_network_processed_tx_s_1min.csv) | 25 Sep: n0 "Processed" tx/s per minute (block-body count) |
| [`plan/NEXT-STORM-PLAN.md`](plan/NEXT-STORM-PLAN.md) | Next-storm measurement plan (locked by commit SHA before the run) |
| [`plan/GROK-BUILD-PROMPT.md`](plan/GROK-BUILD-PROMPT.md) | Paste-in prompt for Grok Build (desk sender): what to send, what to log, dry run, stop rules |
| [`scripts/extract.py`](scripts/extract.py), [`scripts/charts.py`](scripts/charts.py) | Rebuild data/ from the raw logs, and charts/ from data/ (Python 3, matplotlib) |

## Sources

Raw logs stay on stp's box. They are large (the virtual-chain log alone is 54 MB) and contain transaction ids.
- **Storm 2, 1–3 Oct:**
  - `stress-tests/data/`: `runner1-4.out`, `p2w1-8.out` (runner reports), `host.jsonl` (mempool, n0 counters, disk), `storm-watch.jsonl` (guards), `api-health-min.jsonl` (api-tn10 health);
  - `stress-tests/run/timeline.md` (operator log);
  - `stress-tests/build-brief-how-box-storm-works-2026-10-02.md`, `storm-p2w-runner.mjs`, `storm-watch.sh`, `r5-engine.mjs` (code and how-to).
- **Storm 1, 25–26 Sep:** `tn10-break-test-2026-09-25/logs/overload/probes.jsonl`, `logs/tps12h/nettps.jsonl`, `logs/storm/ramp.log`, `HANDOFF.md`.
- **Public repos:** [tn10-storm-2026-10-public-report](https://github.com/STP-KAS/tn10-storm-2026-10-public-report), [grok-bot-vprogs-round1-public](https://github.com/STP-KAS/grok-bot-vprogs-round1-public), [grok-bot-vprogs-round2](https://github.com/STP-KAS/grok-bot-vprogs-round2), [tn10-vprogs-build-opinion](https://github.com/STP-KAS/tn10-vprogs-build-opinion).

## Limits
- One node (n0) on one small box, with a lowered mempool cap. Our own miners made a large share of blocks.
- "Accepted" is first acceptance on n0's selected chain, measured on the box clock. Not finality.
- n0's "Processed" counter double-counts transactions that sit in several parallel blocks.
- The box rate cap is a target, not a measured offered load.
- api-tn10 is a third-party service. We only see it from outside.
- Where a number above is an estimate rather than a measurement, it is marked *(estimate)*.
