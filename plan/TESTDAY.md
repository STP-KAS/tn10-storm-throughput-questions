> **Experimental. We are just trying this.**
>
> Good intentions, shaky hands. STP does not know what he is doing. We test, we write down what we think we saw, and that is the whole product. A number here is not the truth. A chart is not the truth. Any other sentence that sounds sure of itself is not the truth either. Do not count any of it as a claim.
>
> [Disclaimer](../DISCLAIMER.md)

Wording, Kaspa Pulse (@gokugalax), 7 Oct 2026: sign-and-send processes are senders; runner is the setup; bot is reserved for the operator.

# Test day: start this, and the desk run starts

Credit Kaspa Pulse ([@gokugalax](https://x.com/gokugalax)). The section below is a pending dry run. It is not the storm.

## Pending dry run, 8 Oct 2026

Not the 9 Oct storm. Not the 13 Oct storm. No storm GO. No 8-hour window. Do not start it from this file. The storm rules further down are unchanged, and they still wait for a separate storm GO and for `steps-utc.json`.

Kaspa Pulse's 7 Oct 2026 messages, 19:23–19:54 UTC, asked for one window and for sent versus accepted. The desk log does not cover 18:52–19:23 UTC. The reading is [PULSE-WINDOW-7-OCT.md](PULSE-WINDOW-7-OCT.md). A process that signs and sends is a sender. The runner is the whole setup.

If stp runs this dry run on 8 Oct 2026, the log is not usable unless it records all of the following.

Every UTC second, one line per sender:

- sender id
- target tx/s, submitted tx/s, and accepted tx/s, as three columns
- the node that sender posts to, by endpoint
- the local pool, and each public pool, each named
- submit-call latency

On a sample of transactions, and on every reject:

- tx id, submit time, and accept time

NTP offset at the start and at the end.

Submitted is not accepted. A stuck pool is named, so a stall is visible when the pool sticks. Do not raise the 3,500 bar. Do not treat 2,750 or 2,951 as a ceiling until his transaction ids and our transaction ids are the same ids.

This section does not send.

## The storm, still waiting on GO

For Grok Build on stp's desk. Fri 9 Oct 2026, 21:30 UTC, for 8 hours, ending Sat 10 Oct 2026, 05:30 UTC. If that day is not ready, Mon 13 Oct 2026, 21:30 UTC, for 8 hours, ending Tue 14 Oct 2026, 05:30 UTC. When the storm GO is given, the window is 8 hours from T0. T0 is 21:30 UTC. The paced table is still 2 h 55 min and ends at T0+175, 00:25 UTC the next day. The time after that stays inside the 8-hour window. The UTC times come from `steps-utc.json`. This is the run. Do not ask stp to paste commands.

The shape is [`DESK-SHAPE-9-OCT.md`](DESK-SHAPE-9-OCT.md). The measurement rules are [`NEXT-STORM-PLAN.md`](NEXT-STORM-PLAN.md) and [`GROK-BUILD-PROMPT.md`](GROK-BUILD-PROMPT.md). If this file and the plan disagree, the plan wins. Stop and ask stp.

## Before any send

1. Confirm stp has given the **storm GO**, separate from the dry-run GO, and has given `steps-utc.json` with the UTC start and end of every step. If either is missing, stop and ask for that one thing. Do not invent the timetable.
2. Confirm the day is the storm day and the clock is at or after the first time in `steps-utc.json`.
3. Use the same measurement sender that produced the 6–7 Oct holds. TN10 only. The Build wallet only. Do not spend the Bot wallet. Build sends on locus, on every step, while locus is synced and the UTXO index is on. The bot uses the tunnel to keel. n0 will not run. Never `bore.pub`. Never `159.223.110.159`.
4. One sender family. If a Build spender is already running, stop and ask. Do not start a second one on the same coins.
5. Leave the 3 Oct halt on the older fleet in place. Do not clear it.
6. The sender arms only when its own GO file is present, and halts when its own STOP file is present. A STOP from stp stops every process.
7. Desk miners stay as stp sets them. Log the count at each phase start. Do not switch them.
8. Per-transaction logs are **on** for the storm. The pre-run turned them off to save disk. The storm needs them.

## What to run

Follow `steps-utc.json`. Send nothing in B0, B1, and the settle phases.

**Paced steps**, including the 25% share. Four fixed processes for the whole paced schedule. No auto-scale, no fleet relaunch, no mempool pause inside a step.

- Depth **2**. In-flight **48**. **4** connections per process. Each lane stays on one connection.
- Each process has its own coin file.
- Fee: if the public quote at step start is the idle floor of 100 sompi/gram, freeze **200 and 300**. If the quote is already above 200, freeze that quote and its 1.5×. If 1.5× would pass **600**, stop and ask. Do not raise the cap.
- Half the lanes at each tier, and a lane keeps its tier for the step.
- Hold the step target. A step is sender-limited if submit-OK stays under 95% of target. Report that.

**Uncapped max step, and any long hold.** Two lane signers on each physical machine, plus the desk node when `measure.mjs --mode check --via own` succeeds. On 7 Oct 2026 the six hostnames were three machines: vector-10, muon-10, and one server for proton-10, electron-10, quark-10 and neutrino-10. Recheck that morning. The public-only shape held **2,210 tx/s submit and 2,207 tx/s seen accepted** from 2026-10-06T23:53:27.326 UTC to 2026-10-07T05:54:53.185 UTC. The desk node, added at 2026-10-07T07:57:46 UTC, saw **1,538 tx/s** accepted on its own feed, and the blocks then sat at about **305 transactions** and **498,000 / 500,000** compute mass.

- Split each node's coins by line into two files. Do not use `part i/2` on a host file.
- Depth **2**. In-flight **64**. **4** connections.
- Fee frozen at **200 and 300**, unless the step-start quote is already above 200. Same 600 cap. The 400 and 600 pre-run finished at 2026-10-07T16:38:59 UTC. Over the public lane logs, 2026-10-07T06:39:01.356Z to 2026-10-07T16:38:59.632Z, it was 668 tx/s submit and 273 tx/s seen accepted. Seen accepted is 0 after 08:05Z. It does not beat 2,207, so the storm fee stays 200 and 300.
- The pipes filled at about one core. Keep two signers per physical machine. Add a third on one machine only when that machine's lanes are not already two deep. Do not add signers to chase idle CPU. The desk node uses its own coin files and is not a third signer on a public machine.

**Ordered stream.** Its own process, its own coins, 4 tx/s, both tiers, depth 1, on proton-10. It counts inside the share.

**Nodes**, index 0 to 5: vector-10.kaspa.green, proton-10.kaspa.stream, electron-10.kaspa.blue, muon-10.kaspa.blue, quark-10.kaspa.red, neutrino-10.kaspa.stream. Path `/kaspa/testnet-10/wrpc/borsh`.

## Coins

Spend only mature coins of at least 2 tKAS that all six public nodes return. Stop the senders and let the mempools drain before a new split. A process restarted onto an old file spends outputs that are already in the mempool.

A sender started inside a short-lived shell dies when that shell closes. Keep the parent alive until the step ends.

## During the run

- Log every second: target, submit-OK, rejects by reason, seen accepted, depth, lanes, fee, CPU.
- Log every transaction: sequence, txid, submit start, submit result, tier, feerate, step, stream. UTC with milliseconds and `Z`.
- Watch the virtual-chain feed. If it goes quiet and depth stays full, that is the failure from 2026-10-06T23:08:02.667 UTC to 2026-10-06T23:11:51.851 UTC. Do not let it sit. The sender opens one hop after 15 quiet seconds and resubscribes after 20.
- Do not change N, depth, fee, or the target inside a step.
- Depth 8, a 45-second burst, and a fee of 2,000 are not this test.

## After the run

Write Build's result in this repo's Build result section, and the same run in [tn10-build-desk-tps](https://github.com/STP-KAS/tn10-build-desk-tps). Exact first and last log times for every step. The bot writes its own file. A figure enters the merged challenge only when both sides name the same file and recompute the same figure.

Do not fill those sections before the storm.
