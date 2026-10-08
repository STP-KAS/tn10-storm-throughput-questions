> **Experimental. We are just trying this.**
>
> Good intentions, shaky hands. STP does not know what he is doing. We test, we write down what we think we saw, and that is the whole product. A number here is not the truth. A chart is not the truth. Any other sentence that sounds sure of itself is not the truth either. Do not count any of it as a claim.
>
> [Disclaimer](../DISCLAIMER.md)

Wording, Kaspa Pulse (@gokugalax), 7 Oct 2026: sign-and-send processes are senders; runner is the setup; bot is reserved for the operator.

# Kaspa Pulse, inputs

Kaspa Pulse ([@gokugalax](https://x.com/gokugalax)). Thank you. These are his messages in the X chat, in the order the screen shows them. The screen is the recording of 8 Oct 2026, 08:23. Sunday on that screen is 4 Oct 2026. Monday is 5 Oct 2026. Yesterday is 7 Oct 2026. The clock on the screen is local (UTC+2). This note does not start the storm.

The five measured questions stay in the [README](../README.md#questions-from-kaspa-pulse-gokugalax). The plan is [NEXT-STORM-PLAN.md](NEXT-STORM-PLAN.md). If this note and the plan disagree, the plan wins.

Where a line of his says "bot" before 7 Oct 2026, 19:54 UTC, the 19:54 message is the correction. A process that signs and sends is a sender. TN10 ops stays the operator.

## 4 Oct 2026, shown as Sunday

**12:28 PM, his reply dated Oct 4, in the chat as a reply to @KASPAglobal.**

Common thread in all three: the rule sits on L1, not with an operator. Pay on delivery, unlock on proof. The next useful question is throughput, how many of those conditional payments one contract can take per minute before they start colliding.

**9:14 PM (19:14 UTC).**

Nice, this is exactly the throughput question worth answering. For the TN10 run on the 13th, the numbers I'd love to see:

- Accepted transactions per second vs submitted, over the whole storm, so we can see where acceptance flattens out
- Confirmation time at each load step (median and worst case), normal fee vs 1.5x
- Does the indexer freeze, and if so at what sustained tps and for how long
- Mempool depth over time, so the backlog is visible, not just the throughput

The fee comparison at 1x and 1.5x is the interesting one, it shows whether paying more actually buys inclusion under load.

On the mainnet congestion costing, I'll pass on that one, not something we'd want to put numbers to on the live network. Happy to dig into all the testnet results with you though.

## 5 Oct 2026

**10:20 AM (08:20 UTC).**

Sounds good, good luck with the build. The setup's in your hands now, I'll stay out of it so the run is yours. Ping me with the numbers after the 9th or the 13th and we'll go through them.

**11:40 AM (09:40 UTC).**

Love that you spun up a repo for it, and thanks for the credit. The sequencing point is the real one. Headline tps hides it, but if a one-minute storm reorders or stalls what a dapp expects in order, that's what actually breaks apps, not the raw throughput. So the metric isn't just how many land, it's whether order holds under load.

On the mainnet idea: I'd keep the deliberate storms on tn10. Measuring the ceiling there tells you the same thing without poking the live chain, and it keeps the finding clean rather than controversial. Once you've got the numbers from the 13th, I'd love to go through them with you, and if they hold up we'd put them in front of our audience with your name on the method.

**2:38 PM (12:38 UTC).** Six points.

Happy to. Before the 13th, send me the plan as a short list (load steps, duration, fee tiers, what you log) and I'll do one pass on it. A few things that make results hard to argue with:

1. Write the plan down before you run it and publish it with the results, so nobody can say the window was picked afterwards.
2. Baseline first: 10 minutes of normal traffic with the same measurements, so the storm has something to compare against.
3. Fixed steps instead of one blast, e.g. 1x, 2x, 5x, 10x normal load for a set time each. That shows where it bends, not just that it bends.
4. Log submitted and accepted per second with UTC timestamps, and for the ordering question, the order you sent vs the order they were accepted.
5. State your mining share up front. With ~60% of TN10 hashrate, your miners decide a lot of what gets in and in what order, so the result describes TN10 with you on it, not mainnet. Saying that openly makes the finding stronger, not weaker.
6. Publish the raw data next to the summary.

**5:01 PM (15:01 UTC).** The screen cuts this bubble at "Show more". The visible opening asks for four tightenings before the lock: the miners-off step in the main run, the box kept separate from the chain, clocks synced, and saturation defined before the start. The working copy of those four is [the plan's tightening table](NEXT-STORM-PLAN.md#kaspa-pulses-four-tightenings-review-of-5-oct-before-the-lock). The lines hidden behind "Show more" are not copied here.

## 7 Oct 2026

**9:16 AM (07:16 UTC).**

No need to apologize, that pushback is right. Without your miners a high load step would only measure backlog. The low load control with a matching miners-on step is the cleaner design. Labelling it as an imperfect control is exactly how it should be read.

Weekly runs sound good. I'd rather see one clean run first and go through those numbers properly before we stack more. Send me the results when it's done and we'll take it from there.

**4:25 PM (14:25 UTC).**

haha that makes two of us most days. the questions in your plan are the hard part, the rest is plumbing. one thing we'd like to add from our side: we count the run straight from the chain while it happens, accepted per second, confirmation times, fees. a second independent count next to your bot's numbers, nothing touches your setup. after the run we put both side by side, you credited. sound good?

**5:21 PM (15:21 UTC).**

perfect, deal. two quick things so we count the same window: when did this one start (utc), and is it still running? we'd like to point our counter at it as a dry run, so we're sharp for the 9th/13th

**9:23 PM (19:23 UTC).**

you did, all clear, thanks. our dry run counted 18:52 to 19:22 utc, right inside your run. once your log for that window is on git we'll put both side by side and send you the comparison first. and the 2,750 ceiling with the pool stuck at 9.7k is exactly the kind of thing we'd love to pin down, chain or node. no spam at all, keep it coming

**9:27 PM (19:27 UTC).**

first dry run done, clean on our side. for the 18:53 to 19:23 utc window we count what the chain actually accepted, and it came out much lower than your screenshot, so before we read anything into it we want to line up the same window. could you share, when you have a sec: start and end of your run, the target tx/s, whether your bot counts sent or accepted, which node it sends to, and a handful of tx ids from that window? then we check those ids on chain one by one. might just be that the bot stalled when your pool got stuck

His "bot" in the 14:25 and 19:27 lines is the sender. He says so at 19:54 UTC.

**9:54 PM (19:54 UTC).**

sleep well, no rush at all. on wording I'd go with "senders" for each wallet process that signs and sends, your own log already says "four signed senders". keep "runner" for the whole setup if you like. "bots" makes people think spam, "senders" says exactly what they do

The reading of the 18:52 and 18:53 windows is [PULSE-WINDOW-7-OCT.md](PULSE-WINDOW-7-OCT.md). Our log ends at 18:38:39 UTC. His window is not in it. The 2,753 `included_s` sum and the mempool 9747 line are different minutes.

Intentions are good; thought process is questionable. STP remains delusional. Si vis pacem, para bellum.
