# Desk shape for the 9 Oct test

What worked on the Grok Build desk during the 6–7 Oct 2026 TN10 pre-run. Use this on the real test, **Fri 9 Oct 2026, 20:00 CEST**, or **13 Oct** if that is the date.

This file does not start the storm, does not lock the plan, and does not fill the result sections. The lock text is still [`NEXT-STORM-PLAN.md`](NEXT-STORM-PLAN.md). If this note and that plan disagree, the plan wins and Build stops and asks stp. The numbers below are the pre-run. The 10-hour total is reported in [tn10-build-desk-tps](https://github.com/STP-KAS/tn10-build-desk-tps) when that clock ends. It is not this file.

TN10 only. Public nodes only. The Build wallet only. The Bot wallet is not spent. One sender family. The fee cap stays **600** sompi/gram.

## Paced steps, the 25% share

The dry run on 6 Oct is the shape that cleared the gate.

- **4 processes**, fixed for the whole paced schedule. No auto-scale, no fleet relaunch, no mempool pause.
- Each process spends its own coins.
- **4** wRPC connections per process. Each lane stays on one connection.
- **Depth 2.** In-flight cap **48**.
- Fee tiers are half the lanes at F1 and half at 1.5× F1, frozen for the step.
- The ordered stream is its own process.

Held, over 3 minutes: **734 tx/s**, **97.9%** of 750, **0 rejects**, **0** seconds at 0. The steps at 25, 100, 225 and 475 tx/s each hit the target on every second. The n0 txid match is still the box's check.

## Long hold, and the uncapped max step

This is the shape that held the highest rate for minutes, with seen-accepted matching submit.

- **Two signers on each of the six public nodes.** Twelve lane processes.
- Each signer gets its own half of that node's coins, split by **line** into two files. Do not split a host file with `part i/2`. The host is already `txid % 6`, and that lines up with `% 2`, so one of the two parts is empty.
- **Depth 2.** In-flight cap **64** per signer. **4** connections per signer.
- Fee frozen at **200 and 300** sompi/gram. The cap stays 600.
- Ordered stream stays a separate process.

At 23:57 UTC on 6 Oct, mempools already full, last 20 seconds: about **2,420 tx/s** submit and **2,450 tx/s** seen accepted, **0 rejects**. The first minute of that same leg was about **2,530** submit and **2,500** seen accepted, also with 0 rejects.

The one-signer leg before it, depth 2 and in-flight 48, frozen at 100 and 150 (vector-10 at 136 and 204), ran about 39 minutes and closed at about **2,050 tx/s** included, with 0 rejects in the last 3 minutes. Moving to two signers and to 200 and 300 gained about **400 tx/s**. The gain was on proton-10, electron-10, quark-10, neutrino-10 and muon-10. Vector-10 came down.

The pipes were full again (depth equal to two hops on every live lane). The twelve signers used about **one core**. The desk was still near **5%** CPU. More signers do not raise the rate once the pipe is full.

A signed one-input one-output is about **1,624 grams**. A full 500,000-gram block at 10 blocks per second holds about **3,080** of them.

### Why 200 and 300

At an empty mempool the public quote was **100**. After this desk filled the mempools the normal quote sat near **186–194**, and the priority bucket was far above that. Signers frozen at 100 and 150 were under that quote for the rest of the leg. **200 and 300** is the pair that then held, and 300 is under the 600 cap.

On 9 Oct, use **200 and 300** for the long hold and for the uncapped max step. For a paced step, if the quote at step start is the idle floor of 100, arm at 200 and 300 as well. A step that starts at 100 spends the rest of the step under the quote its own mempool creates. If the quote at step start is already above 200, freeze that quote and its 1.5×. If 1.5× would pass 600, stop and ask. Do not raise the cap.

## Coins

- Spend only mature coins of at least **2 tKAS**.
- Keep a coin only when **all six** public nodes return it.
- Lane host is the first four txid bytes, modulo 6.
- Coins whose bucket modulo 32 is 31 go to the ordered stream, not to a lane signer.
- Stop the senders and let the public mempools drain before a new split. A fresh process pointed at the old file spends outputs that are already in the mempool.
- Two processes never share a coin file.

## What the sender has to do

These are the behaviors that kept a depth-2 pipe moving. A sender without them filled its depth and then sat at zero.

- Subscribe to `virtual-chain-changed`. Count an accept only when the id is one this process still has pending.
- Log the raw virtual-chain event count each second.
- After **15** quiet seconds with no virtual-chain events, and every lane already at max depth, open one hop on each idle lane.
- After **20** quiet seconds with no progress, subscribe to the virtual chain again.
- On a reject, cool that lane for **400 ms**.
- Drop a lane after **8** orphan rejects.
- Drop a lane on an already-spent or already-in-mempool error.
- Start at most **32** submits in one turn.
- The lane cap has to cover the coin file. A cap of 4,000 left muon-10 short. This pre-run used **24,000**.
- A `GO` file arms a spend. A `STOP` file halts it. The 3 Oct halt on the older fleet stays where it is. This sender does not clear it.
- Do not send to `bore.pub` or `159.223.110.159`.

## Nodes

One process family, spread across:

| Index | Node |
|---:|---|
| 0 | vector-10.kaspa.green |
| 1 | proton-10.kaspa.stream |
| 2 | electron-10.kaspa.blue |
| 3 | muon-10.kaspa.blue |
| 4 | quark-10.kaspa.red |
| 5 | neutrino-10.kaspa.stream |

Socket path `/kaspa/testnet-10/wrpc/borsh`.

## Ordered stream

Its own process and its own coins. **4 tx/s**, both fee tiers, depth 1, not a blast. On 6 Oct it ran on proton-10, so it did not share vector-10 with the fastest lane signer.

## How a long process stays up

A sender started inside a short-lived shell dies when that shell's job closes. A detached Node child dies with it. The pre-run stayed up when the parent was created with `Win32_Process.Create` and left running until the deadline.

A watcher may start one dead signer again, on that signer's own coin file. It must not rewrite the coin files while another signer is still spending.

## Do not repeat on 9 Oct

- A 45-second burst as the measurement.
- **Depth 8.** The pipe filled, about four fifths of the seconds were zero, and the combined mean over about 90 minutes was about **540 tx/s**.
- **Fee 2,000** with a cap of 4,000. That attempt stalled. Orphans passed submits and the rate fell to about 0.
- A few seconds at ten processes: about **9,100** submit-OK tx/s and **28,617** orphan rejects. That was not a hold.
- Two processes on one coin file.
- Raising the 600 cap.

## Still open

The n0 txid match, the box dry run, 35 GB free at T0, the plan lock, the end-of-run clock offset, and the final OK on the start time. Earliest start remains Fri 9 Oct 2026, 20:00 CEST, otherwise 13 Oct.
