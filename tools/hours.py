# Estimate hours per project two ways:
#  1) git: commits (deduped by hash) grouped into sessions (gap <= 2h); session = last - first + 30 min lead-in
#  2) Claude Code transcripts: message timestamps grouped by project folder (cwd), gap <= 30 min = active time
import subprocess, os, re, glob, collections, datetime as dt

HOME = "/root"
# SINCE=2026-11-10T06:00:00Z counts only time after that moment (for adding new days to an earlier total:
# Claude Code clears chat history older than ~30 days, so a full rerun undercounts old weeks).
SINCE = os.environ.get("SINCE")
PROJECT_OF_REPO = {
    "pulse-site": "Solana Pulse", "solana-pulse-ai-agent-gateway": "Solana Pulse", "pulse-benchmark": "Solana Pulse",
    "base-pulse": "Base Pulse", "cashout-check": "CashOut Check", "clip-drop": "Clip Drop", "dev-log": "Dev log + portfolio",
    "gh-profile": "Dev log + portfolio", "trading-review": "Dev log + portfolio", "firewood-buyers": "Firewood Buyers",
    "gig-bidder": "Gig Bidder", "money-scan": "Money Scan", "night-desk": "Night Desk (stocks + forex)",
    "rug-check": "Rug Check", "trade-desk": "Trade Desk (memecoins)", "v1-ready": "V1 Ready",
    "contrib/core": "Upstream contributions", "contrib/solana-dev-skill": "Upstream contributions",
}
AUTHOR_FILTER = {"contrib/core", "contrib/solana-dev-skill"}  # forks: only Tim's own commits

def ts(s): return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))

def sessions(times, gap_min, lead_min):
    times = sorted(times); total = 0.0; n = 0
    if not times: return 0.0, 0
    start = prev = times[0]
    for t in times[1:]:
        if (t - prev).total_seconds() > gap_min * 60:
            total += (prev - start).total_seconds() / 3600 + lead_min / 60; n += 1; start = t
        prev = t
    total += (prev - start).total_seconds() / 3600 + lead_min / 60; n += 1
    return total, n

# ---- 1) git
me = subprocess.run(["git", "-C", f"{HOME}/pulse-site", "log", "-1", "--format=%ae"], capture_output=True, text=True).stdout.strip()
seen = set(); git_times = collections.defaultdict(list); first_last = {}
for repo, proj in PROJECT_OF_REPO.items():
    path = f"{HOME}/{repo}"
    if not os.path.exists(path): continue
    args = ["git", "-C", path, "log", "--format=%H %aI %ae"]
    out = subprocess.run(args, capture_output=True, text=True).stdout.split("\n")
    for line in out:
        if not line.strip(): continue
        h, t, email = line.split(" ", 2)
        if repo in AUTHOR_FILTER and email != me: continue
        if h in seen: continue
        if SINCE and ts(t) < ts(SINCE): continue
        seen.add(h); git_times[proj].append(ts(t))

# ---- 2) transcripts
def proj_of_cwd(cwd):
    c = cwd.replace("/data/data/com.termux/files/home", "/root")
    for key, proj in sorted(PROJECT_OF_REPO.items(), key=lambda kv: -len(kv[0])):
        if c == f"{HOME}/{key}" or c.startswith(f"{HOME}/{key}/"): return proj
    if "pulse-video" in c or "listing-prs" in c or "/grant" in c: return "Solana Pulse"
    if "/contrib" in c: return "Upstream contributions"
    if "scam-reports" in c: return "CashOut Check"
    if "texas-inmate" in c: return "Other / personal"
    return "General (mixed: planning, research, outreach, ops)"
