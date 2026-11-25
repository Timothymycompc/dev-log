# Investigator case studies

Real Solana wallet traces, written up the way a fraud analyst would: what the chain shows, what it can't show,
and what I'd tell the owner. All data comes from my own tool, [Solana Pulse](https://github.com/Timothymycompc/solana-pulse-ai-agent-gateway)
(`trace`), reading mainnet through an RPC; amounts are on-chain, and dollar values are Jupiter prices at the time of the trace.

Victims' wallets are shortened (first 4…last 4) on purpose. Full transaction IDs are available on request to anyone with a
legitimate reason (the owner, an exchange, law enforcement).

| # | Case | What it shows |
|---|---|---|
| 1 | [1,300 SOL: what the chain can and can't prove](01-1300-sol.md) | Separating "the owner signed it" from "someone stole the key"; poisoning bots react within seconds of a big transfer |
| 2 | [The drain my tool missed](02-the-miss.md) | My checker said "just dust" on a wallet that lost 99.98% of its SOL. How I found the miss and fixed the tool |
| 3 | [When the tool cries wolf](03-false-alarms.md) | Casino play and trading-bot wallets that look exactly like drains, and the rules that tell them apart |

What I've learned so far, across all three:
1. **Signed by the owner's key** is the most common finding, and the chain can't tell the owner apart from a thief who has the key. Say so.
2. **Look at timing and order**: lookalike dust that arrives *after* a big send means the send went to the real address, not an imitation.
3. **Every pattern has innocent twins.** A tool that only looks for the drain shape will accuse casinos and bots.
4. **Measure the misses.** A checker that's never been caught wrong has never been tested.
