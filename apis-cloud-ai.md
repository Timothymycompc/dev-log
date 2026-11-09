# What I learned: APIs, cloud hosting, and working with AI

None of this was known to me in August. It was all learned by building real services, mostly from a phone.

## APIs
**Used for real:** Solana RPC (Helius), Jupiter (prices, quotes, swaps, limit orders), RugCheck, GeckoTerminal and
DexScreener (pools and candles), Coinbase's Base node, x402 payment facilitators (Coinbase first, PayAI as backup), Telegram
Bot API, GitHub API, Oanda v20 (forex candles + demo orders), Alpaca (stock data + paper orders), FRED and federalreserve.gov,
Freelancer.com, Google Text-to-Speech, Overture/OpenStreetMap/NWS/FCC (free public data), and the Claude API.

| Lesson | Where it hit |
|---|---|
| **Free tiers rate-limit hard.** Jupiter's keyless API answered "429 too many requests" after ~5 quick calls; GeckoTerminal needed 1 call a second | Got proper API keys, spaced calls, retried with limits, cached |
| **An error message can lie.** A "no route for this swap" (HTTP 400) was being reported as "Jupiter is down" (503), so a rugged coin was never recognised | Read status codes properly; tests for each error path |
| **Silence isn't an answer.** One source having no price doesn't mean a coin is dead; a failed call isn't "zero" | Say "unknown", never guess; use a second source only when it's comparable |
| **APIs have quirks.** Alpaca's free feed returns nothing without a start date; Oanda's daily candles start at 5 PM New York; the Fed's site lists meetings in four different formats | Read the docs, then test against real responses and keep them as fixtures |
| **The chain changes under you.** Solana started carrying *version 1* transactions that common libraries couldn't decode | Measured it, fixed Pulse, reported it to 31 projects |
| **Respect the site.** Some data sites block automated downloads | Never worked around a bot check; found an official API instead |
| **Keys are money** ([more on security](security.md)). Every key lives in Google Secret Manager, loaded at startup; tokens expire and need renewing (the bug-report job's GitHub token runs 90 days) | A `save-secret` helper copies a key from the phone clipboard straight into Secret Manager without it ever being printed |
| **Data has terms.** Price data from brokers comes with rules about re-sharing | Learned to check before publishing |

## Cloud hosting (Google Cloud)
**What runs there:** Solana Pulse, Base Pulse, Trade Desk, Rug Check and the Telegram bots as **Cloud Run services**; the
stock desk, the forex paper trader, Money Scan and Gig Bidder as **Cloud Run jobs** fired by **Cloud Scheduler**; one shared
**Cloud SQL Postgres** instance with a database per project; **Secret Manager** for every key; **Cloud Storage** for results
and backups; **Cloud Build** for tests, video renders and big backtests; a separate cloud project for V1 Ready.

| Lesson | How |
|---|---|
| **Every deploy is a new revision; rollback is one command.** | Each deploy note records the "undo" (send traffic back to the previous revision) |
| **Don't ship your data folder.** A 79 MB research folder got uploaded with the code and broke deploys from the phone | `.gcloudignore` files; only what the server needs gets uploaded |
| **The phone can't do heavy work.** Headless browsers crash, and a full test run once reset every terminal session | Heavy jobs run in Cloud Build: a 23,379-coin backtest split into 8 parallel shards (~10 hours), video renders, 41 MB data releases |
| **Scheduled jobs beat remembering.** | Bug reports post themselves (max 6 a day), the forex paper trader runs hourly, scans run every 6 hours |
| **Things fail quietly.** Bots hit rate limits and nearly stopped without saying so | Health checks, uptime alerts, emails at most once an hour |
| **Usage logs need honesty.** Most "visitors" were bots faking browsers | Owner dashboard with a fake-browser flag; inputs and outputs kept 30 days, no IP addresses |
| **Payments for machines.** x402: an AI agent pays per call in USDC; the directory checkers must get a "402 Payment Required", never a free call | Two facilitators so either can settle; 25 free calls per tool per day |

## Working with AI
**Tools:** Claude Code as the main pair-programmer (in a phone terminal, with voice mode), Google's Antigravity/Gemini as a
second opinion and red-team reviewer, the Claude API inside the Gig Bidder, and experiments running local models on the phone
(llama.cpp / Ollama).

| Lesson | Example |
|---|---|
| **AI builds fast; checking is my job.** | Every claim needs a number from real data. The rule "never call a caller a person without checking" came from a dashboard that looked like people and wasn't |
| **A second AI catches the first one's blind spots.** | Gemini's review found that a memecoin replay was too optimistic (+14.2% became +0.9%) |
| **AI is great at finding "edges" that are really luck.** | ~1,500 forex versions → one "winner" that failed on unseen data. Now tests are committed to git *before* they run |
| **Small steps, one at a time.** | On a phone, one or two steps per message works; long pastes break |
| **Hand off to save cost.** | Long jobs go to a second AI through files (task in, short result out) so the main session stays small; both have usage quotas, and one ran out mid-research |
| **Guardrails matter.** | The AI declined to scrape Facebook, bypass bot checks or write keys without me, and asked before anything public. Annoying sometimes, right every time |
| **Building *for* AI agents is its own skill.** | Pulse's tools are described for AI readers: plain inputs and outputs, usage examples, a token budget (tool list cut from ~4,640 to ~3,662 tokens), read-only hints, and a public benchmark so an agent can trust the answers |
| **Some funders won't take AI-written work.** | One grant program banned AI-written proposals and code, so it was ruled out. Others ask how it was built — be upfront |
