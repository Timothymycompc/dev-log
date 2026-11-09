# How we handle secrets and do things securely

Several of these projects touch real money (a hot wallet, payment keys, broker accounts), so security is built in from the
start, not added later.

## Secrets
| Practice | How it works here |
|---|---|
| **Every secret lives in Google Secret Manager** | API keys, bot tokens, database passwords, wallet keys. Each service loads a fixed list of secrets at startup; nothing is baked into code or images |
| **Never in git** | `.env` files are git-ignored; only `.env.example` with blank values is committed. Before anything goes public it is scanned for keys, tokens, account numbers, wallet addresses and emails, and those are removed |
| **Keys go in without being shown** | A `save-secret` helper copies a key from the phone's clipboard straight into Secret Manager and only prints the last 4 characters as proof |
| **Least privilege** | The GitHub token used by the bug-report job can only touch public repos and expires after 90 days. npm packages and MCP-registry listings publish through GitHub's OIDC sign-in, so no long-lived publishing token is stored at all |
| **One project, one set of secrets** | Each bot has its own token (the public Pulse bot is never reused for private bots). V1 Ready runs in its own cloud project with its own Secret Manager |
| **If a key leaks, rotate it** | A key pasted into a chat or a screenshot is treated as exposed: make a new one, delete the old one |

## Money and wallets
| Practice | How it works here |
|---|---|
| **Pulse never holds anyone's keys** | It reads the chain and checks transactions; signing stays with the user or agent |
| **Hard limits on the trading hot wallet** | $25 per trade, $100 per day, 1% max slippage, an allow-list of tokens, a $10 minimum order, and a kill switch (`TRADING_PAUSED`) that stops every action, including cancels and account closes |
| **Check before signing** | Every swap the desk builds must pass Pulse's own checks first: `check_tx` (nothing dangerous in it), `tx_matches` (it does exactly what was asked) and `token_safety` (not a known trap) |
| **Don't trust one price** | A price feed once said a coin was down 96%, but it wasn't. Now a real quote must agree before a stop-loss sells |
| **Owner-only trading** | Trading tools need the owner key; the public only sees the read-only safety tools |
| **Investigate before assuming** | When the wallet showed transactions we didn't expect, we traced them before deciding anything. They turned out to be mine, not a leak |
| **Paper means paper** | The forex trader refuses any non-demo account, only manages trades carrying its own tag (it can never close a trade I opened by hand) and is capped at tiny sizes |

## Data and users
| Practice | How it works here |
|---|---|
| **No IP addresses stored** | Usage logs keep tool inputs/outputs for 30 days, never IP addresses; callers are identified by a salted hash |
| **Owner pages are locked** | Dashboards and owner endpoints need the owner key |
| **The AI reads, never writes, the databases** | A read-only `db-look` tool lets Claude inspect any project database; writes only happen through the app itself |
| **Telegram owner commands check who's asking** | Private bot commands answer only the owner's Telegram ID |
| **Honest about what a check means** | "SAFE" means none of the traps we know about were found, never a guarantee |

## Working safely with AI and the web
- The AI asks before anything public (posts, repos, comments) or hard to undo, and refuses to bypass bot checks, scrape
  sites that forbid it, or write secrets without me.
- No scraping of accounts or platforms that ban bots (Facebook, Fiverr); official APIs only.
- The phone's terminal bridge only listens on the phone itself (localhost) and uses a key restricted to that address.
- Scam investigations look, record and report; they never touch the scammer's or victims' funds.
