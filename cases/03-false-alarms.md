# Case 3: When the tool cries wolf

A drain checker that accuses innocent wallets is worse than none. These are real false alarms I found by testing my own
tool (Pulse `trace`) on activity I knew was legitimate.

## A. Online casino play flagged as "stolen key, high confidence" (2026-11-21)
I traced a wallet from a short, known-legitimate session at an on-chain casino (13 minutes of small bets).
**The tool flagged 3 things, all wrong:** the player's wallet and the casino's payout wallet both as "stolen key, HIGH
confidence", plus one "address poisoning" on a legitimate 0.0007 SOL game transfer.

**Why:** casino settlement has exactly the sweeper shape: fast money in and out, tiny amounts, fresh counterparties,
balances that hit zero.

**What tells them apart (rule designed, not built yet):** game transactions carry a memo with the game and amount, and
**money comes back from the same counterparty**. A real drain never pays the victim back.

Side finding: the bets settle on-chain, but **who wins is decided on the casino's own server**. The chain proves
payment, not fairness (no on-chain randomness proof was visible). I only read one session, so that's a lead, not a verdict.

## B. Trading-bot wallets that look like stolen accounts (2026-11-22)
A scan of 6,662 "suspicious" events (token account ownership changes and approvals to ordinary wallets) seemed to show
mass theft: one address had "taken over" 161 accounts.

**Checking by hand:** all 161 were the **same recycled account**. A sample wallet had 3 transactions ever, all in one
block: funded by the "attacker", swapped USDC → SOL → USDC through two market makers, returned everything, and closed.
That's a trading bot's disposable wallet, not theft. Two more big clusters had the same signature.

**Rules I wrote before counting any case as a drain:**
1. The wallet had history before the event, and wasn't created in the same block.
2. The receiver didn't fund it just before.
3. The money taken was the wallet's own.
4. Nothing came back (so not a sale, swap or bridge).

## What this taught me
Every drain pattern has innocent twins. Before calling anything theft, ask "what legitimate activity has this exact
shape?" and test that against real examples. The headline number (6,662 suspicious events) meant almost nothing until each
cluster was checked.
