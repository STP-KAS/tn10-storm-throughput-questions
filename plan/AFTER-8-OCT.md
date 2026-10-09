> **Experimental. We are just trying this.**
>
> [Disclaimer](../DISCLAIMER.md)

Thank you, Kaspa Pulse (@gokugalax), for the guidance and the input over this stretch, from 4 Oct 2026 on. The 7 Oct 2026 wording stays: sign-and-send processes are senders; runner is the setup; bot is reserved for the operator.

# After the 8 Oct 2026 checkout

Written after the 20:11:33Z halt on Thursday 8 Oct 2026. This file is the checkout. It is not the storm. It does not fill [Build result](../README.md#build-result) or [bot result](../README.md#bot-result). Those stay empty until the real test.

The real test stays Friday 9 Oct 2026, 21:30 UTC, for 8 hours, ending Saturday 10 Oct 2026, 05:30 UTC. If that day is not ready, Monday 13 Oct 2026, 21:30 UTC. This file does not give the storm GO, does not lock [`NEXT-STORM-PLAN.md`](NEXT-STORM-PLAN.md), and does not start a sender.

If this file and the plan disagree, the plan wins. The disagreements are listed in the checkout result. They do not change the plan.

The row sheet is [tonight-8-oct/RESULTS.md](https://github.com/STP-KAS/grok-bot-build-combo/blob/593a4baf4d9fcf5299634474d97960a517b2cf24/tonight-8-oct/RESULTS.md) on the private combo repo, commit `593a4baf4d9fcf5299634474d97960a517b2cf24`. This page is the count. It does not copy tx ids.

## 1. The 8 Oct updates

Read from that same combo commit, not from memory.

- Tonight's checkout clock stays 18:00–20:00 UTC. 20:00 UTC is the stop. His counter for tonight is that same window. His Friday counter is 21:25 UTC through Saturday 10 Oct 2026 05:35 UTC. Friday T0 stays 21:30 UTC. The DM times 20:00 UTC tonight and 21:00 UTC Friday are not these clocks.
- The per-minute line he asked for is on top of the per-second log. Per minute: tx sent, the node by name, and five tx ids in the local log only. Git gets the count, not the ids.
- The hours after 00:25 UTC stay unnamed. He asked to name them or to end the storm at 00:25. stp chooses in the storm GO. This checkout does not choose.

## 2. The checkout result

### Sample line

The written sample, 18:30:00Z–18:45:00Z at 62 tx/s, was **skipped**. Rehearsal GO was not said. n0 was still syncing, and the real test was postponed for that reason. That sample has no first submit and no last submit. It saved no tx ids.

The bot's blocks were not printed. Every bot cell on the 10-minute sheet stays **not measured**. n0 synced, n0 lag, n0 mempool, and the box disk were not read. At 20:11:33Z the desk senders were halted so n0 can catch up. This file does not move Friday 21:30 UTC. If n0 is still behind at that T0, the written fallback stays Monday 13 Oct 2026, 21:30 UTC. stp decides.

### What the desk did run

These rounds are desk tests on the Build wallet. They are not rehearsal GO and not storm GO. Local `accept_seen` is the desk node's counter. It is not Kaspa Pulse's chain count. Finished runs that wrote a summary line use that line. A run stopped before the summary uses the per-second sum, which can undercount accepts.

| Round | Start UTC | End UTC | Senders | Node | Target tx/s | Submit | Local accept | Rejects |
|---|---|---|---:|---|---:|---:|---:|---|
| 1 pre8 | 15:49:32 | 16:04:33 | 4 | locus, vector-10.kaspa.green, proton-10.kaspa.stream | 62 | 55,490 summary | 55,488 summary | 0 |
| 2 s7 | 17:22:11 | 17:52:15 | 7 | vector-10.kaspa.green, proton-10.kaspa.stream, electron-10.kaspa.blue, muon-10.kaspa.blue | 109 | 195,076 summary | 195,073 summary | 0 |
| 3 k3 | 18:01:20 | 18:22:36 | 6 | locus | 3,024 | mean 2,191.2 | mean 2,142.9 | 0 |
| 4 h10 | 18:24:48 | 18:37:37 | 10 | locus | 5,040 | mean 1,854.8 | mean 1,750.7 | 0 |
| 5 q10 | 18:48:19 | 19:00:06 | 10 | locus | 5,040 | node process gone at 19:00:06Z | | 0 until the process was gone |
| 6 u10 | 19:02:53 | 19:03:41 | 10 | locus | 5,040 | node faulted again | | |
| 7 v10 | 19:13:37 | 19:41:20 | 10 | locus | 5,040 | see the 10-minute rows | | 0 on the rows that were read |
| 8 w11 | 19:42:01 | 19:42:12 | 11 | locus | 5,544 | stopped | | about 3,400 per second, orphans |
| 9 x10 | 19:42:37 | 19:57:41 | 10 | locus | 5,040 | stopped while a change to nine was being set up | | 0 on the opening seconds |
| 10 a10 | 20:04:50 | 20:11:33 | 10 | locus | 5,040 | mean 2,100.1 | mean 1,954.1 | 0 |

Round 3 is 1,215 aligned seconds. Round 4 is 714. Round 10 is 378 aligned seconds, 20:04:52Z through 20:11:33Z, and 0 zero seconds. Nine senders were not armed. Twelve and fourteen were stopped within seconds on the same pattern as eleven: free RAM at or under about 1.1 GB, and orphan rejects.

Locus is the desk kaspad, testnet-10, UTXO index on, loopback Borsh, started without `--ram-scale`. It exited twice with no shutdown line, at 19:00:06Z and at 19:03:41Z, both an access violation `0xc0000005` at offset `0x1931c7a` in `kaspad.exe`. It was restarted with the same flags. The 18 desk miners were restored with it and were not switched. The older fleet halt file still says `halt`.

### Why six and ten submitted almost the same rate

The plan's mass cap is about 3,024 included tx/s. Six senders already target 3,024. Ten target 5,040, which is above that cap.

Each sender holds at most four unconfirmed hops on each coin. A full sender has about 1,008 coins, so the cap is 4,032 hops in flight. A new hop is submitted when an older one is accepted. Once that cap is full, submit equals whatever locus accepts.

Round 3 was already on that cap and held about 2,191 submit tx/s and 2,143 local accept tx/s. Ten senders open near 5,000 tx/s for a few seconds, then each sender sits on its own cap and the sustained rate falls to about 1,700–2,200 tx/s. Round 10's mean was 2,100.1 submit and 1,954.1 local accept. The extra senders add waiting hops. They do not add a second drain. Under ten, the desk mempool stayed near 33,000–35,000 and the live quote rose to about 183, while the senders stayed frozen at the arm quote of 100 and 150.

On the plan's submit-versus-target rule, both shapes are sender-limited: submit stayed under 95% of target. Local accept stayed close to submit on the clean windows, so those windows are not a measured saturation. Saturation in the plan is scored on n0. n0 was not read. The two process deaths are a dead locus process. Free RAM under 1 GB was the eleven, twelve, and fourteen attempts, and those were stopped. Mining share was **not measured**.

### Monitor rows

Bot columns, n0 lag, bot NTP, bot disk, and usage stay **not measured** on every row. Accepted in this table is local `accept_seen` on the Build side. The 18:00 and 18:10 rows were not read.

| UTC | Build | Senders | Desk disk GB | Desk NTP mean | Submit tx/s | Local accept tx/s | Indexer | Note |
|---|---|---:|---:|---:|---:|---:|---|---|
| 18:20 | up | 6 | 646.7 | −0.1087 s | 2161 | 2472 | synced, lag 1 s | round 3 |
| 18:30 | up | 10 | 646.3 | −0.1097 s | 1628 | 1570 | synced, lag 2 s | written sample not started |
| 18:40 | up | 10 | 632.6 | −0.1102 s | 3013 | 1697 | synced, lag 2 s | late read, opening seconds |
| 18:50 | up | 10 | 631.9 | −0.1109 s | 2245 | 2137 | synced, lag 3 s | depth at cap, 0 rejects |
| 19:00 | node down | 10 | 646.1 | −0.1102 s | 1653 | 1602 | synced, lag 3 s | process gone at 19:00:06Z |
| 19:10 | up | 10 | 645.9 | −0.1137 s | 4657 | 1990 | synced, lag 3 s | late read, hour opening |
| 19:20 | up | 10 | 645.8 | −0.1111 s | 2067 | 2004 | synced, lag 4 s | depth at cap, 0 rejects |
| 19:30 | up | 10 | 647.9 | −0.1109 s | 1706 | 1665 | synced, lag 1 s | depth at cap, 0 rejects |
| 19:40 | up | 10 | 649.7 | −0.1113 s | 2225 | 2165 | synced, lag 83 s | one sample, under the 120 s freeze line |
| 19:50 | up | 10 | 650.2 | −0.1118 s | 1780 | 1724 | synced, lag 34 s | round 9, depth at cap, 0 rejects |
| 20:00 | up | 0 | not measured | not measured | 0 | 0 | not read at 20:00 | senders off from 19:57:41Z until 20:04:50Z |

The late read at 20:07:37Z, after round 10 was armed: 10 senders, disk 650.8 GB, free RAM 4.7 GB, NTP mean −0.1117 s, submit mean 2,142.5 tx/s, local accept mean 2,096.0 tx/s, 0 rejects, indexer synced, lag 17 s. Desk mempool 34,905, quote 183. The six public mempools were about 12,500–13,800, fees 179–180. Halted at 20:11:33Z. At that sample the desk mempool was 18,165 and the quote was 179. The desk node and the 18 miners were left up.

The 18:00 NTP pair was not read, so the 50 ms movement flag was not scored. Later desk offsets stayed near −0.111 s. No indexer sample met the freeze rule. Evening locus rounds turned per-transaction logging off, so those minutes have no five-id set. The skipped 18:30 sample saved none either. Earlier minute files for pre8 and s7 stayed on the desk.

### Where this disagrees with the plan

The plan wins. None of these change N, the fee pair, or the share.

- The checkout used depth 4 and, at the high rate, up to 10 locus senders, with the fee frozen at 100 and 150. The storm shape stays 4 paced processes, depth 2, fee 200 and 300.
- Eleven or more senders on this desk exhausted RAM and were orphaned. That does not raise the storm's N.
- The combined score needs both accepted rates. The bot side is **not measured**. Locus accept is not the combined rate.

## 3. Kaspa Pulse's input

The 8 Oct note already in the combo repo at the commit above is the input used here. He said the checkout PDF is solid. The 9th works on his side. He counts tonight 18:00–20:00 UTC and Friday 21:25 UTC through Saturday 05:35 UTC. The per-minute fields are the three listed in section 1. The hours after 00:25 UTC stay his open question.

**No new input.** Nothing new arrived during or after this checkout. He was not pinged. This page does not send him the sheet.

## The candidate prompt

From this note and from the plan, the candidate paste is [`GROK-BUILD-PROMPT-AFTER-8-OCT.md`](GROK-BUILD-PROMPT-AFTER-8-OCT.md). It does not replace [`GROK-BUILD-PROMPT.md`](GROK-BUILD-PROMPT.md) until stp says so.

Intentions are good; thought process is questionable. STP remains delusional. Si vis pacem, para bellum.
