# Study log

Daily study sessions (started 2026-11-25). Each lesson is a real bug or fix from one of my live projects, taught by
Claude: I answer in my own words, get corrected, and get an honest grade. The point is to track what I'm good at and
what to work on as I learn to read and write code myself. The milestones are in the [study plan](PLAN.md).

**Grades:** A = explains how it works step by step, in the right words, and catches the trade-offs. B = right idea,
some gaps in the how. C = right neighborhood, mostly the what. D = lost, needs the lesson again.

| Date | Lesson | Grade | Strongest | Work on | Went back and fixed |
|---|---|---|---|---|---|
| 2026-11-25 | [1. The day Drain Check choked](lesson-01-drain-check-timeout.md) | B | Found the staleness trade-off on my own | Explaining the step-by-step *how*; knowing which layer a problem is in | Layers: 2026-11-26 session 2 (placed a failure in the access layer, not the blockchain) |
| 2026-11-26 | 1 (session 2). Failures and my first test | B | Layers; plumbing pressure test = code test | Mirror-image bugs (`runs` too high vs too low); exact definition of a test | (not yet) |

Misses stay in, on purpose. The **Went back and fixed** column records when I return to a weak answer, get it right,
and use it in a later lesson. That's where the learning shows.

## Running list
**Good at:** instincts for what should happen; spotting risks and trade-offs; real-world failure thinking.
**Improving:** step-by-step explanations; exact terms; reading tests.
**Fixed:** layers (2026-11-26).
