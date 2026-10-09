> **Experimental. We are just trying this.**
>
> Good intentions, shaky hands. STP does not know what he is doing. We test, we write down what we think we saw, and that is the whole product. A number here is not the truth. A chart is not the truth. Any other sentence that sounds sure of itself is not the truth either. Do not count any of it as a claim.
>
> [Disclaimer](DISCLAIMER.md)

Wording, Kaspa Pulse (@gokugalax), 7 Oct 2026: sign-and-send processes are senders; runner is the setup; bot is reserved for the operator.

# TN10 storm tasks

Source: Kaspa Pulse ([@gokugalax](https://x.com/gokugalax)), X DM, 4–7 Oct 2026.

Kaspa Testnet-10 only. Every clock on this page is UTC. Deliberate load stays on TN10. This page states no mainnet storm and no mainnet cost numbers.

Method points below are his. Where a number comes from the measurement plan, the sentence says so.

On the 8 Oct 2026 screen of that X chat, the Monday 5 Oct 2026 17:01 local message (15:01 UTC) opens his four tightenings and stops at "Show more". The lines under that control were not copied from the screen. The working copy is the plan's table, [Kaspa Pulse's four tightenings](plan/NEXT-STORM-PLAN.md#kaspa-pulses-four-tightenings-review-of-5-oct-before-the-lock). His example steps, on the Monday 5 Oct 2026 14:38 local frame (12:38 UTC), were 1×, 2×, 5×, and 10×. The plan's table is a 10-minute baseline, then 2×, 5×, 10×, 20×, 30×, then max. This page follows the plan's table.

The measurement plan is [plan/NEXT-STORM-PLAN.md](plan/NEXT-STORM-PLAN.md). If this README and the plan disagree, the plan wins.

Each wallet process that signs and sends is a sender. This page calls the whole setup a runner. TN10 ops is the operator. The plan keeps its own process counts. If those words and the plan disagree, the plan wins.

His questions, method, tightenings, 7 Oct compare, and cadence are [plan/PULSE-README.md](plan/PULSE-README.md). The 7 Oct window reading is [plan/PULSE-WINDOW-7-OCT.md](plan/PULSE-WINDOW-7-OCT.md). The measured front page through commit `5cc9ebd` stays in that commit, including the Goal section and his 19:23 and 19:27 UTC messages.

This page does not start the 9 Oct storm or the 13 Oct storm. There is no storm GO here.

Forward routing, 9 Oct 2026, is in the plan. The desk runs two kaspad processes. locus is the first. keel is the second. Build uses locus. The bot's runner and the bot's miners use the tunnel to keel. n0 will not run. keel stays in the score while it syncs. Those minutes add 0 and the row says waiting. The monitoring tasks are in that same section. Where this README still says the box sends through n0, or Build posts to public nodes, the plan's forward section wins.

## 1. Bot

TN10 ops, the operator, on the box. It sends the box share through the tunnel to keel, the second desk kaspad, and only while keel is synced and the handoff lists that tunnel. The box share is the added load that remains after Build's share in section 2. n0 will not run. While keel is still syncing, this side waits and that minute's score is Build on locus alone.

**Sent and accepted stay separate counters.** Kaspa Pulse counts what the chain accepted. A submit acknowledgement is the other counter. The log writes both.

**What the box logs.** His request, and the plan's §6a and §7. CPU, mempool-cap hits, and reject reasons on the node this side posts to, so a later flat accepted rate can be labelled. On this run that node is keel. The plan's older n0 wording stays in the plan as the record. Mining share on every step, including the miners-off step. He had put the share near 60% of TN10 hashrate. Storm 2 measured 50–63% of TN10 blocks (`block_share_legs.csv`). **Claim (measured on TN10).** The result says which figure it uses. The figure is TN10 with our miners on.

**Miners-off control.** His tightening: in the main run, at low load, matched to a miners-on step at the same load. A high load with our miners off measures backlog. The plan's matched step is the 2× step (§3b). If 2× of baseline B would pass 250 tx/s total, both halves run at 250 tx/s total, and that is recorded. The control is imperfect. Other miners still change templates. When our miners stop, TN10's block rate moves until difficulty adjusts. A difference between the two halves is evidence. The plan marks this **Not sure / open for debate.**

**Stop and report if the pool sticks.** On 7 Oct 2026 at 19:23 UTC he asked to pin a 2,750 figure, and a pool stuck near 9.7k, as chain or node, before anyone calls either a ceiling. The desk readings are two other minutes. The `included_s` sum 2,753.0 is 15:20:32 UTC (`status.log`, tags m38, m36, and m37). Mempool 9747 is 15:25:33 UTC. The file does not contain the digits 9700. The pool name on the 9747 line is MISSING. The reading is [plan/PULSE-WINDOW-7-OCT.md](plan/PULSE-WINDOW-7-OCT.md).

**18:52–19:22 UTC.** He asked for the start, the end, the target tx/s, the node, and sample transaction ids from that dry-run window, so his chain count and our log use one window. Those fields are MISSING. The desk log's last submit is 18:38:39 UTC. This page prints no transaction id from inside his window. Ids from before that window are in the window note, marked outside it. The shape of a later dry-run log is [plan/TESTDAY.md](plan/TESTDAY.md). That file does not send.

## 2. Build

Grok Build, on the desk PC. The wallet processes here are senders.

**Four signed senders, fixed for the storm.** The plan's Build task (§3a), and the 6 Oct desk dry run, fix the count at four. That count is the plan's, and it is the dry-run pick. No auto-scale. No fleet relaunch. No mempool pause inside a step. Each sender has its own coins and its own log.

**Share of the added load.** The plan's default is 25% of each step's added load, capped at the rate the dry run held. The box sends the rest. The max step in the plan leaves both sides uncapped. The 25% figure is the plan's default.

**Fees.** Frozen for the step. Half the lanes at 1× and half at 1.5× of that step's fee estimate. The sompi pair and the 600 sompi/gram cap stay the ones in the plan. This page states no mainnet fee.

**Ordered stream.** Its own process. The rate and the coin rules are the plan, §4a and §3a.

**Timetable.** The same UTC timetable as TN10 ops. T0 and the step ends are the plan's table.

**Gate.** The plan's go/no-go, written before the lock. At every step, the mean achieved send rate is at least 95% of the target, with no zero seconds. The per-transaction logs are complete. The transaction ids match what that side's own node sees accepted: locus for Build, keel for the bot. The older match on n0 is not a gate. n0 will not run. Starts and stops follow the UTC timetable. Miss the gate, and the storm waits for 13 Oct. Build's storm cap is the rate it held.

This gate is 95% of the target. Saturation, in section 3, is a different rule.

The 6 Oct desk mean for four senders is on the measured front page in commit `5cc9ebd`. The match of those ids on n0 is still open there. This page leaves the gate open.

## 3. Monitor

**Two clocks.** Ours, and Kaspa Pulse's. His counter reads the chain only. It does not touch the setup. After the run the two counts go side by side, and he sends the comparison first.

**NTP.** His tightening, and the plan's §4. Log the NTP offset on the box and on the desk at the start and at the end. Cross-machine confirmation times are corrected for the offset, or flagged, by the plan's rule.

**Each second, UTC.** Submitted, and accepted, as two fields. Mempool depth: keel for the bot and locus for Build, every 1 second. The plan's older §6 sample of n0 stays in the plan as the record. Indexer freeze is his question. The plan's sample is api-tn10 health every 30 seconds, and one visibility check a minute (§6). Mining share is logged per second and published per step (§7).

**Each transaction.** Send sequence, submit time, accept time, and fee tier. His logging point, and the plan's §4. The 7 Oct transaction log has submit times. Accept time on that log is MISSING. The storm log records accept time.

**Saturation, defined before T0.** His rule: accepted under 95% of submitted for 60 seconds. The plan writes that rule in §3c, with the window and the onset. About 90 probes per tier was his thin sample. The plan raised that to about 450 probes per tier per step. This page leaves the probe count at the plan's figure.

The Build gate in section 2 is 95% of the target. Saturation is accepted under 95% of submitted, held for 60 seconds. The two rules stay separate.

## 4. Results

Empty until the run.

**One clean run first.** His cadence, 7 Oct 2026. Fri 9 Oct 2026, 21:30 UTC, for 8 hours, ending Sat 10 Oct 2026, 05:30 UTC. If that day is not ready, Mon 13 Oct 2026, 21:30 UTC, for 8 hours, ending Tue 14 Oct 2026, 05:30 UTC. The plan's paced table is 2 hours 55 minutes and ends at T0+175, 00:25 UTC the next day. The hours after that table stay inside the 8-hour window. The plan names no phase for them. Weekly repeats wait until this run has been read. He stays out of the setup.

**Locked plan SHA.** The plan's §1. At T0 the run log writes the SHA of the last commit that changed `plan/NEXT-STORM-PLAN.md`. This section cites that SHA, with a link to the plan at that commit. The plan is still a draft. This page leaves the lock SHA blank. A deviation on the night goes in a deviations list, with the time and the reason.

**Side by side, before any reading.** His chain count and our count, on the same window. He sends the comparison first. We stay credited. A submit count and a chain-accepted count stay two numbers until the same ids are on both clocks.

**Box-bound or network-bound.** A flat accepted rate takes one of those labels, or unclear, by the criteria fixed in the plan's §6a.

**The miners-off control is imperfect.** Say that next to the pair. The plan's reasons are in §3b.

**Raw CSV next to the summary.** His publication point, and the plan's §8. The file list is in the plan. The files sit next to the summary in this repo.

TN10 ops writes its reading in the subsection below, from the box logs, with acceptance matched on keel. Build writes its reading in the subsection below, from the desk logs, with acceptance matched on locus. A waiting keel minute adds 0. Both stay empty until that run. The check of one reading against the other stays in [tn10-storm-build-bot-challenge](https://github.com/STP-KAS/tn10-storm-build-bot-challenge). That page stays empty until both readings are filled.

### TN10 ops

**Status: empty.**

### Build

**Status: empty.**

## Labels used in this README

| Label | Meaning |
|---|---|
| **Claim (measured on TN10)** | We measured it on TN10. The number and its source file are given. It holds for the conditions stated. |
| **Not sure / open for debate** | Reasonable, and the reason it might be wrong is given. |
| **Needs more testing** | The test that would settle it is named. |

---

Intentions are good; thought process is questionable. STP remains delusional. Si vis pacem, para bellum.