pat_t = re.compile(r'"timestamp":"([0-9T:\.\-]+Z)"'); pat_c = re.compile(r'"cwd":"([^"]+)"'); pat_u = re.compile(r'"type":"(user|assistant)"')
chat_times = collections.defaultdict(list); all_chat = []; general_msgs = []
KW = [("Night Desk (stocks + forex)", r"night-desk|night desk|forex|eur_usd|eur/usd|oanda|alpaca|fomc|backtest"),
      ("Trade Desk (memecoins)", r"trade-desk|trade desk|memecoin|lottery lane|ladder a|wait-5|pumpswap"),
      ("Base Pulse", r"base-pulse|base pulse"),
      ("Upstream contributions", r"issue-poster|bug report|maxsupportedtransactionversion|v1 bug|pulse-open-issues"),
      ("V1 Ready", r"v1-ready|v1 ready|v1ready"),
      ("CashOut Check", r"cashout|casino|gamevault|luckquexa|boomwins"),
      ("Firewood Buyers", r"firewood|woodfiner"),
      ("Freelance (Fiverr/Freelancer, Gig Bidder)", r"fiverr|freelancer|gig-bidder|gig bidder"),
      ("Money Scan", r"money-scan|money scan|superteam earn|money-makers"),
      ("Rug Check", r"rug-check|rug check"),
      ("Dev log + portfolio", r"dev-log|trading-review|gh-profile|portfolio"),
      ("Clip Drop", r"clip-drop|clip drop|reels"),
      ("Phone setup + AI tooling", r"termux|proot|voice mode|keyhub|ghost-desk|ghost desk|agy-go|antigravity|listen|button bar"),
      ("Solana Pulse", r"pulse-site|solana pulse|token_safety|check_tx|tx_matches|x402|mcp registry|grant|tensorblock|glama|pulse-stats|pulse bot|solanapulsecheckbot")]
KWC = [(n, re.compile(r, re.I)) for n, r in KW]
for f in glob.glob(f"{HOME}/.claude/projects/*/*.jsonl") + glob.glob(f"{HOME}/.claude/projects/*/*/*.jsonl"):
    if "/subagents/" in f: continue
    cwd = None
    with open(f, errors="replace") as fh:
        for line in fh:
            m = pat_c.search(line)
            if m: cwd = m.group(1)
            if not pat_u.search(line): continue
            t = pat_t.search(line)
            if not t or not cwd: continue
            tt = ts(t.group(1))
            if SINCE and tt < ts(SINCE): continue
            pr = proj_of_cwd(cwd); all_chat.append(tt)
            if pr.startswith("General"):
                hits = [n for n, rx in KWC if rx.search(line)]
                general_msgs.append((tt, hits))
            else: chat_times[pr].append(tt)
# re-sort General: blocks of messages <=30 min apart go to the project mentioned most in that block
general_msgs.sort()
block = []
def flush(block):
    if not block: return
    c = collections.Counter(h for _, hs in block for h in hs)
    who = c.most_common(1)[0][0] if c else "General (unclear)"
    chat_times[who].extend(t for t, _ in block)
for t, hs in general_msgs:
    if block and (t - block[-1][0]).total_seconds() > 1800: flush(block); block = []
    block.append((t, hs))
flush(block)

print(f"{'Project':48} {'git hrs':>8} {'sess':>5} {'commits':>7} {'chat hrs':>9}  span")
rows = set(git_times) | set(chat_times)
tot_g = tot_c = 0
for p in sorted(rows, key=lambda p: -(sessions(chat_times[p], 30, 0)[0] + sessions(git_times[p], 120, 30)[0])):
    g, gs = sessions(git_times[p], 120, 30); c, _ = sessions(chat_times[p], 30, 0)
    tot_g += g; tot_c += c
    allt = sorted(git_times[p] + chat_times[p])
    span = f"{allt[0]:%b %d} – {allt[-1]:%b %d}" if allt else ""
    print(f"{p:48} {g:8.0f} {gs:5d} {len(git_times[p]):7d} {c:9.0f}  {span}")
print(f"{'TOTAL':48} {tot_g:8.0f} {'':5} {len(seen):7d} {tot_c:9.0f}")
allc, n = sessions(all_chat, 30, 0)
days = len({t.date() for t in all_chat})
pre = [t for t in git_times["Solana Pulse"] if t < ts("2026-10-10T00:00:00Z")]
print(f"Solana Pulse git hours BEFORE chat history starts (Aug 30 - Oct 9): {sessions(pre,120,30)[0]:.0f} h in {sessions(pre,120,30)[1]} sessions, {len(pre)} commits")
print(f"Overall chat active time (no double counting across folders): {allc:.0f} h over {days} days with activity; first {min(all_chat):%Y-%m-%d}")
