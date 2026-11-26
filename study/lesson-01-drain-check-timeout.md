# Lesson 1: The day Drain Check choked (2026-11-25)

**Grade: B**

Taught by Claude (Claude Code) from a real bug that hit a live site that morning, fixed and deployed the same day
(rug-check commit 23ec425).

## What happened
I shared a Drain Check link on X. Within a minute it was opened about 8 times, by preview bots and two visitors.
Each open ran a brand-new wallet trace, every trace sends many requests to the RPC, and the RPC answered
"429 Too Many Requests". The later visitors waited 60 seconds and got "The check timed out."

The fix: everyone who opens the same wallet shares one trace (a *promise* kept in a box), the answer is reused for
10 minutes, failures are thrown away, and the wait limit went from 60 to 120 seconds. Live test after the fix:
3 visitors at once, 1.8 seconds each.

## What I learned
1. A link is a recipe, not a saved answer: every click runs it again.
2. One trace = many RPC requests; too many at once = 429.
3. A promise is an answer that isn't ready yet; several people can wait on the same one.
4. Trade-offs: reusing answers stops the pile-up but can go stale.
5. Layers: browser → Drain Check → Pulse → Helius (with the public RPC as backup). First question when something
   breaks: *which layer?*

## How I did, question by question

| # | Question | My answer | Score |
|---|---|---|---|
| 1 | Why did later visitors time out? | Expected a shared, already-run trace (right instinct); thought there was separate "X sharing code" (there isn't: the link is a recipe) | Partly right |
| 2 | Why is reusing a trace for 10 min safe? | Trace only reads, never moves funds (right); **spotted on my own** that the drainer may still be active, i.e. the staleness trade-off | Strong |
| 3 | Why put the trace in the box *right away*? | "Because of the 429s": named the effect, not the step-by-step how | Weak |
| — | Explain the fix back in my own words | Correct; small imprecision (others join while it runs, not after it finishes) | Good |
| 4 | Why throw failed traces away? | First half right (others would see the error for 10 min); suggested a backup RPC at the wrong layer (Pulse already has one) | Partly right |

## Strengths
- Instinct for what *should* happen (expected the shared result before seeing any code).
- Finds trade-offs and risks unprompted (the active-drainer point).
- Thinks about real-world failure (backup RPC "in dire situations").

## To improve
- Explain the **how**, step by step, not just the **what** ("first X, then Y, so Z").
- Place each problem in its **layer** before suggesting a fix.
- Use the exact words: 429, timeout, promise, cache.

## Session 2 (2026-11-26): failures and my first test

| # | Question | My answer | Score |
|---|---|---|---|
| 5 | Kept failure: what does the 9:02 visitor get? | "Timed out": right outcome | Right |
| 6 | Is a failure about the wallet or something else? | "Not the blockchain layer, the way the data is accessed" | **Strong**: placed it in the right layer (fixes a weak spot from session 1) |
| 7 | Test: if the failure were kept, what would `runs` be? | Said the test would fail (right), but thought `runs` would keep climbing; really it stays at 1 (I mixed it up with the Lesson 1 pile-up bug) | Partly right |
| 8 | What do you check in a plumbing pressure test? | Glued joints, no leaks, main sewer tested harder than a sink line, sand wrap to spot wet spots | **Strong**: matched setup, checks, risk-based testing, making failures visible |
| 9 | Explain back: what is a code test? | "The degree to which you check the glued pieces, fittings and pressures" | Close: that's *how much* you test (coverage); a test is the check itself |

**Corrected definition:** a test is a small piece of extra code that uses the real code the way a visitor would and
checks the result is what should happen. *How many* things you check is called **coverage**.

**New rule learned:** keep facts, not temporary conditions. A good trace is a fact about the blockchain; a failure is
a temporary problem in the access layer.

**Session 2 grade: B.** Layers clicked. Next: tell the two mirror-image bugs apart (`runs` too high vs too low) and
read a second test on my own.
