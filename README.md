> **Experimental. We are just trying this.**
>
> Good intentions, shaky hands. STP does not know what he is doing. We test, we write down what we think we saw, and that is the whole product. A number here is not the truth. A chart is not the truth. Any other sentence that sounds sure of itself is not the truth either. Do not count any of it as a claim.
>
> [Disclaimer](DISCLAIMER.md)

Wording, Kaspa Pulse (@gokugalax), 7 Oct 2026: sign-and-send processes are senders; runner is the setup; bot is reserved for the operator.

# TN10 storms: throughput, confirmation time, order, indexer and mempool

> **Experimental. Not advice.** [Disclaimer](DISCLAIMER.md).

Questions and guidance from Kaspa Pulse ([@gokugalax](https://x.com/gokugalax)). Thank you for the questions, for the guidance on how to run and publish the next test, for the sequencing point, and for the pass on the plan and its four tightenings.

**Kaspa Pulse, 7 Oct 2026:** weekly runs sound good. One clean run first, and go through those numbers properly, before we stack more. We send the results when that run is done, and take the next step from there.

Analysis and charts by TN10 ops, stp's AI operator bot for his TN10 stack. The runs are stp's TN10 setup: TN10 ops on its own node, and Grok Build on stp's desk PC. First written Sun 4 Oct 2026, 21:00–21:59 UTC. The front of this note was put in reading order on 6 Oct 2026. The measured tables below are the same extracts.

Kaspa **Testnet-10 (TN10) only**. Every clock on this page is **UTC**. Deliberate load stays on TN10. Mainnet comparisons and mainnet costing are out of scope, as Kaspa Pulse asked.

In our storms, our own miners made **50–63% of TN10 blocks** while they ran (storm 2 public report, `block_share_legs.csv`). The numbers describe **TN10 with our miners on it**, through one node on one small box. Every number names the file it came from. The CSVs in [`data/`](data/) are small extracts of our raw logs. The scripts in [`scripts/`](scripts/) rebuild those CSVs and every chart. Where something was **not logged**, the text says so.

## The notes

Each note keeps the disclaimer at the top. They are not one repo.

| Open this | What it is |
|---|---|
| [plan/PULSE-README.md](plan/PULSE-README.md) | Kaspa Pulse ([@gokugalax](https://x.com/gokugalax)). His inputs, in the order of the X chat. |
| [plan/GROK-BUILD-PROMPT.md](plan/GROK-BUILD-PROMPT.md) | Paste-in for Grok Build on 9 or 13 Oct. Ready. It does not start the storm. |
| [plan/TESTDAY.md](plan/TESTDAY.md) | The run, after the storm GO and `steps-utc.json`. |
| [plan/DESK-SHAPE-9-OCT.md](plan/DESK-SHAPE-9-OCT.md) | The shape that held. |
| [plan/NEXT-STORM-PLAN.md](plan/NEXT-STORM-PLAN.md) | The measurement plan. If the prompt, the test day, or the shape disagree with it, the plan wins. Not locked. |
| [tn10-build-desk-tps](https://github.com/STP-KAS/tn10-build-desk-tps) | Desk runs, oldest first. The six-hour 2,207 is here. |
| [tn10-build-desk-tps-3500](https://github.com/STP-KAS/tn10-build-desk-tps-3500) | 7 Oct included-rate tries, oldest first. 3,500 was not read. |
| [what-limits-tx-rate](https://github.com/STP-KAS/what-limits-tx-rate) | Why a signed payment stops near 3,080. Not a run log. |
| [tn10-storm-build-bot-challenge](https://github.com/STP-KAS/tn10-storm-build-bot-challenge) | Empty until after the storm. |

This page is the questions, the method, and the empty result sections. The runs below are oldest first.

## Contents

- [The notes](#the-notes)
- [What](#what)
- [Why](#why)
- [How](#how)
- [Goal](#goal)
- [Questions from Kaspa Pulse (@gokugalax)](#questions-from-kaspa-pulse-gokugalax)
- [Build and the bot](#build-and-the-bot)
- [Monitoring](#monitoring)
- [History of the storms](#history-of-the-storms)
- [Tasks for stp](#tasks-for-stp-before-the-storm), the [dry run](#desk-dry-run-6-oct-2026), the [9 Oct shape](plan/DESK-SHAPE-9-OCT.md), the [test-day run](plan/TESTDAY.md), [advice for the bot](plan/BOT-TPS.md), and [early recommendations for builders](#early-recommendations-for-builders)
- [Results after the storm](#results-after-the-storm): [Build](#build-result), [bot](#bot-result), [Leg 3](#leg-3-merged-challenge)
- [Open builder leg](#open-builder-leg), a separate idea
- [Measured data](#measured-data): charts and tables from the past storms

## What

One measured TN10 series. Two senders, one UTC timetable, five questions.

- **TN10 ops** (the bot) sends from stp's box through its own node, n0.
- **Grok Build** sends from stp's desk PC through public TN10 nodes.

The storm starts at **Fri 9 Oct 2026, 21:30 UTC** and runs **8 hours**, to **Sat 10 Oct 2026, 05:30 UTC**. If Build's dry run has not passed, or the tKAS and the usage resets are not ready, the same plan runs on **Mon 13 Oct 2026, 21:30 UTC**, to **Tue 14 Oct 2026, 05:30 UTC**. The 6 Oct early run is cancelled. There is no storm until the dry run passes and stp gives a separate GO for the storm. When that GO is given, the window is **8 hours** from T0. T0 is **21:30 UTC**. The paced table inside that window is still **2 h 55 min** and ends at T0+175 (**00:25 UTC** the next day).

This is a series. Weekly runs sound good. **One clean run first**, and go through those numbers properly, before we stack more. We send Kaspa Pulse the results when that run is done. Each run is published with its locked plan SHA and its own raw data.

The lock text is [`plan/NEXT-STORM-PLAN.md`](plan/NEXT-STORM-PLAN.md). Build's paste-in is [`plan/GROK-BUILD-PROMPT.md`](plan/GROK-BUILD-PROMPT.md). It is ready for 9 or 13 Oct. It does not start the storm. The run, once GO and `steps-utc.json` exist, is [`plan/TESTDAY.md`](plan/TESTDAY.md). The shape is [`plan/DESK-SHAPE-9-OCT.md`](plan/DESK-SHAPE-9-OCT.md). If the prompt, the test day, or the shape disagrees with the plan, the plan wins, and Build stops and asks stp.

## Why

Storm 1 (25–26 Sep 2026) and storm 2 (1–3 Oct 2026) left these gaps:

- submitted vs accepted came from a closed-loop sender, with no network-wide unique count;
- confirmation time was cumulative, at one fee per runner, and **1.5× was not tested**;
- indexer freezes were seen, and never tied to a load that was held on purpose;
- send order vs accept order was seen on probes 30 s apart, and never across senders or per step;
- Build's desk load was logged as submit-OK;
- our own miners (50–63% of blocks) and our own node's limits were mixed in with the chain.

The next storm counts both senders, switches our miners off for one control step, and logs the box limits on their own. The tables under [Measured data](#measured-data) are the record of those gaps.

## How

Kaspa Pulse's six process points, and the four tightenings from his review, are the method. Full text: [`plan/NEXT-STORM-PLAN.md`](plan/NEXT-STORM-PLAN.md).

| # | Point | In this run |
|---|---|---|
| 1 | Write the plan down first | Public now. Locked by commit SHA before T0. The results cite that SHA and list any deviation. |
| 2 | Baseline first | **B0:** 10 min of normal TN10 traffic, both senders off, measurements on. **B1:** 10 min after the load. |
| 3 | Fixed steps | **2×, 5×, 10×, 20×, 30×** the measured baseline, then max. A **2× miners-off control** sits right after the 2× step, at the same load. 15 min at the target, then 5 min of drain. The paced table is about 2 h 55 min. The storm window around it is 8 hours. If the baseline is under 50 or over 200 tx/s, the fallback is absolute steps of 500–3,000 tx/s. |
| 4 | Log submitted and accepted per second, and order | Per-second UTC counters for the box, for Build, and for the network. Per transaction: send sequence, submit time, accept position. |
| 5 | State the mining share up front | **50–63%** in the earlier storms. This run publishes the share **for every step**, including the miners-off control. |
| 6 | Raw data next to the summary | Per-second CSV, per-step summary, every probe, per-transaction samples, mempool, indexer and mining share, in `data/`. |

The four tightenings, already in the plan, before the lock:

1. **Miners-off control, in the main run.** One 2× step with our miners off, matched to the 2× step with them on. Last storm, with the box miners off, our inclusion fell to ~300 tx/s while n0's mempool sat near a median of 71,498. The control stays at the 2× target and under 250 tx/s total. Other miners' templates can still change. We log that beside the result.
2. **The box is its own machine.** Box traffic goes through n0: kaspad 2.1.0, `--ram-scale=0.1`, `--async-threads=4`, `--outpeers=6`, `--maxinpeers=24`, `--rpcmaxclients=64`, no UTXO index. Mempool cap about 100,000 transactions. We log n0's CPU, cap hits, evictions and reject reasons, and each runner's CPU, every second. Each plateau is labelled **box-bound**, **network-bound** or **unclear**, by a rule fixed before T0.
3. **Clocks.** NTP offset on the box and on the desk, at the start and at the end. A confirmation time that crosses the two machines is corrected for the offset, or flagged.
4. **Saturation and sample size, fixed before T0.** Saturated means our accepted stays under 95% of our submitted for 60 seconds, on a rolling 60-second window. Reorder rates are counts and percentages, with n and a 95% interval. Probes move from every 10 s to every **2 s**: about 450 samples per tier per step, and about 2,250 for 1× and 1.5× once the ordered stream is included.

Build runs on that same UTC timetable.

- The process count is fixed for the whole storm. The dry run settled it at **4** sender processes for the planned share. No auto-scale, no fleet relaunch, no mempool pause inside a step. Each process spends its own coins. One more process runs the ordered stream. The six-process hold on 6 Oct is a rehearsal. The planned share stays at 4.
- Build's share of each step's added load defaults to **25%**, capped at what the dry run held. The box sends the rest. Both rates are measured.
- Fees: half the lanes at **1×** the node's normal estimate, half at **1.5×**, frozen for the step. 1.5× stays under the 600 sompi/gram cap.
- Gate: achieved send rate at least 95% of target at every step, per-transaction logs complete, txids matched to what n0 accepted, UTC timetable followed. Miss the gate, and the storm waits for 13 Oct.

Box side: 6 runners × 4 connections, a 7th only at the max step. Go only with at least 35 GB free at T0. Between 28 and 35 GB, the steps shrink to 10 min. Below 28 GB, no storm. Keep about 19 GB free for n0's pruning. A guard stop ends the run for the box and for Build, and the stop is reported. T0 is 21:30 UTC. The storm window is 8 hours.

## Goal

Goals from Kaspa Pulse ([@gokugalax](https://x.com/gokugalax)). Thank you. The screen of the X chat on 8 Oct 2026 is the source for this list. The measurement plan is [plan/NEXT-STORM-PLAN.md](plan/NEXT-STORM-PLAN.md). If this list and that plan disagree, the plan wins.

Two headlines. Order under load, because a reorder or a stall is what a dapp would feel. And whether paying 1.5× buys inclusion while 1× is waiting.

**What the storm measures.** Asked 4 Oct 2026, for the TN10 run.

1. Accepted transactions per second against submitted, over the whole storm, and where acceptance flattens.
2. Confirmation time at each load step, median and worst, normal fee against 1.5×.
3. Whether the indexer freezes, at what sustained rate, and for how long.
4. Mempool depth over time, so the backlog is visible and the rate is not the only number.
5. Send order against accept order. He named this the real question on 5 Oct 2026: the metric is whether order holds under load, not the raw throughput.

**How the run is judged.** Asked 5 Oct 2026, before the lock.

1. The plan is written down before the run and published with the results. The window was not picked after the fact.
2. A short baseline first, so the storm has something to sit next to.
3. Fixed steps, not one blast. His example was 1×, 2×, 5×, and 10× of normal load, each held long enough to see where it bends. The step table in the plan is the one the run uses.
4. Submitted and accepted, per second, UTC. For order: the order sent, and the order accepted.
5. Mining share stated up front. He put our share near 60% of TN10 hashrate. The storm 2 report measured 50–63% of blocks. The result says which figure it is using. It describes TN10 with our miners, not mainnet.
6. Raw data next to the summary.
7. One miners-off step in the main run, at a load the other miners can absorb, matched to the same step with our miners on. A high load with our miners off only measures backlog. The low matched step is the control.
8. The box is not the chain. Log the box limits on their own, and label each plateau box-bound or network-bound.
9. Both clocks checked against NTP at the start and at the end.
10. Saturation defined before the start: accepted below 95% of submitted for 60 seconds. Reorder rates as counts and percentages, with n and an interval.

**What this series is.** Asked 7 Oct 2026.

- One clean run first. Go through those numbers properly. Send Kaspa Pulse the results when that run is done. Weekly repeats wait until that pass.
- He counts the chain on his own side: accepted per second, confirmation times, and fees. He does not touch the setup. After the run the two counts go side by side, and he sends the comparison first.
- The same window on both clocks. A chain-accepted count and a submit count are not one number.
- A stuck pool is named, chain or node, before anyone calls it a ceiling. The 2,750 figure and the pool near 9.7k are that question. The reading is [plan/PULSE-WINDOW-7-OCT.md](plan/PULSE-WINDOW-7-OCT.md). On 7 Oct those two were not the same minute, and his 18:52–19:23 UTC window is not in our log.
- A process that signs and sends is a sender. The runner is the whole setup. TN10 ops stays the operator.

Mainnet congestion costing is out. He passed on it. Deliberate load stays on TN10.

A number is ready for the merged result when both senders are in the run, the transaction can be matched by txid on n0, and the file behind the number is in this repo. TN10 ops writes its own result. Grok Build writes its own result. The figure both sides reproduce is written in the [challenge repo](https://github.com/STP-KAS/tn10-storm-build-bot-challenge).

## Questions from Kaspa Pulse (@gokugalax)

These five are the measured goals. Thank you, Kaspa Pulse ([@gokugalax](https://x.com/gokugalax)), for them, and for making order its own question. The right-hand column is the short reading of data we already had. The next run is what is supposed to close the gaps.

His inputs, in the order of the screen, are [plan/PULSE-README.md](plan/PULSE-README.md). The two that were missing from this section are here as well.

**7 Oct 2026, 19:23 UTC.** Kaspa Pulse ([@gokugalax](https://x.com/gokugalax)): you did, all clear, thanks. our dry run counted 18:52 to 19:22 utc, right inside your run. once your log for that window is on git we'll put both side by side and send you the comparison first. and the 2,750 ceiling with the pool stuck at 9.7k is exactly the kind of thing we'd love to pin down, chain or node. no spam at all, keep it coming

**7 Oct 2026, 19:27 UTC.** Kaspa Pulse ([@gokugalax](https://x.com/gokugalax)): first dry run done, clean on our side. for the 18:53 to 19:23 utc window we count what the chain actually accepted, and it came out much lower than your screenshot, so before we read anything into it we want to line up the same window. could you share, when you have a sec: start and end of your run, the target tx/s, whether your bot counts sent or accepted, which node it sends to, and a handful of tx ids from that window? then we check those ids on chain one by one. might just be that the bot stalled when your pool got stuck

At 19:54 UTC the same day he replaced "bot" in that ask with sender. The window reading is [plan/PULSE-WINDOW-7-OCT.md](plan/PULSE-WINDOW-7-OCT.md).

| # | Question | What we will log | Past storms |
|---|---|---|---|
| 1 | Accepted tx/s vs submitted, over the whole storm, and where acceptance flattens | Per second, UTC: submitted, accepted and offered, for the box and for Build, by fee tier. Network-wide unique accepted from n0's `virtual-chain-changed`. Rejects by reason. | Partly. Box acceptance flattened around 2,200–2,600 tx/s. The sender was closed-loop. |
| 2 | Confirmation time at each load step, median and worst, normal fee vs 1.5× | Per transaction: sequence, submit time, accept time, tier. Probes every 2 s at 1×, 1.2×, 1.5× and 2×. | Partly. 25 Sep has 1×, 1.2×, 2× and higher. **1.5× was not tested.** |
| 3 | Does the indexer freeze, at what sustained tx/s, and for how long | api-tn10 `/info/health` every 30 s. Once a minute, the time until one of our accepted transactions shows up there. | Partly. It froze. We have no threshold from a held load. |
| 4 | Mempool depth over time | n0 mempool every 1 s. Fee estimate every 10 s. | Answered for storm 2, sampled every 15 s. Peak 99,992. |
| 5 | Send order vs accept order | A send sequence per sender, and the accept position on n0. An ordered stream of independent transactions, 2 per second per tier, at 1× and 1.5×. | Partly, and coarse. Probes 30 s apart on 25 Sep. The October storm did not log order. |

Charts, sample sizes and the source files are under [Measured data](#measured-data).

## Build and the bot

Two senders. Each one writes its own result. Same questions, same UTC timetable, same acceptance clock: n0 sees every accepted transaction, whichever node it was sent to.

| | Grok Bot — TN10 ops | Grok Build |
|---|---|---|
| Where it runs | stp's box | stp's desk PC |
| Where it sends | Its own node, n0 (kaspad 2.1.0, `--ram-scale=0.1`, mempool cap about 100,000) | Paced steps: public TN10 nodes. The long hold and the uncapped max also use the synced desk node, on coins the public signers are not using. On 7 Oct 2026 the six public hostnames were three machines. Recheck before counting them. Never n0. Never bore.pub. |
| This storm | The rest of each step, after Build's share | Paced steps: **4** sender processes plus one ordered stream. Default share 25%. Long hold and uncapped max: two signers on each physical machine, plus the desk node. |
| Coins | Its own | Its own. A separate set for each process. |
| Fee | 1× and 1.5× of n0's normal estimate, frozen for the step | The same two tiers on the node it asks, frozen for the step. 1.5× stays under the 600 sompi/gram cap. |
| What it logs | Per second and per transaction, on the box | Per second and per transaction, on the desk. Inclusion is the txid match on n0. |
| Where the result goes | [Bot result](#bot-result), after the storm | [Build result](#build-result), after the storm |
| Earlier storms | Storm 1 and storm 2, the box runners. [How the TPS was reached, box](#a-how-tn10-ops-runs-a-storm-stps-box). | The desk sender logged submit-OK. Transaction ids were not matched to n0. [How the TPS was reached, desk](#b-how-build-generated-its-load-stps-desk-pc). |

The 6 Oct dry run and the monitored hold sit under [Tasks for stp](#tasks-for-stp-before-the-storm). They are the gate and a rehearsal. They are not the result sections.

## Monitoring

The same watches run for the baseline, every step, both drains, and the miners-off control. They have to be able to answer all five questions.

| Watch | Rate |
|---|---|
| Submitted, accepted, offered, and rejects, by sender and by fee tier | Every second, UTC |
| Network-wide unique accepted, from n0 `virtual-chain-changed` | Every second |
| Fee probes at 1×, 1.2×, 1.5×, 2× | Every 2 s |
| Ordered stream, independent transactions, at 1× and at 1.5× | 2 tx/s per tier |
| n0 mempool size | Every 1 s |
| Fee estimate | Every 10 s |
| api-tn10 `/info/health`, cache bypassed | Every 30 s |
| Whether the indexer can see one of our transactions | Every minute |
| n0 CPU, mempool-cap hits, evictions, reject reasons, and runner CPU | Every second |
| Mining share | Published for every step, including miners off |
| NTP offset, box and desk | At the start and at the end |

A step is sender-limited when that sender's submit-OK stays under 95% of its target. Saturation is the 95% / 60 s rule in the plan.

The [monitored hold of 6 Oct, 20:57 UTC](#monitored-hold-6-oct-2026-2057-utc) is a rehearsal of this table: six fixed Build processes, the five questions recorded together, for 45 seconds. It does not replace the four-process gate, and it does not start the storm.

## History of the storms

Oldest first. The short bursts stay above the long holds. The 9 or 13 Oct row is last because it has not been run.

| Run | When | Who | What we can already say |
|---|---|---|---|
| Storm 1 | 25–26 Sep 2026 | TN10 ops on the box, with fee-tier probes | Confirmation time by fee tier, and a coarse order check. No 1.5× tier. |
| Storm 2 | 1–3 Oct 2026, legs L1–L4 | TN10 ops through n0. Build on the desk over the same days. | Box submitted vs accepted, indexer freezes, mempool depth. Build logged submit-OK. Order was not logged. |
| Desk dry run | 6 Oct 2026, about 20:07–20:29 UTC | Build. Four processes for the planned share. Public nodes. | Four processes cleared 95% of 750 on the mean (734 tx/s, 97.9%). The txid match against n0 is still open. This was not the storm. |
| Ceiling bursts | 6 Oct 2026, after that dry run and before 20:57 UTC | Build. Public nodes. | 6,321 submit-OK for 20 s, seen accepted about 1,900 in that window. 9,100 submit-OK for 12 s, with 28,617 orphans. Not holds. |
| Monitored hold | 6 Oct 2026, 20:57 UTC | Build. Six processes. | A 45-second rehearsal of the five questions. Mean submit-OK 6,281 tx/s. This was not the storm. |
| Depth 8 hold | 2026-10-06 21:22–22:53 UTC | Build. Six public nodes. | 539 tx/s submit, 521 tx/s seen accepted. Most seconds were zero. [Desk note](https://github.com/STP-KAS/tn10-build-desk-tps#long-holds-6-7-oct-2026). |
| Depth 2, five nodes | 2026-10-06 23:12–23:52 UTC | Build. | 1,655 tx/s submit, 1,641 tx/s seen accepted. |
| Two signers, fee 200 and 300 | 2026-10-06 23:53 UTC to 2026-10-07 05:54 UTC | Build. Two signers on each public node. | **2,210 tx/s submit, 2,207 tx/s seen accepted.** The long number. |
| Fee 400 and 600 | 2026-10-07 06:39–16:38 UTC | Build. Twelve public lane signers. | **668 tx/s submit, 273 tx/s seen accepted.** Seen accepted is 0 after 08:05 UTC. Does not replace 2,207. |
| Included-rate tries | 2026-10-07 14:26–16:27 UTC | Build. Desk node. Lighter hop. | Best minute 2,951. Best socket 1,636. 3,500 was not read. [3500 note](https://github.com/STP-KAS/tn10-build-desk-tps-3500). |
| Next storm | Fri 9 Oct 2026, 21:30 UTC, for 8 hours, to Sat 10 Oct 05:30 UTC. Otherwise Mon 13 Oct 21:30 UTC, to Tue 14 Oct 05:30 UTC. | The bot and Build, on one timetable | The five questions, both senders, and the miners-off control. When GO is given, 8 hours from T0. The paced table is 2 h 55 min inside that window. The result sections stay empty until then. |

While the box miners ran in storm 2 they made 50–63% of TN10 blocks. When they stopped on Thu 1 Oct at 23:31:50 UTC, our inclusion fell to about 300 tx/s.

Charts and per-minute files: [Measured data](#measured-data). Earlier write-ups, still the sources: [storm 2 public report](https://github.com/STP-KAS/tn10-storm-2026-10-public-report), [round1-public](https://github.com/STP-KAS/grok-bot-vprogs-round1-public), [round2](https://github.com/STP-KAS/grok-bot-vprogs-round2), [build opinion](https://github.com/STP-KAS/tn10-vprogs-build-opinion).

## Tasks for stp (before the storm)

Status at the close of the desk pre-run, 2026-10-07T05:55:18 UTC. The long holds, with the exact window of every run, are in [tn10-build-desk-tps](https://github.com/STP-KAS/tn10-build-desk-tps#long-holds-6-7-oct-2026). The senders stopped at 2026-10-07T05:54:55 UTC. Covenant activity on TN10 is gaining traction again after that stop. The slices and the reason are in [point 9](#early-recommendations-for-builders) and on the [desk page](https://github.com/STP-KAS/tn10-build-desk-tps#after-the-stop).

| # | Task | Status |
|---|---|---|
| 1 | Dry-run gate. No storm until it passes. | **Passed on the desk.** 4 processes, 734 tx/s, 97.9% of 750, 0 rejects. Log check at 2026-10-07T13:59 UTC: 148,991 submit-OK, 0 rejects, every required field present, seq 1..N with no gaps. The manifest is on the desk, not in git. The n0 txid match is still open. Detail below. |
| 2 | Enough tKAS for the full schedule. | **OK for both wallets.** [Grok Build](https://github.com/STP-KAS/groks-wallet#grok-build) ([TN10 page](https://tn10.kaspa.stream/addresses/kaspatest:qp4jge54eztxewf8r53rtjdvxakmatsu6tjd0nn9sjhgvzxknsfvjvmwurqhd)) and [Grok Bot](https://github.com/STP-KAS/groks-wallet#grok-bot) ([TN10 page](https://tn10.kaspa.stream/addresses/kaspatest:qzffl5xy9np46gkttyuftqnv2w04pr8g3wsp7c3vv8se3txtelx6q7c0v0ldx)). Desk reading of Build at 23:00 UTC on 6 Oct: 3,612,867 tKAS, 15,944 coins of at least 2 tKAS. The Bot wallet is OK on stp's word. The box balance was not read from this desk. |
| 3 | Usage resets for the bots and Build. | **OK**, per stp on 7 Oct 2026. |
| 4 | Box dry run, and at least 35 GB free at T0. | **Not done.** Not measured from this desk. |
| 5 | Set Build's share, then lock the plan by commit SHA. | **Not locked.** The 25% share still fits the dry run. The shape to use is saved. Lock stays with stp before T0. |
| 6 | Desk clock, and the miner switch. | **Start logged, switch not run.** +73 ms at 2026-10-06T23:00:16 UTC. Stripchart at 2026-10-07T13:58:54 UTC was +77 ms. Miners: 0. |
| 7 | Final OK on the start time. | **Not given.** The start is Fri 9 Oct 2026, 21:30 UTC, for 8 hours, to Sat 10 Oct 05:30 UTC, otherwise Mon 13 Oct 21:30 UTC, to Tue 14 Oct 05:30 UTC. |

### On test day

Start [`plan/TESTDAY.md`](plan/TESTDAY.md). That is the run. It uses [`plan/DESK-SHAPE-9-OCT.md`](plan/DESK-SHAPE-9-OCT.md) and the paste-in prompt [`plan/GROK-BUILD-PROMPT.md`](plan/GROK-BUILD-PROMPT.md). No command list to copy. It sends only after the storm GO and `steps-utc.json`. If it disagrees with [`plan/NEXT-STORM-PLAN.md`](plan/NEXT-STORM-PLAN.md), the plan wins.

Paced steps: 4 processes, depth 2, in-flight 48. The long hold and the uncapped max step: two signers on each public node, depth 2, in-flight 64, fee 200 and 300, cap 600. That shape held 2,207 tx/s seen accepted from 2026-10-06T23:53:27.326 UTC to 2026-10-07T05:54:53.185 UTC.

### For the Grok bot

[`plan/BOT-TPS.md`](plan/BOT-TPS.md) is the high-TPS advice from this pre-run. The bot keeps its own wallet and its own sender. Depth 2, a fee near the loaded quote, and disjoint coins are what turned a 521 tx/s long run into a 2,207 tx/s long run. Depth 8, a fee of 2,000, and a few seconds above 6,000 submit-OK did not hold.

The gate itself is unchanged. Build's process count is fixed for the whole storm. No auto-scale. Each process has its own coins. A step passes when achieved stays at or above 95% of target, the per-transaction logs are complete, the txids match what n0 sees accepted, and the run follows the UTC timetable. The prompt is [`plan/GROK-BUILD-PROMPT.md`](plan/GROK-BUILD-PROMPT.md).

### Early recommendations for builders

**Not sure / open for debate.** This is this desk's view after the 6–7 Oct TN10 pre-run. It is not a Kaspa rule, not an audit, and not a mainnet result. It is a plan a builder can try when a dapp, or anything else that sequences its own transactions, should keep moving on TN10. The same plan is what this desk would try on mainnet. Mainnet was quiet the same night, about 11 tx/s with mempool 1, so that part is untested.

The one request behind the plan: a flow that is hurt by sitting in the mempool should raise its own fee while the network is loaded, and lower it when the load passes. The rest are the other things this desk would change before calling a rate real.

**1. Let the fee follow the network, up to a ceiling chosen first.** Read a public fee estimate on a timer. When the normal estimate rises above the fee on your next transaction, raise that fee toward the estimate. When the estimate falls, lower it. Do not leave a sensitive flow frozen at the quiet-network floor for the whole congestion. On this desk the quiet floor was 100 sompi/gram. After the mempool filled, the normal estimate sat near 186–194, and a pair frozen at 200 and 300 kept inclusion moving for six hours. A pair frozen at 100 and 150 took a smaller share of the same kind of blocks. A fee of 2,000 did not hold: orphans overtook submits and the rate fell away. This desk's own ceiling stays 600 sompi/gram. An automatic raise that can pass the ceiling is not this plan.

**2. Keep the unconfirmed chain short.** Depth 8, from 2026-10-06T21:22:15.436 UTC to 2026-10-06T22:53:03.590 UTC, filled and then sat at zero for most seconds: 521 tx/s seen accepted. Depth 2, two signers on each public node, from 2026-10-06T23:53:27.326 UTC to 2026-10-07T05:54:53.185 UTC, held 2,207 tx/s seen accepted. For a sequencer, this desk would start at two unconfirmed hops per coin and add the next hop when one is accepted.

**3. Count accepts, and treat a silent feed as a fault.** Submit-OK of about 6,300 tx/s for 20 seconds, and about 9,100 tx/s for 12 seconds, did not last. The number to publish is seen accepted over the whole window. At 2026-10-07T03:39:25 UTC this desk's observer stopped reporting new blocks. The signers' own feeds kept counting accepts until the stop at 05:54:53 UTC. A builder who only watches one subscription can mistake a dead feed for an idle network. Reconnect, and check a second node, before you drop the fee or add more transactions.

**4. One spender per coin, and do not reshuffle coins while the mempool is full.** Two processes on one coin spend the same output. A new split while the old transactions are still in the mempool spends outputs that already have a child in flight. At 2026-10-07T06:09 UTC, about 15 minutes after this desk stopped, vector-10 still reported about 50,900 in the mempool, and the count was falling by only a few per second, while the virtual DAA score was still advancing at about 10 per second. At 2026-10-07T06:27:46 UTC the highest of the six public mempools was still 49,141. Wait for that count to clear before the next split. The count is a warning about coins. It is a poor signal that the next block is full: the 06:09 UTC slice in point 9 was about 1.5 user transactions per block.

**5. When every lane is already waiting, more CPU does not raise the rate.** The twelve signers used about one core, and the machine was near 5% CPU, with every lane two deep. A signed one-input one-output is about 1,624 grams. At 500,000 grams and 10 blocks per second that is about 3,080 tx/s. This hold was 2,207. The gap is block space, not idle cores. The change this desk would test next is a higher fee still under the 600 ceiling, not a thirteenth signer. A lighter transaction is the change to test only after that, and it is untested here.

**6. Order is something you measure.** In the 25 Sep probes on this repo, sent 30 seconds apart, 2.6–10.4% of consecutive probes at the storm's own fee were accepted out of send order. At twice that fee, reversals were rare. A higher fee shortened the wait in those probes. It does not by itself prove a later sequence will hold. A sequencer that needs order should use its own coins, send the next one after the previous accept, log send order against accept order, and publish the reversals with the rate.

**7. Do not read inclusion only from the indexer.** On 2 Oct, api-tn10 froze for 86 minutes, lag up to 4,311 seconds, while the box was still sending. A dapp that decides "included" from the indexer should also have a node feed. The indexer can lag, or stop, while the chain is still accepting.

**8. Mainnet gets the same shape of plan, not these TN10 numbers.** A sensitive mainnet flow should watch the mainnet estimate, raise and lower its fee inside a ceiling chosen for mainnet, keep a short unconfirmed chain, and count accepts. It should not copy 200, 300, or 2,207 tx/s onto mainnet. Those numbers are this TN10 pre-run. Mainnet that night was quiet, about 11 tx/s with mempool 1.

**9. After a plain flood stops, covenant activity comes back because the block opened.** The senders stopped at 2026-10-07T05:54:55 UTC. Covenant flows on TN10 are gaining traction again. This desk's view: the apps did not change. The plain transfers stopped taking the block, a waiting covenant step can be accepted, and the app can post the next step.

Three slices from api-tn10, 40 selected-chain blocks each, coinbase left out. A covenant transaction is one with a covenant on an output. The times are the two ends of the walk. These are a few seconds each, so they are not an hour rate. The same table is on the [desk page](https://github.com/STP-KAS/tn10-build-desk-tps#after-the-stop).

| When | Span | User txs | Covenant txs | Per block |
|---|---|---:|---:|---:|
| During the hold | 2026-10-07T02:59:49 UTC to 02:59:58 UTC | 12,218 | 3 | about 305 |
| 15 min after the stop | 2026-10-07T06:09:38 UTC to 06:09:43 UTC | 61 | 3 | about 1.5 |
| 22 min after the stop | 2026-10-07T06:17:11 UTC to 06:17:19 UTC | 279 | 7 | about 7 |

During the hold that slice was 12,218 user transactions and 3 covenant transactions. After the stop the plain flood is gone, and covenant transactions are in the open blocks (3, then 7, with 8 and then 26 covenant outputs). A render of the TN10 homepage at this desk left the last-hour Covenants card empty, so this is the block sample, not that card.

The six-hour hold included 2,207 plain transfers per second. Each is about 1,624 grams, at 200 and 300 sompi per gram. About 3,080 of them fill a 500,000-gram block at 10 blocks per second, so the hold was most of the mass. Miners take a higher fee per gram first. A covenant step often weighs more, so the same fee per gram costs more, and a step that stays near the quiet floor waits behind the plain transfers. A covenant app is a sequence. The next step is built from the output of the previous one, so one waiting step holds the whole flow. The explorer then shows a quiet covenant lane. When the plain flood stops, the next blocks have room. The waiting step is included, the app posts the next one, and the lane looks busy again. That is the traction.

The mempool count can stay large while this happens. At 2026-10-07T06:27:46 UTC the highest public mempool was 49,141. A vector-10 fee read at 2026-10-07T06:28 UTC was about 162 and 131 sompi per gram in the normal buckets, and about 243 in the priority bucket. During the hold the normal quote was about 186–194 and the priority quote was about 876. Watch the blocks. A high mempool count alone will keep calling the network packed after the blocks have opened.

The mainnet hour the same night, Covenants 44 and mempool 1, is the other network. It is not this TN10 recovery.

This plan does not start the 9 Oct storm. The storm's own fee rule is still the one in [`plan/NEXT-STORM-PLAN.md`](plan/NEXT-STORM-PLAN.md). If they disagree, the plan wins.

### Desk dry run, 6 Oct 2026

Result of task 1, from the desk. The storm was not started. Raw txid logs stay on the desk for the box to match. They are not in this commit.

**Process count for the storm: 4.** Fixed for the whole run. No auto-scale, no fleet relaunch, no mempool pause. Each process spends its own coins. The ordered stream is a separate process. Desk miners during the test: **0**, and that count did not change.

**Node path: public TN10 nodes** (vector-10, proton-10, electron-10, muon-10), four connections per process, each lane pinned to one connection. The desk's own node was started for the comparison and was still downloading headers, with no RPC open, so it took no traffic. A split across the desk node and the public nodes waits until that node is synced.

**Ordered stream, 30 s** (2 per second at 1× and 2 per second at 1.5×). 120 of 120 submit-OK, 0 rejects, 0 seconds at 0. Fees 100 and 150 sompi/gram. All 120 were seen accepted on those public nodes' virtual chain.

**Top share, 750 tx/s**, counted on the wall clock:

| Processes | Window | Wall-clock mean | Of 750 | Seconds at 0 | Gate |
|---|---|---:|---:|---:|---|
| 1 | 31 s | 637 tx/s | 85% | 0 | fail |
| 2 | 3 min | 698 tx/s | 93% | 0 | fail |
| 4 | 3 min | 734 tx/s | 97.9% | 0 | pass on the mean |

One process is at the signing ceiling, so its slices run longer than a wall second. Two processes still land at 93%. Four is the smallest count that clears 95%.

The four-process confirmation ran 20:23:29 UTC to 20:26:29 UTC. 132,371 submit-OK, 0 rejects. Fees frozen at 100 and 150 sompi/gram. 1.5× is under the 600 sompi/gram cap, so the cap was not raised. 66,007 transactions at 1× and 66,364 at 1.5×. Every per-transaction field is present, times are UTC with milliseconds and `Z`, and `seq` is monotonic per process. 132,026 of those transactions were seen accepted on the public nodes before the processes stopped. 345 were still in flight at the stop.

The mean clears 95%. The rate is not flat: 21 of 177 seconds were under 95% of 750, and the lowest second was 374. No second was 0.

**Lower steps, same 4 processes, 20 s each, started on a UTC time.** Each hit its target on every second, with 0 rejects and 0 seconds at 0.

| Step target | Submit-OK | Seen accepted before stop |
|---:|---:|---:|
| 25 tx/s | 500 | 483 |
| 100 tx/s | 2,000 | 2,000 |
| 225 tx/s | 4,500 | 4,500 |
| 475 tx/s | 9,500 | 9,006 |

The rest of the 25 and 475 steps were still in flight at the stop, not rejected.

**Clock.** Offset against `time.windows.com` was +35 ms at 20:07 UTC, +45 ms at 20:18 UTC, and +50 ms at 20:29 UTC. All under 100 ms. No resync. Node.js 24.19.0. Public nodes reported kaspad 2.1.0.

**n0.** Acceptance above is from the public nodes the desk submitted to. It is not yet matched against the box node n0. That match is the box's check, once it has the desk logs.

**Ceiling, same evening.** The table above is the gate for the planned share. After it passed, the desk tried for the highest submit rate it could hold. Same wallet, public nodes only, fees still frozen at 100 and 150 sompi/gram. The desk's own node was still syncing and took no traffic.

| Setup | Window | Submit-OK | Rejects | Mean submit | Seen accepted during the window |
|---|---|---:|---:|---:|---:|
| 1 process, vector-10 | 20 s | 44,996 | 0 | 2,250 tx/s | 32,344 |
| 6 processes, one per public node | 20 s | 126,426 | 0 | 6,321 tx/s | 38,822 |
| 10 processes, two each on the five faster nodes | 12 s | 109,991 | 28,617 orphans | about 9,100 tx/s | about 14,500 |

Muon-10 held about 290 tx/s in the six-process run, so the ten-process run left it out. The orphans are a child submitted before that node would take its parent. Submit-OK counts only transactions the node took. Inclusion during the window was lower than the submit rate: the rest was still in mempools when the processes stopped. Just after the ten-process run, proton-10's mempool was about 37,000 and its normal fee estimate had moved to 162 sompi/gram. The runs did not follow that move. They stayed at 100 and 150, under the 600 cap.

Past about 9,000 tx/s the public nodes are the limit. The desk still had free CPU and free RAM. This ceiling is not a new storm rate. The storm still uses 4 fixed processes for the planned share.

Tasks 1, 2, and 3 are marked in the table above. Tasks 4, 5, and 7 are still open. Task 6 has its start and its pre-run end offset. The miner switch waits for the storm. The start is Fri 9 Oct 2026, 21:30 UTC, for 8 hours, to Sat 10 Oct 05:30 UTC, otherwise Mon 13 Oct 21:30 UTC, to Tue 14 Oct 05:30 UTC. This note does not start the storm. The long-hold totals are in [tn10-build-desk-tps](https://github.com/STP-KAS/tn10-build-desk-tps#long-holds-6-7-oct-2026).

### Monitored hold, 6 Oct 2026, 20:57 UTC

The bot already holds more than 3,000 tx/s on its own. This run asked whether the desk can hold that or more, with the five questions recorded at the same time. It is a rehearsal, not the storm. Six fixed processes, one per public node, plus the ordered stream. Fees frozen at the step start: **158 and 237** sompi/gram. Desk miners: **0**. The desk clock was **+60 ms** against time.windows.com. The desk's own node was still syncing, so acceptance was read from vector-10's virtual chain. The box node n0 still matches the same txids.

| Question | What this 45-second hold showed |
|---|---|
| 1. Submit vs accept | **6,281 tx/s** mean submit-OK (min 2,952, max 10,404). 282,651 submit-OK. About 3,200 orphan rejects. The listeners saw about **1,500/s** of ours accepted during the send. **55.8%** had been accepted on vector-10 by two minutes after the stop. The 95% saturation rule fails on this window. |
| 2. Confirmation, 1× vs 1.5× | Of the transactions that landed before the watch stopped: 1× median **23.0 s** (p95 140 s, n=79,448); 1.5× median **20.9 s** (p95 139 s, n=78,290). Paying 1.5× bought about 2 seconds at the median. The tail did not move. **44%** were still unaccepted when the watch stopped, so these percentiles are the ones that made it in. |
| 3. Indexer | api-tn10 `/info/health` every 30 s: HTTP 200, synced, accepted-tx lag **0–3 s**. It did not freeze during this short hold. |
| 4. Mempool | Four public nodes climbed together to a max of about **181,000**. vector-10 peaked near **51,000**. muon-10 stayed near a median of **2,100** and only contributed about 270 tx/s. The normal fee estimate moved from about 148 to about 192 while our tiers stayed frozen. |
| 5. Order | The ordered stream (4 tx/s, both tiers) had **4 reversals in 66** consecutive pairs sent at least 1 s apart (**6.1%**, 95% CI 2.4–14.6%). One same-event tie. No 30-second stall in that stream. On the flood, 46% of 1.5× transactions passed an earlier 1× from the same process. The blast itself sends faster than one per second, so its consecutive pairs are not the ≥1 s sample. |

Block rate stayed about 8–10 per second, with a one-second peak of 21. The network kept producing blocks while the mempool grew.

If Build's job is to match the bot, this desk did it at **six** processes, not at the four that hold the planned 750 tx/s share. Muon-10 is the weak node. The four-process gate for the planned share still stands. This rehearsal does not replace it, and it does not start the storm.

## Results after the storm

Empty on purpose. These three sections are filled only after the storm of Fri 9 Oct 2026 or 13 Oct 2026. The 6 Oct dry run and the monitored hold stay under Tasks. They are rehearsals, and they stay there.

### Build result

**Status: empty.**

After the storm, Grok Build's own reading goes here, from Build's logs. Each number names its file. The five questions, for Build's transactions:

1. Submit vs accept, and where acceptance flattened.
2. Confirmation time, 1× vs 1.5×, per step.
3. Indexer freezes: the sustained tx/s, and the length.
4. Mempool depth across the steps.
5. Send order vs accept order.

### Bot result

**Status: empty.**

After the same storm, TN10 ops writes its own reading here, from the box logs. The same five questions, for the box, plus the network-wide counts n0 saw. This section keeps the bot's numbers. Build's numbers stay in the Build section.

### Leg 3: merged challenge

**Status: empty. The page for it is already open.**

After both sections above are filled, Build and the bot each test the other's result against the same files. The test has its own repository, so the two sections on this page stay as each side wrote them.

https://github.com/STP-KAS/tn10-storm-build-bot-challenge

The challenge repo is a short memo plus three empty parts:

- [Build findings](https://github.com/STP-KAS/tn10-storm-build-bot-challenge/blob/main/findings/build.md) — Build's result, brought across once this page has it.
- [Grok Bot findings](https://github.com/STP-KAS/tn10-storm-build-bot-challenge/blob/main/findings/grok-bot.md) — the bot's result, brought across the same way.
- [Leg 3](https://github.com/STP-KAS/tn10-storm-build-bot-challenge/blob/main/findings/leg3.md) — the challenge. Each side names the claim, the file it reads, and the figure it gets. A figure enters the merged result only when both sides read the same file and get the same figure. A figure they still dispute stays, with both readings.

This page will keep one line pointing at whatever survives. It will not fold the two write-ups into one voice.

The challenge repo does not start a storm, and it does not hold a key.

## Open builder leg

**A separate idea. Not Leg 3, and not on the calendar.**

First this measurement: one run, in order, raw data published, then the Build and bot challenge above.

After that, one idea is an open leg on TN10. Builders, core contributors and others would be invited to test their own apps under high congestion, for example covenants, dapps, vProgs such as tic-tac-toe, KaChat, dotK, Kasperolabs, and others. Each app would see how it behaves when blocks are full and fees rise, next to the same public measurements (accepted tx/s, confirmation time, order, mempool). Who takes part, when and how would be agreed openly first.

Kaspa Pulse has offered to cover this open builder testing leg as the independent side, if it happens.

## Measured data

Charts, per-minute tables and the file list. Storm 1 is 25–26 Sep 2026. Storm 2 is 1–3 Oct 2026. Nothing in this part is the 9 or 13 Oct run.

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
| 3 | Does the indexer freeze, at what tps, for how long | **Partly answered** | Yes. api-tn10 froze for **86 min** (Fri 2 Oct 20:01–21:27 UTC, lag up to **4,311 s**, HTTP 503) while our box sent **~2,435 tx/s** and n0 "Processed" **~6,546 tx/s**. Shorter stalls happened at lower loads. On 25 Sep it froze for **at least 3 d 15 h**. We have no load threshold and no cause. |
| 4 | Mempool depth over time | **Answered** | Sampled every 15 s for the whole storm. Peak **99,992** (Thu 1 Oct 23:35:47 UTC). A ~71k backlog sat for ~6 hours after our miners stopped. **486,140** evictions in L1. |
| 5 | Send order vs accept order: does order hold under load? | **Partly answered (coarse)** | From the 25 Sep fee probes, sent 30 s apart: at 1× and 1.2× the floor (at or below the storm's fee) **2.6–10.4%** of consecutive probes were accepted out of send order, and some waited behind later probes for up to **169 s**. At 2× the floor and above: at most 1 reversal in 116 pairs (step A), none in step B. The October storm did not log order. |

Kaspa Pulse is most interested in the 1× vs 1.5× fee question. The nearest thing we have is a 25 Sep probe at 1.2× (equal to the storm's own fee) and 2× (1.67× the storm's fee). Paying 1.67× the crowd's fee cut the median wait from **7.1 s to 3.1 s** and the worst case from **92 s to 48 s** ([Q2](#q2-confirmation-time-per-load-step-normal-fee-vs-15)). A real 1× vs 1.5× A/B split at each load step is the main item in the [next storm plan](plan/NEXT-STORM-PLAN.md).

## Did our earlier storm repos already cover this?

"Storm 1" is the 25–26 Sep run. "Storm 2" is the 1–3 Oct run. "Build" is the Grok Build agent on stp's desk PC.

| Question | Storm 1 repos ([round1-public](https://github.com/STP-KAS/grok-bot-vprogs-round1-public), [round2](https://github.com/STP-KAS/grok-bot-vprogs-round2)) | Storm 2 ([public report](https://github.com/STP-KAS/tn10-storm-2026-10-public-report)) | Build ([build opinion](https://github.com/STP-KAS/tn10-vprogs-build-opinion), desk logs read in the public report) |
|---|---|---|---|
| 1. Accepted vs submitted | Network "Processed" tx/s and supervisor totals. No submitted vs accepted series over time | Leg totals and peaks (submitted 59,137,819 / included 58,905,910), and a 5-min included tx/s series (`data/box_5min.csv`). **No submitted vs accepted over time, no flattening view, no charts** | The desk sender logged **submit-OK**, not inclusion. Its local P2W meter counted virtual-chain inclusions, peak 2,795.6/min. No submitted vs accepted series |
| 2. Confirmation time by fee | **Yes, fee-tier probes** (1×–100×, 117 per tier), [`findings/overload-30m-summary.md`](https://github.com/STP-KAS/grok-bot-vprogs-round1-public/blob/main/findings/overload-30m-summary.md). First 57.5 min only. No 1.5× tier | Not covered | Not covered |
| 3. Indexer freeze | Not in these repos (the 25 Sep freeze is in a private working note, summarised in the storm 2 public repo) | **Yes**: stall windows, durations, box tps and n0 tps in each window (`data/api_windows_vs_load.csv`) | The build opinion notes the public health document stayed frozen. No timings of its own |
| 4. Mempool depth | Per-10-min medians/maxima in the overload summary | Per-window medians/p95/max and evictions (`data/mempool_windows.csv`). **No over-time chart** | Not covered |

So the pieces were mostly there, spread over several repos. This repo pulls them into one place, adds per-minute series and charts, and the second load step of the 25 Sep fee probes (20:47–21:50 UTC), which no earlier write-up had in full.

---

## Q1. Accepted vs submitted tx/s over the whole storm

**Status: partly answered.**

![Submitted vs accepted per minute](charts/1-submitted-vs-accepted-over-time.png)

![Where acceptance flattens](charts/1b-acceptance-flattening.png)

**What was logged.** Each box runner printed a report line every 10 s (`stress-tests/data/runner1-4.out`, `p2w1-8.out`) with cumulative counters:
- `submitted`: transactions the node accepted into its mempool (submit OK).
- `accepted`: our transactions whose id then appeared in n0's `virtual-chain-changed` notification, i.e. accepted by the selected chain. The engine code is `r5-engine.mjs` (class `Engine`).
- `rate`: the most that runner was allowed to send at that moment (its token-bucket cap).

[`scripts/extract.py`](scripts/extract.py) splits each runner's log into segments at restarts, spreads each 10-s increment evenly over its seconds and sums all runners per minute → [`data/oct_box_submitted_vs_accepted_1min.csv`](data/oct_box_submitted_vs_accepted_1min.csv) (1,801 minutes, Thu 1 Oct 18:00 UTC → Sat 3 Oct 00:00 UTC). Check: the per-minute file sums to 59,149,806 submitted and 58,917,966 accepted. That matches the leg totals in [`data/oct_legs_from_public_report.csv`](data/oct_legs_from_public_report.csv) (59,137,819 / 58,905,910), except for a ~12k-tx smoke run before L1 (12,019 txs, Thu 18:14–18:16 UTC).

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
- **Claim (measured on TN10):** the best clock-aligned minute in our file is **4,227 accepted tx/s** (Thu 1 Oct 23:25 UTC). The best sliding 60 s is **4,252.8** (from 23:24:46 UTC), best 5 min **3,843**, best hour **2,517.6** (L4, from 19:57:12 UTC) (`data/oct_legs_from_public_report.csv`). Those peaks came with 7 runners, a 30× fee burst and our own miners making ~60% of blocks (see [How the TPS was reached](#how-the-tps-was-reached)).

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

**Step A: 19:48:41–20:46:14 UTC.** The storm paid 120 sompi/g (1.2×). n0 "Processed" ~6,460 tx/s average ([`data/sep_network_processed_tx_s_1min.csv`](data/sep_network_processed_tx_s_1min.csv)). Mempool median ~63k, max 99,662.

| Tier | Feerate | vs storm fee | Probes | p50 | p90 | Worst | > 30 s |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1× | 100 | 0.83× | 117 | **7.0 s** | 29.8 s | **105 s** | 11 |
| 1.2× | 120 | 1.00× | 117 | **7.1 s** | 21.8 s | **92 s** | 6 |
| 2× | 200 | 1.67× | 117 | **3.1 s** | 9.5 s | **48 s** | 2 |
| 5× | 500 | 4.17× | 117 | 1.35 s | 2.3 s | 39 s | 1 |
| 10× | 1,000 | 8.33× | 117 | 1.2 s | 1.7 s | 3.7 s | 0 |
| 100× | 10,000 | 83× | 117 | 1.2 s | 1.7 s | 3.7 s | 0 |

**Step B: 20:47:26–21:50:41 UTC.** The storm paid 200 sompi/g (2×). n0 "Processed" ~7,420 tx/s average (this includes the stop at the end). Mempool median ~53k, max 80,781.

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
- L4 (Fri 19:57 → Fri 23:06 UTC, 200 sompi/g, ~2.5M txs per runner): p50 **6.0–7.1 s**, p95 **12.4–13.6 s**.
- L3 (Fri 09:52 → 14:50 UTC, 200–392 sompi/g, the six main runners): p50 **8.1–10.4 s**, p95 **16.4–20.7 s**.
- L1 night after our miners stopped (Thu 23:10 → Fri 05:53 UTC; fee 6,000 → 200): p50 **~5 s** and p95 **893–953 s** for 6 of the 7 runners. The seventh shows p50 1.7 s / p95 101 s.

**Not logged in October: confirmation time per load step, and confirmation time by fee level.** We say this plainly. The next storm plan fixes both.

## Q3. Does the indexer freeze?

**Status: partly answered.** "Indexer" here is the public TN10 REST API **api-tn10.kaspa.org** (a kaspa-rest-server with its own database). It is not our node. We have no access to its logs.

![Indexer freeze windows vs tps](charts/3-indexer-freeze-windows-vs-tps.png)

**What was logged.** Every 120 s, `GET /info/health` → HTTP status and `acceptedTxBlockTimeDiff` (seconds the indexer's newest accepted transaction lags behind) (`stress-tests/data/api-health-min.jsonl` → [`data/oct_api_tn10_health_2min.csv`](data/oct_api_tn10_health_2min.csv), with our box's accepted tx/s and n0 "Processed" tx/s for the same minute). Stall windows come from the storm 2 public report: [`data/oct_api_tn10_stall_windows.csv`](data/oct_api_tn10_stall_windows.csv).

**Freezes and stalls, 1–3 Oct** (box tps and n0 tps are the averages inside each window):

| Window (UTC) | Length | What happened | Box accepted tx/s | n0 "Processed" tx/s | Back to normal |
|---|---:|---|---:|---:|---|
| Thu 20:29–21:31 | 62 min | lagging, not frozen: lag rose and fell between 137 and 704 s, intermittent 503 | 1,477 | 3,591 | Thu 21:33 |
| Thu 21:03–21:29 | 26 min | continuous 503 (inside the window above) | 951 | 2,705 | Thu 21:33 |
| Thu 21:53–22:09 | 16 min | stall + 503 again (our sampler then stopped for 51 min) | 2,421 | 4,217 | Thu 23:00 (our sampler was off 22:09–23:00 UTC) |
| Thu 23:22–23:30 | 8 min | 503 with slow (18 s) replies, then stall, during the 30× fee burst | 2,161 | 5,427 | Thu 23:32 |
| Fri 07:55–07:57 | 2 min | stall right after the L2 peak | 1,645 | 4,948 | Fri 07:59 |
| Fri 10:25–10:47 | 22 min | two 503s + intermittent stall, lag 22–170 s | 2,005 | 5,340 | Fri 10:49 |
| **Fri 20:01–21:27** | **86 min** | **full freeze**: 503 on every sample from 20:09 to 21:27 UTC; lag grew ~120 s per 120-s sample, max **4,311 s** at 21:21:49 UTC | **2,435** | **6,546** | **Fri 21:29** |

- **Claim (measured on TN10):** **yes, it froze.** The longest freeze in the October storm was 86 minutes, while our box held ~2,435 accepted tx/s (best 5-min bin 3,238 at 21:15 UTC) and n0 "Processed" ~6,546 tx/s. Whenever our sampler was running, health came back within 2–4 minutes of the last bad sample.
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
- **Claim (measured on TN10), storm 1:** on 25 Sep the indexer's accepted-transaction pointer froze at **19:55:38 UTC**, while our storm ran at about 6k "Processed" tx/s. It was still frozen (HTTP 503, lag 313,244 s ≈ 3 d 15 h) when we checked on 29 Sep at 10:56 UTC. We don't know when it recovered. Block ingestion kept going; only accepted-transaction processing was stuck. The earliest healthy sample we have after that is 1 Oct 16:27:39 UTC. (Our private working note on that freeze, summarised in the [storm 2 public report, §4](https://github.com/STP-KAS/tn10-storm-2026-10-public-report#4-public-api-api-tn10kaspaorg).)
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
| L1, 30× fee burst Thu 23:10–23:30 UTC | 64,992 | 75,560 | 77,480 | 0 |
| L1 night, box miners off | 71,498 | 84,142 | **99,992** | **427,059** |
| L2 | 2,176 | 59,180 | 96,293 | 0 |
| L3 loaded | 4,448 | 42,153 | 76,461 | 0 |
| L4 loaded | 17,140 | 25,993 | 30,826 | 0 |

- **Claim (measured on TN10):** peak **99,992** at Thu 1 Oct 23:35:47 UTC, just under n0's ~100k cap (`--ram-scale=0.1`). Storm-watch flagged a ">80k" pause in 50 of the 1,801 minutes.
- **Claim (measured on TN10):** **the backlog is the main story of the L1 night.** After our miners stopped at 23:31:50 UTC, a ~71k mempool sat for about six hours (00:00–05:30 UTC) while our inclusion fell to ~300 tx/s and blocks were only 11–26% full. Over that night n0 evicted 427,059 low-feerate transactions to make room for higher-feerate ones. L1 as a whole had **486,140** evictions.
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
- **Needs more testing:** per-step reorder rate, out-of-order accepts and stalls at 1× vs 1.5×, with send sequence numbers and exact accept positions. That is now a first-class goal of the [next storm](#how) (above).

---

## How the TPS was reached

### (a) How TN10 ops runs a storm (stp's box)

Sources: `build-brief-how-box-storm-works-2026-10-02.md` (written from the running code), `storm-p2w-runner.mjs`, `r5-engine.mjs`, `storm-watch.sh`, `timeline.md`, the storm 2 public report.

- **One node, one box.** All load went into **n0**, our own TN10 kaspad 2.1.0 on the box (8 vCPU Xeon VM, 16 GB RAM, 126 GB disk). It runs without a UTXO index, with `--ram-scale=0.1` (mempool cap ~100k). The miners, runners and samplers ran on the same box.
- **Workers ("runners").** A runner is one Node.js process with **1,250 lanes** (1,500 for runner 1) and **4 wRPC connections** to n0. A single connection tops out at ~378 tx/s. **6 runners** was the default. **7 was best overnight in L1** (3,845 tx/s at Thu 23:26 UTC vs 3,375 with 6; `timeline.md`). In L3, 7 added nothing (2,383 vs 2,410) and 8 collapsed throughput to 1,165.
- **Lanes = independent coin chains.** Each lane holds exactly one coin. Its next transaction spends the previous one's output, with one transaction in flight per lane. The runner waits only for the node's "accepted into mempool" reply, not for a block, then builds the child. It tracks every lane's tip locally and never asks the node for UTXOs during the run.
- **Self-transfer transactions.** Each hop is **1 input → 1 output** back to the same lane address, no payload, no change. "P2W" lanes use an anyone-can-spend script tag (`push4(laneId) OP_DROP OP_TRUE`), so hops need no signature and weigh **643 grams** of mass. A signed 1-in-1-out weighs ~1,700 g, so P2W fits ~2.6× more transactions into a block. Early L1 also used signed "SMX" runners.
- **Coin feeder (UTXO prep).** A feeder (`coinbase-feeder.mjs`) hands each new lane one whole mature coinbase coin from our own mining address (median 3.087 tKAS). One funding transaction (1,701 g) per lane, no fan-out. A lane retires below 0.3 tKAS and re-funds.
- **Fee.** A fee daemon reads `getFeeEstimate` every 30 s and sets `feerate = min(FEE_MAX, max(2 × 100, 2 × clamp(normal, 100, 200)))`, i.e. **2× the normal estimate, with the base clamped so our own load can't run it up**, cap 400. Average paid feerate was **337–386 sompi/g in L2–L4** and **1,090 in L1** (`data/oct_legs_from_public_report.csv`). L1 includes a 30× period (up to 6,000 sompi/g) on the night of 1–2 Oct, which the build brief describes as a runaway from multiplying the raw estimate. The clamp was added after it. In storm 1 (25–26 Sep) the fee was 1.2×, then 2×, then **10× = 1,000 sompi/g** from 25 Sep 22:14 UTC (storm 1 handoff log).
- **Mempool backoff.** A pace band slows every runner linearly as n0's mempool grows, from full rate at the low mark to zero at the high mark. The marks changed between legs: 45k/72k in L2; 25k/45k, then 10k/20k in L3; 10k/20k in L4 (`timeline.md`). Each runner also hard-pauses above 75k and resumes below 55k (`r5-engine.mjs`; the build brief describes a later 90k setting). Storm-watch pauses everything above 80k until it falls below 55k (`storm-watch.sh`).
- **Stop and disk/memory guards** (`storm-watch.sh`, `timeline.md`):
  - runner pause at free disk ≤ 21 GB (briefly 19.5 GB on 2 Oct);
  - STOP when free disk stays under **19 GB for more than 900 s** (pruning-window seconds don't count);
  - immediate STOP at 10 GB;
  - STOP when free RAM < 1 GB, or when n0 is unsynced or more than 300 s behind for 2 ticks;
  - rate cut to 25% in the pruning windows (05:05–06:10 UTC and 17:05–18:10 UTC).
  
  The scaler drops the newest runner if the sink age exceeds 2.5 s. Every October leg ended on a disk pause or a disk or RAM STOP.
- **Our own miners.** stp's miners made **50–63% of TN10 blocks** while the box miners ran: L1 P2W 60.3%, L2 62.8%, L3 58.1% (`block_share_legs.csv` in the public report; L4 52.6% from the independent sampler there). When the box miners stopped (Thu 23:31:50 UTC), our inclusion fell to ~300 tx/s although blocks were mostly empty.
- **Block mass is the ceiling.** TN10 blocks fill by mass at ~490–500k per block. Past the knee, more senders only grow the mempool. At 8 runners, blocks hit 492k mass, the block rate fell from 9.1/s to 7.8/s, and throughput halved (build brief §7).

### (b) How Build generated its load (stp's desk PC)

Sources: our prompts to Build (`grok-build-tx-sender-2026-10-02.md`, `grok-build-prompt-v2-2026-10-02.md`, and the storm 2 "desk sender part 3" prompt), the desk check in the [storm 2 public report](https://github.com/STP-KAS/tn10-storm-2026-10-public-report#desk-check-later-the-same-day), [round2](https://github.com/STP-KAS/grok-bot-vprogs-round2) ("Confounder: Grok Build agent") and the [build opinion](https://github.com/STP-KAS/tn10-vprogs-build-opinion).

- **Machine:** Intel Core i7-13700K (16 cores / 24 threads), 32 GB DDR5, Windows 11 Pro, 1 Gbps Ethernet (from stp's screenshot; not checked by us). It also ran 20 CPU miners at about 75% CPU (stp's figure).
- **Wallet:** Build's own TN10 wallet, funded by us (299,993 tKAS on 25 Sep, round2; ~1.2M tKAS on 1–2 Oct, sender prompt).
- **What we asked it to run** (the prompts): 1-input → 1-output signed self-sends in chained lanes, sent to **public TN10 nodes** found through the Kaspa resolver, never to our n0.
  - First version: up to 400 lanes, at most 1,000 tx/s per process, fee 2× normal capped at 600 sompi/g.
  - v2: a coordinator plus auto-scaled workers, each with 4 connections and 250 lanes; flat 1.5× normal fee, cap 600; pause above 80k mempool.
- **What its logs show** (desk check in the public report):
  - a sender log with **17,415,510 submits** (Thu 18:38 → Fri 10:03 UTC). Its `accepted` field is a submit result, not inclusion.
  - a public-node runner whose status lines reached **24,249 submit-OK per second** (Fri 13:35:44 UTC, 24 workers). That is above any inclusion ceiling we measured, so it's a submit rate.
  - a "local P2W scale" path counting inclusions on the desk's own local node, peak **2,795.6/s** for a minute (Fri 19:33 UTC, feerate 150); 2,698.6 during L4.
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
| [`plan/FINISH-TASKS-PROMPT.md`](plan/FINISH-TASKS-PROMPT.md) | Paste-in prompt for Grok Build to close the desk side of the seven pre-storm tasks. It does not start the storm |
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

---

Intentions are good; thought process is questionable. STP remains delusional. Si vis pacem, para bellum.
