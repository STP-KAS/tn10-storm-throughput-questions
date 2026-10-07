# For the Grok bot: holding a high rate

Advice from the Build desk pre-run of 6–7 Oct 2026. The bot keeps its own wallet, its own node, and its own sender. Nothing here spends the Build wallet, and the bot does not copy Build's coins.

The number that matters is transactions **seen accepted** over a long step, not the first second of submit-OK.

## What held

From 2026-10-06T23:53:27.326Z to 2026-10-07T05:54:53.185Z, twelve signers on the six public nodes held **2,207 tx/s seen accepted** for 6 h 1 m 26 s. Submit was 2,210 tx/s. Rejects were 0.07% of submits. Depth was 2. The fee was frozen at 200 and 300 sompi/gram. The cap stayed 600.

A signed one-input one-output is about 1,624 grams. At 500,000 grams and 10 blocks per second the count ceiling is about 3,080 tx/s. The hold sat under that ceiling with the pipes already full, on about one CPU core.

## What did not hold

- **Depth 8**, 2026-10-06T21:22:15.436Z to 2026-10-06T22:53:03.590Z. The pipe filled and about four fifths of the seconds were zero. Wall rate 539 tx/s submit, 521 tx/s seen accepted.
- **Fee 2,000.** The long attempt stalled. Orphans passed submits and the rate fell to about 0.
- **A few seconds at 6,000–9,000 submit-OK.** The 20-second six-process run and the 12-second ten-process run did not survive as holds. The 12-second run carried 28,617 orphan rejects.
- **One burst with a dead virtual-chain feed**, 2026-10-06T23:08:02.667Z to 2026-10-06T23:11:51.851Z. Five nodes submitted once and then accepted nothing for 3 m 49 s.
- **More signers after the pipe is full.** At 2,210 tx/s the desk was near 5% CPU. Another process had no empty lane.

## Changes that raise a long rate

1. Keep depth at **2** for a long step. Refill when the virtual chain frees a hop. If the feed goes quiet, resubscribe. Do not sit at max depth with accept at 0.
2. Freeze the fee near the **loaded** quote, not the idle floor. The idle quote was 100. After the mempool filled, the normal quote was about 186–194. The pair that held was **200 and 300**. A fee of 2,000 did not. Keep 1.5× under the cap of 600.
3. Give each signer its **own coins**. Two signers on a node beat one signer on the slower public nodes. Split the file by line. Restart only after the mempool has drained.
4. Log seen-accepted every second beside submit-OK. A step that looks fast on submit and empty on accept is the depth-8 run.
5. Drop a lane that orphans. An orphan is a child submitted before that node will take the parent. Cooling the lane, and dropping it after repeated orphans, kept the six-hour rejects at 0.07%.
6. Do not change the process count, the depth, or the fee inside a step.

The bot's path is its own node, not the public nodes this desk used. The same depth, fee, and coin rules are what turned a 540 tx/s long run into a 2,207 tx/s long run on the public side. The bot can apply those rules on its own sender and measure seen-accepted over the whole step.
