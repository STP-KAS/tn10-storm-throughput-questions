# Prompt for Grok Build: next TN10 storm (desk sender)

*Paste-in prompt for Grok Build on stp's desk PC. It follows [`plan/NEXT-STORM-PLAN.md`](https://github.com/STP-KAS/tn10-storm-throughput-questions/blob/main/plan/NEXT-STORM-PLAN.md) (§3a, §4, §4a, §5). If this prompt and the plan disagree, the plan wins. Stop and ask stp.*

**Storm date:** early run no earlier than **Fri 9 Oct 2026, 20:00 CEST**. If the 9th isn't ready, **13 Oct** (evening CEST). Exact step times come from stp at T0.

## Why this time is different

In the last storm your part wasn't measured well:
- your logs had only submit-OK counts, with no inclusion on chain;
- there was no timing per transaction;
- nobody knows which script versions ran;
- your runners did not run at 100% of their target (stp's observation).

So we could not say how much of your load actually landed, or how fast. This time, follow the plan exactly, hold your target rate, and log what is listed below. If you can't do something, say so before the run. Don't improvise during it.

## Hard rules

1. **TN10 only.** Use only `kaspatest:` addresses and network `testnet-10`. If a node reports any other network, stop.
2. **Public TN10 nodes only.** Never send to stp's node n0 (or `bore.pub`, `127.0.0.1`, `localhost`).
3. **Keys stay on the desk.** Never print, paste, log, upload or commit a key, seed or wallet file. Don't open the key file. Pass only its path to the script.
4. **No public posting.** Don't post or publish anything (X, GitHub, chats). Logs go to stp only.
5. **One sender.** Never run a second sender from the same wallet.
6. **No real transactions without stp's GO.** One GO for the dry run, a separate GO for the storm.
7. If anything doesn't match this prompt, **stop and ask stp**.

## What to send

- **Timetable:** at T0 stp gives you `steps-utc.json`. It holds each step's start and end in UTC, your target per step and the fee rule. Use those UTC times exactly.
- **Baselines:** **off** in B0 (the first 10 min) and B1 (the last 10 min). Send nothing at all.
- **Your share:** a fixed share of each step's *added* load, **default 25%**. The exact numbers are in `steps-utc.json`, capped at what you held in the dry run. The max step is uncapped for both senders.
- **Hold the target rate for the whole step.** Every step runs **15 min at a fixed target**, then **5 min of drain** at 0 (the max step drains for 10 min). Within a step, nothing changes:
  - same rate;
  - same fees;
  - same number of lanes and workers.
- **Fix the shortfall from last time before the storm:**
  - find why your runners didn't reach 100% (pacing, lanes, workers, connections, CPU or the node; **confirm on the desk**) and fix it;
  - your rate must stay steady at the target, not spike and dip.
  - A step counts as **sender-limited** if your submit-OK rate stays below **95% of target**. Report that, don't hide it.
- **Fees:** at each step start, read your public node's normal fee estimate → **F1** (floor 100 sompi/gram), **F1.5 = 1.5 × F1**.
  - Freeze both for the step.
  - Half your lanes pay F1 and half pay F1.5. A lane keeps its tier for the whole step.
  - Log the F1 you read.
  - If your sender can't split fees, use one fee, log it, and tell stp before the run. Your transactions then stay out of the 1× vs 1.5× comparison.
  - If F1.5 is above your sender's fee cap (600 sompi/gram in the earlier scripts; **confirm on the desk**), stop and tell stp. Don't raise the cap.
- **Small ordered stream (sequencing):** same rules as the box stream in plan §4a, during the steps only.
  - Send independent (not chained) self-transfers in sequence, **2 per second per tier at F1 and F1.5**.
  - Use a pool of pre-split coins. Reuse a coin only after its previous transaction was accepted.
  - This stream counts inside your share.
  - Whether your sender can do non-chained sends from a coin pool: **confirm on the desk**.

## What to log

All times are **UTC, ISO 8601 with milliseconds and `Z`** (e.g. `2026-10-09T18:15:00.123Z`).

**Per transaction**, one JSON line each, in `build-tx-<date>.jsonl`:

| Field | Meaning |
|---|---|
| `seq` | Send sequence number, monotonic per sender process, assigned when the submit starts |
| `txid` | Transaction id |
| `t_submit_start` | UTC time the submit started |
| `t_submit_ok` | UTC time the node answered (empty if rejected) |
| `result` | `ok`, or the reject reason as the node gave it |
| `tier` | `1x` or `1.5x` |
| `feerate` | sompi/gram actually paid |
| `step` | Step name from `steps-utc.json` |
| `stream` | `lane` or `order` |
| `lane` | Lane id (for `lane` transactions) |
| `worker` | Worker / process id |
| `node` | Public node URL used |

**Per second**, one JSON line each, in `build-sec-<date>.jsonl`:
- `t`, `step`, `tier`;
- **`target`** (tx/s you were told to send) and **`achieved`** (submit-OK that second), so any shortfall shows up second by second;
- `submit_ok`, rejects by reason, and the number of active workers and lanes.

**Once per run**, in `build-run-meta-<date>.json`:
- the script file names and their **SHA-256**, plus the version string;
- Node and SDK versions;
- the node URLs used;
- the F1 per step;
- the desk clock's offset from UTC at T0 (`w32tm /stripchart` or equivalent; exact command **confirm on the desk**);
- the wallet address (public address only).

**Where:**
- save everything in the sender's `logs` folder (earlier prompts used `%USERPROFILE%\kaspa-tn10\build-storm\logs\`; **confirm on the desk**);
- one file set per run date;
- after the run, zip only these files and give them to stp, who copies them to the box.
- Nothing else leaves the desk.

We match your txids against the transactions n0 sees accepted on the chain. So you don't need to check inclusion yourself, but every txid must be in the log.

## Dry run first (before the storm, after stp's GO)

1. **Fee split and order:** send a small ordered, fee-split stream from the desk for **5 min**: 2 per second at F1 and 2 per second at F1.5, through public nodes only.
2. **Mini-timetable:** follow a short `steps-utc.json` from stp, with UTC starts and stops (for example 2 min on, 1 min off, 2 min on).
3. **Held rate:** hold one fixed target (stp gives it, e.g. your step-1 share) for **5 min**, so we see what you can really sustain.
4. Hand over the three log files. The box then checks:
   - every field is present, `seq` is monotonic and all times are UTC `Z`;
   - your txids match n0's accepted ids;
   - your starts and stops line up with the UTC timetable (clock offset recorded);
   - both fee tiers are present, with the logged F1;
   - **`achieved` stays at ≥ 95% of `target`** through the held-rate test, with no dips to 0. If not, fix it and repeat the dry run.
5. Your cap for the storm is what you held in step 3.

## Stop rules

- **stp says STOP, or a box STOP is relayed:** stop at once (Ctrl+C, or the script's STOP file). Write out the txids still pending.
- **Step end:** go to 0 for the drain. Don't carry load over.
- **B0 and B1:** off.
- A node reports a network other than `testnet-10` → stop.
- F1.5 above your fee cap → stop and ask.
- Wallet running low → stop and tell stp (amount **confirm on the desk**).
- Any error not covered here → stop and ask stp.
- Never restart or change settings mid-step without telling stp. If it happens, log the time and the reason.
