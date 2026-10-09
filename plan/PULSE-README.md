> **Experimental. We are just trying this.**
>
> Good intentions, shaky hands. STP does not know what he is doing. We test, we write down what we think we saw, and that is the whole product. A number here is not the truth. A chart is not the truth. Any other sentence that sounds sure of itself is not the truth either. Do not count any of it as a claim.
>
> [Disclaimer](../DISCLAIMER.md)

Thank you, Kaspa Pulse (@gokugalax), for the guidance and the input over this stretch, from 4 Oct 2026 on. The 7 Oct 2026 wording stays: sign-and-send processes are senders; runner is the setup; bot is reserved for the operator.

# Kaspa Pulse

Source: Kaspa Pulse ([@gokugalax](https://x.com/gokugalax)), X DM, 4–7 Oct 2026.

TN10 only. No mainnet costing. No mainnet storm. This note does not start the 9 Oct or 13 Oct storm.

The measurement plan is [NEXT-STORM-PLAN.md](NEXT-STORM-PLAN.md). If this note and the plan disagree, the plan wins. The 7 Oct window reading is [PULSE-WINDOW-7-OCT.md](PULSE-WINDOW-7-OCT.md).

## Questions

1. Accepted tx/s vs submitted, whole storm, where acceptance flattens.
2. Confirmation time per load step, median and worst, normal fee vs 1.5×. Does paying 1.5× buy inclusion.
3. Indexer freeze: at what sustained tx/s, for how long.
4. Mempool depth over time, backlog not just throughput.
5. Order holds under load. Sent order vs accepted order. Headline tx/s is not the metric.

## Method, before the run

1. Write the plan first. Publish it with the results. Cite the commit SHA. List deviations.
2. Baseline first: 10 min normal traffic, same measurements, then the storm.
3. Fixed steps, not one blast. His example was 1×, 2×, 5×, 10×. The plan uses 2×, 5×, 10×, 20×, 30×, then max. A set time each. Show where it bends.
4. Log submitted and accepted per second, UTC. Log send order vs accept order.
5. State mining share up front. Storm 2 measured about 50–63% of TN10 blocks. He had put the share near 60% of TN10 hashrate. The result says which figure it uses. It is TN10 with our miners on, not mainnet.
6. Raw data next to the summary.

## Four tightenings

1. Miners-off is in the main run, not optional. Low load only, matched miners-on step at the same load. Imperfect control: other miners still change templates. Say that.
2. Separate the box from the chain. One node, capped mempool, ram-scale 0.1. When accepted flattens, log n0 CPU, cap hits, reject reasons. Label each plateau box-bound or network-bound.
3. Sync clocks. NTP on the box and the desk. Log the offset at the start and the end. Correct confirmation times or flag the drift.
4. Saturation defined before T0: accepted under 95% of submitted for 60 s. Reorder rates as counts and percentages, with n. About 90 probes per tier is thin. The plan raised that to about 450 per tier per step.

## Dry-run compare, 7 Oct

His counter: 18:52–19:22 UTC inside our run, and 18:53–19:23 UTC for what the chain accepted.

His chain-accepted count came out much lower than our screenshot.

He wants: start and end UTC, target tx/s, whether we count sent or accepted, which node we send to, and a handful of tx ids from that window.

His read: the sender may have stalled when the pool stuck. Pool stuck at 9.7k. The 2,750 figure is the one to pin as chain or node, not a ceiling, until those ids match.

His side counts the chain only. Nothing touches our setup. Side by side after the run. He sends the comparison first. We stay credited.

Our log does not cover 18:52–19:23 UTC. The last submit is 18:38:39 UTC. The 2,753 `included_s` sum is 15:20:32 UTC. Mempool 9747 is 15:25:33 UTC. Those are not one minute. The reading is [PULSE-WINDOW-7-OCT.md](PULSE-WINDOW-7-OCT.md).

## Wording

Senders are each wallet process that signs and sends. The log already says four signed senders.

Runner is the whole setup, if we want that word.

Do not say bots for a sender. It reads as spam. TN10 ops stays the operator.

## Cadence

One clean run first. Go through the numbers. Then weekly. Do not stack runs before that.

Ping him after 9 or 13 Oct. He stays out of the setup.

Intentions are good; thought process is questionable. STP remains delusional. Si vis pacem, para bellum.
