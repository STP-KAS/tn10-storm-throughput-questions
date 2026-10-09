# Desk shape for the 9 Oct test

What worked on the Grok Build desk during the 6–7 Oct 2026 TN10 pre-run. Use this on the real test, **Fri 9 Oct 2026, 21:30 UTC, for 8 hours, ending Sat 10 Oct 2026, 05:30 UTC**, or **Mon 13 Oct 2026, 21:30 UTC, for 8 hours, ending Tue 14 Oct 2026, 05:30 UTC** if that is the date. When the storm GO is given, the window is 8 hours from T0. T0 is 21:30 UTC. The paced table is still 2 h 55 min and ends at T0+175, 00:25 UTC the next day.

This file does not start the storm, does not lock the plan, and does not fill the result sections. The lock text is still [`NEXT-STORM-PLAN.md`](NEXT-STORM-PLAN.md). If this note and that plan disagree, the plan wins and Build stops and asks stp. The numbers below are the pre-run. The 10-hour window is already in [tn10-build-desk-tps](https://github.com/STP-KAS/tn10-build-desk-tps): 668 tx/s submit and 273 tx/s seen accepted. It does not move the fee on this page. The paste-in for 9 or 13 Oct is [`GROK-BUILD-PROMPT.md`](GROK-BUILD-PROMPT.md).

TN10 only. The Build wallet only. The Bot wallet is not spent. One sender family. The fee cap stays **600** sompi/gram. Build sends on locus on every step. The bot's runner and the bot's miners use the tunnel to keel. n0 will not run. Never `bore.pub`. Never `159.223.110.159`. The public-node sentences below are the 6–7 Oct shape that was measured. They are not this send path.

## Paced steps, the 25% share

The dry run on 6 Oct is the shape that cleared the gate.

- **4 processes**, fixed for the whole paced schedule. No auto-scale, no fleet relaunch, no mempool pause.
- Each process spends its own coins.
- **4** wRPC connections per process. Each lane stays on one connection.
- **Depth 2.** In-flight cap **48**.
- Fee tiers are half the lanes at F1 and half at 1.5× F1, frozen for the step.
- The ordered stream is its own process.

Held, over 3 minutes: **734 tx/s**, **97.9%** of 750, **0 rejects**, **0** seconds at 0. The steps at 25, 100, 225 and 475 tx/s each hit the target on every second. The n0 txid match is not a gate. n0 will not run.

## Long hold, and the uncapped max step

This is the shape that held the highest rate for minutes, with seen-accepted matching submit.

- **Two signers on each of the six public nodes.** Twelve lane processes.
- Each signer gets its own half of that node's coins, split by **line** into two files. Do not split a host file with `part i/2`. The host is already `txid % 6`, and that lines up with `% 2`, so one of the two parts is empty.
- **Depth 2.** In-flight cap **64** per signer. **4** connections per signer.
- Fee frozen at **200 and 300** sompi/gram. The cap stays 600.
- Ordered stream stays a separate process.

The whole leg, 2026-10-06T23:53:27.326 UTC to 2026-10-07T05:54:53.185 UTC (6 h 1 m 26 s, stopped on request): **2,210 tx/s** submit and **2,207 tx/s** seen accepted, 47,922,856 submits, 47,863,985 seen accepted, 35,639 rejects. The first minute was about **2,530** submit and **2,500** seen accepted. The rate then settled at the six-hour figure. Use the six-hour figure on 9 Oct.

The one-signer leg before it, depth 2 and in-flight 48, frozen at 100 and 150 (vector-10 at 136 and 204), ran about 39 minutes. Its five nodes plus the older muon process overlapped near **2,050–2,120 tx/s** included. Per node, submit tx/s, one signer then two signers: vector-10 574 then 549, proton-10 263 then 320, electron-10 282 then 327, quark-10 274 then 328, neutrino-10 263 then 311, muon-10 465 then 376. The second signer raised the four slower nodes by about 50 tx/s each. The two fast nodes went down. The net over the long window was about **2,207**, not a 400 tx/s gain. The first minute of the two-signer leg was about 2,500, and that minute is not the gain.

The pipes were full again (depth equal to two hops on every live lane). The twelve signers used about **one core**. The desk was still near **5%** CPU. More signers do not raise the rate once the pipe is full. A third signer is not the default. Add one on a node only when that node's lanes are not already two deep.

A signed one-input one-output is about **1,624 grams**. A full 500,000-gram block at 10 blocks per second holds about **3,080** of them.

### Why 200 and 300

At an empty mempool the public quote was **100**. After this desk filled the mempools the normal quote sat near **186–194**, and the priority bucket was far above that. Signers frozen at 100 and 150 were under that quote for the rest of the leg. **200 and 300** is the pair that then held, and 300 is under the 600 cap.

On 9 Oct, use **200 and 300** for the long hold and for the uncapped max step. Sender counts stay the plan's. The paced share stays four processes. Every Build process posts to locus. A third signer is only for a machine whose lanes are not already two deep. n0 will not run. The public-node signer counts above are the 6–7 Oct measurement.

A 10-hour pre-run at **400 and 600**, same depth, same two signers, ran from 2026-10-07T06:38:59 UTC to 2026-10-07T16:38:59 UTC. It spends coins that no mempool transaction for this wallet already spends, so it did not wait for the whole public mempool to reach zero. In the seconds ending 2026-10-07T06:40:14 UTC the lanes were about **2,140 tx/s** submit and the same seen accepted, 0 rejects, and every lane was already about two deep, so the reserved third share was not started. That opening is not the result. From 2026-10-07T07:20:00 UTC to 2026-10-07T07:58:00 UTC the public signers were **2,159 tx/s** submit and **2,158 tx/s** seen accepted. One signer had exited at 2026-10-07T07:32:20 UTC and was not restarted. That slice does not beat the six-hour 2,207. The whole window is now in [tn10-build-desk-tps](https://github.com/STP-KAS/tn10-build-desk-tps): 668 tx/s submit and 273 tx/s seen accepted from 2026-10-07T06:39:01.356Z to 2026-10-07T16:38:59.632Z, and seen accepted is 0 after 08:05Z. 9 Oct stays on 200 and 300. Do not switch the storm to 400.

On the morning of 7 Oct 2026 the six hostnames were three servers. vector-10 was one. muon-10 was one. proton-10, electron-10, quark-10 and neutrino-10 were one server. Recheck before the storm. Do not count six names as six nodes.

A synced desk node joined that pre-run at 2026-10-07T07:57:46 UTC with four signers on coins the public signers were not using. Depth 2, in-flight 64, fee 400 and 600. From 2026-10-07T07:59:00 UTC to 2026-10-07T08:03:33 UTC those four saw **1,538 tx/s** accepted, matching submit, 0 rejects, lanes two deep. In that same minute the public virtual-chain feeds went silent and the public seen-accepted count fell to 0, while those signers still submitted about 430 tx/s. Do not add that 0 to the desk figure. At 2026-10-07T08:07 UTC the desk node recorded about **305 transactions per block** and compute mass about **498,000 of 500,000**. That is this transaction's inclusion ceiling, about **3,050 tx/s**. Public mempools then were about 54,000 to 58,000. On 9 or 13 Oct, Build sends on locus for the paced share, the long hold, and the uncapped max, while locus is synced. keel is the second desk node. The bot uses the tunnel to it. n0 will not run. NEXT-STORM-PLAN's forward section is that rule. The plan is not locked. For a paced step, if the quote at step start is the idle floor of 100, arm at 200 and 300 as well. A step that starts at 100 spends the rest of the step under the quote its own mempool creates. If the quote at step start is already above 200, freeze that quote and its 1.5×. If 1.5× would pass 600, stop and ask. Do not raise the cap.

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

The box dry run, 35 GB free at T0, the plan lock, the end-of-run clock offset, and the final OK on the start time. The old n0 txid match is not a gate. n0 will not run. The start is Fri 9 Oct 2026, 21:30 UTC, for 8 hours, ending Sat 10 Oct 2026, 05:30 UTC, otherwise Mon 13 Oct 2026, 21:30 UTC, ending Tue 14 Oct 2026, 05:30 UTC.
