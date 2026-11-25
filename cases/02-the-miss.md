# Case 2: The drain my tool missed

**Wallet:** p61X…aLoq (shortened on purpose), reported as drained. **First traced:** 2026-11-11.

## The miss
My checker (Pulse `trace`, behind Drain Check) looked at this wallet and reported **only dust signs**: tiny transfers from
lookalike addresses. It did not mention that the wallet had just lost almost everything.

## What the chain actually shows
| Time (Dallas) | What happened |
|---|---|
| Nov 5, early am | Eight tiny token transfers (fractions of a meme token) from one sender: spam/dust. |
| Nov 5-6 | Normal-looking deposits from several wallets bring the balance to ~83.9 SOL. |
| **Nov 6, 11:58 am** | **83.90 SOL (99.98% of its SOL, ~$5,700)** leaves in one transaction to HRts…mnXe, a **program-controlled deposit address**. Signed by this wallet, fee paid by this wallet. |
| 12:00 pm | A lookalike of HRts… (same first and last 4 characters) sends 0.00001 SOL: poisoning, again *after* the send. |
| 12:04 pm | The last tokens are sent away. |

## Why the tool missed it
The drain rule looked for the **sweeper pattern**: money pulled out by someone else, fast, to fresh wallets. This was one
big send, signed by the wallet itself, to a program address. It didn't match, so the report led with the only flags
that did match: the dust. Technically true, and useless to a scared owner.

## The fix (2026-11-11, Pulse commit b7ea54ca)
- **Biggest move first:** if 50% or more of the wallet's SOL left in one transaction, the report now opens with it
  (amount, share, dollar value, who signed it, link).
- Destinations ranked by **dollar value** (Jupiter prices) instead of transaction count.
- The drain rule itself was **not** loosened. A big send isn't proof of theft; it's the first thing the owner needs to see.

Re-traced 2026-11-25: the report now opens with "The biggest move: 83.900005006 SOL (about $5,677.21), 99.98% of the
wallet's SOL…" and says the destination is a program-controlled address, so the owner should check their account at any
exchange or app they used around then.

## What this taught me
A report can be accurate and still miss the point. Now I ask "what would the owner need to see first?" and test the
tool against real reported cases, not only the patterns I already know.
