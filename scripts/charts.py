#!/usr/bin/env python3
"""Draw charts/*.png from the CSVs in data/ (matplotlib). Times are UTC."""
import csv, os, datetime as dt, collections, statistics as st
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.dates as md
H = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
D = lambda f: list(csv.DictReader(open(f"{H}/data/{f}")))
T = lambda s: dt.datetime.strptime(s, "%Y-%m-%d %H:%M" if len(s) == 16 else "%Y-%m-%d %H:%M:%S")
F = lambda v: float(v) if v not in ("", None) else float("nan")
LEGS = [("L1", "2026-10-01 18:35", "2026-10-02 05:53"), ("L2", "2026-10-02 07:07", "2026-10-02 08:15"),
        ("L3", "2026-10-02 09:49", "2026-10-02 14:51"), ("L4", "2026-10-02 19:52", "2026-10-02 23:06")]
def legs(ax, ymax=None):
    for n, a, b in LEGS:
        ax.axvspan(T(a), T(b), color="#f2f2f2", zorder=0)
        ax.text(T(a), 1.0, " " + n, transform=ax.get_xaxis_transform(), va="top", fontsize=8, color="#555")
def tfmt(ax):
    ax.xaxis.set_major_formatter(md.DateFormatter("%a %H:%M", tz=dt.timezone.utc))
    ax.xaxis.set_major_locator(md.HourLocator(byhour=range(0, 24, 3), tz=dt.timezone.utc))
    plt.setp(ax.get_xticklabels(), rotation=0, fontsize=8)
os.makedirs(f"{H}/charts", exist_ok=True)
SRC = "Source: TN10 ops (stp's TN10 setup), TN10 storm 1-3 Oct 2026. "

# 1. submitted vs accepted over the whole storm
R = D("oct_box_submitted_vs_accepted_1min.csv"); t = [T(r["minute_utc"]) for r in R]
fig, ax = plt.subplots(figsize=(14, 5.5)); legs(ax)
ax.plot(t, [F(r["box_target_rate_tx_s"]) for r in R], color="#bbbbbb", lw=0.8, label="runner rate cap (sum of what runners were allowed to send)")
ax.plot(t, [F(r["n0_processed_tx_s_all_senders"]) for r in R], color="#9467bd", lw=0.7, alpha=0.7, label="n0 Processed tx/s, all senders (block-body count, overstates unique tx)")
ax.plot(t, [F(r["box_submitted_tx_s"]) for r in R], color="#1f77b4", lw=1.1, label="box submitted tx/s (submit OK)")
ax.plot(t, [F(r["box_accepted_tx_s"]) for r in R], color="#d62728", lw=0.9, alpha=0.85, label="box accepted tx/s (seen on n0 virtual chain)")
ax.set_ylim(0, 12000); ax.set_ylabel("tx/s, 1-minute average"); tfmt(ax)
ax.set_title("TN10 storm, 1-3 Oct 2026: what the box runners submitted vs what was accepted, per minute (UTC)")
ax.legend(loc="upper right", fontsize=8); ax.grid(alpha=0.3)
fig.text(0.01, 0.01, SRC + "data/oct_box_submitted_vs_accepted_1min.csv (from runner1-4.out, p2w1-8.out, host.jsonl)", fontsize=7, color="#555")
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(f"{H}/charts/1-submitted-vs-accepted-over-time.png", dpi=110); plt.close(fig)

# 1b. where acceptance flattens: accepted vs rate cap, one dot per minute
fig, ax = plt.subplots(figsize=(8, 6))
xs = [F(r["box_target_rate_tx_s"]) for r in R if F(r["box_target_rate_tx_s"]) >= 100 and r["runner_reps_paused"] == "0"]
ys = [F(r["box_accepted_tx_s"]) for r in R if F(r["box_target_rate_tx_s"]) >= 100 and r["runner_reps_paused"] == "0"]
ss = [F(r["box_submitted_tx_s"]) for r in R if F(r["box_target_rate_tx_s"]) >= 100 and r["runner_reps_paused"] == "0"]
ax.scatter(xs, ss, s=8, color="#1f77b4", alpha=0.35, label="submitted")
ax.scatter(xs, ys, s=8, color="#d62728", alpha=0.35, label="accepted")
B = collections.defaultdict(list)
for x, y in zip(xs, ys): B[int(x // 1000) * 1000 + 500].append(y)
bx = sorted(k for k in B if len(B[k]) >= 5); ax.plot(bx, [st.median(B[k]) for k in bx], "k-o", ms=4, label="median accepted per 1,000 tx/s bin")
m = max(xs); ax.plot([0, m], [0, m], ls="--", color="#999", lw=0.8, label="accepted = cap")
ax.set_xlabel("runner rate cap, tx/s (sum over runners, minute mean)"); ax.set_ylabel("tx/s, 1-minute average"); ax.set_ylim(0, 5000)
ax.set_title("Where box acceptance flattens (1-3 Oct, minutes with no runner paused)", fontsize=10); ax.legend(fontsize=8); ax.grid(alpha=0.3)
fig.text(0.01, 0.01, SRC + "data/oct_box_submitted_vs_accepted_1min.csv", fontsize=7, color="#555")
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(f"{H}/charts/1b-acceptance-flattening.png", dpi=110); plt.close(fig)

# 4. mempool depth over time
fig, ax = plt.subplots(figsize=(14, 5)); legs(ax)
ax.fill_between(t, [F(r["n0_mempool_min"]) for r in R], [F(r["n0_mempool_max"]) for r in R], color="#ff7f0e", alpha=0.25, lw=0, label="min-max in the minute")
ax.plot(t, [F(r["n0_mempool_median"]) for r in R], color="#d35400", lw=0.9, label="median (15-s samples)")
ax.axhline(100000, color="k", ls=":", lw=0.8); ax.text(t[5], 101500, "n0 mempool cap ~100k (--ram-scale=0.1)", fontsize=7)
ax.axhline(80000, color="#c0392b", ls="--", lw=0.7); ax.text(t[5], 81500, "storm-watch pause > 80k", fontsize=7, color="#c0392b")
pz = [T(r["minute_utc"]) for r in R if r["storm_watch_pause_flags"] not in ("", "0")]
ax.plot(pz, [104000] * len(pz), "|", color="#c0392b", ms=6, label="minute with a storm-watch pause flag")
ax2 = ax.twinx(); ax2.plot(t, [F(r["box_accepted_tx_s"]) for r in R], color="#2c3e50", lw=0.5, alpha=0.5); ax2.set_ylim(0, 9000)
ax2.set_ylabel("box accepted tx/s (thin grey line)", fontsize=8)
ax.set_ylim(0, 110000); ax.set_ylabel("n0 mempool, transactions"); tfmt(ax); ax.grid(alpha=0.3); ax.legend(loc="upper right", fontsize=8)
ax.set_title("TN10 storm, 1-3 Oct 2026: n0 mempool depth per minute (UTC)")
fig.text(0.01, 0.01, SRC + "data/oct_box_submitted_vs_accepted_1min.csv (mempool from host.jsonl, pauses from storm-watch.jsonl)", fontsize=7, color="#555")
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(f"{H}/charts/4-mempool-depth-over-time.png", dpi=110); plt.close(fig)

# 3. indexer freeze windows + tps at the time
A = D("oct_api_tn10_health_2min.csv"); W = D("oct_api_tn10_stall_windows.csv")
fig, (a1, a2) = plt.subplots(2, 1, figsize=(14, 7), sharex=True, gridspec_kw={"height_ratios": [1.2, 1]})
day = {"Thu": "2026-10-01", "Fri": "2026-10-02", "Sat": "2026-10-03"}
def wt(s): d, hm = s.split(); return T(f"{day[d]} {hm}")
for a in (a1, a2):
    legs(a)
    for w in W:
        if w["window"].startswith("L") and "health" in w["window"] and "subset" not in w["note"]:
            a.axvspan(wt(w["start_utc"]), wt(w["end_utc"]), color="#e74c3c", alpha=0.18 if "freeze" not in w["window"] else 0.35, lw=0)
ta = [T(r["time_utc"]) for r in A]
lag = [F(r["indexer_lag_s_acceptedTxBlockTimeDiff"]) for r in A]
a1.semilogy(ta, [max(x, 1) for x in lag], ".", ms=3, color="#2c3e50", label="api-tn10 /info/health acceptedTxBlockTimeDiff (indexer lag, s)")
bad = [(x, r) for x, r in zip(ta, A) if r["http"] not in ("200",)]
a1.plot([x for x, r in bad if r["http"] in ("503", "502")], [3000] * len([1 for x, r in bad if r["http"] in ("503", "502")]), "v", color="#c0392b", ms=4, label="HTTP 503/502")
a1.plot([x for x, r in bad if r["http"] == ""], [6000] * len([1 for x, r in bad if r["http"] == ""]), "x", color="#7f8c8d", ms=4, label="timeout / no answer")
a1.axhline(120, ls="--", color="#999", lw=0.7); a1.set_ylabel("indexer lag, s (log)"); a1.legend(loc="upper left", fontsize=8); a1.grid(alpha=0.3)
a1.set_title("api-tn10 indexer health vs load, 1-3 Oct 2026 (UTC). Red bands = stall windows; dark red = full freeze (L4, 86 min)")
a2.plot(t, [F(r["n0_processed_tx_s_all_senders"]) for r in R], color="#9467bd", lw=0.7, label="n0 processed tx/s, all senders")
a2.plot(t, [F(r["box_accepted_tx_s"]) for r in R], color="#d62728", lw=0.8, label="box accepted tx/s")
a2.set_ylim(0, 10000); a2.set_ylabel("tx/s, 1-min avg"); a2.legend(loc="upper left", fontsize=8); a2.grid(alpha=0.3); tfmt(a2)
fig.text(0.01, 0.01, SRC + "data/oct_api_tn10_health_2min.csv (api-health-min.jsonl), data/oct_api_tn10_stall_windows.csv, data/oct_box_submitted_vs_accepted_1min.csv", fontsize=7, color="#555")
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(f"{H}/charts/3-indexer-freeze-windows-vs-tps.png", dpi=110); plt.close(fig)

# 2. Sept fee-tier confirmation-time distribution, two load steps
P = D("sep_fee_tier_probes.csv"); tiers = ["1", "1.2", "2", "5", "10", "100"]
fig, axs = plt.subplots(1, 2, figsize=(13, 5.5), sharey=True)
for ax, ph, title in ((axs[0], "P1-overload", "Step A: 19:48-20:46 UTC, storm paid 120 sompi/g (1.2x)\nn0 'Processed' ~6,460 tx/s avg, mempool median ~63k"),
                      (axs[1], "P4-max", "Step B: 20:47-21:50 UTC, storm paid 200 sompi/g (2x)\nn0 'Processed' ~7,420 tx/s avg, mempool median ~53k")):
    data = [[F(p["inclusion_s"]) for p in P if p["phase"] == ph and p["tier_x_min_feerate"] == m and p["inclusion_s"]] for m in tiers]
    ax.boxplot(data, whis=(0, 100), widths=0.55, medianprops=dict(color="#d62728", lw=2))
    for i, d in enumerate(data):
        ax.plot([i + 1 + (k % 7 - 3) * 0.03 for k in range(len(d))], d, ".", ms=2.5, alpha=0.35, color="#1f77b4")
        ax.text(i + 1, 0.32, f"p50 {st.median(d):.1f}s\nmax {max(d):.0f}s", ha="center", fontsize=7)
    stf = 120 if ph.startswith("P1") else 200
    ax.set_xticks(range(1, 7), [f"{m}x\n{int(float(m)*100)} s/g\n({float(m)*100/stf:.2f}x storm)" for m in tiers], fontsize=7)
    ax.set_yscale("log"); ax.set_ylim(0.25, 300); ax.grid(alpha=0.3, axis="y"); ax.set_title(title, fontsize=9)
axs[0].set_ylabel("submit -> accepted on virtual chain, seconds (log)")
fig.suptitle("Confirmation time by fee tier under load (TN10 storm 25 Sep 2026, one probe per tier every 30 s; no 1.5x tier was run)", fontsize=10)
fig.text(0.01, 0.01, "Source: TN10 ops (stp's TN10 setup). data/sep_fee_tier_probes.csv (logs/overload/probes.jsonl), data/sep_network_processed_tx_s_1min.csv. Whiskers = min/max.", fontsize=7, color="#555")
fig.tight_layout(rect=(0, 0.03, 1, 0.95)); fig.savefig(f"{H}/charts/2-confirmation-time-by-fee-tier.png", dpi=110); plt.close(fig)

# 2b. Sept probes over time with mempool backlog
fig, ax = plt.subplots(figsize=(13, 5))
cols = {"1": "#d62728", "1.2": "#ff7f0e", "2": "#2ca02c", "10": "#1f77b4"}
for m, c in cols.items():
    pp = [p for p in P if p["tier_x_min_feerate"] == m and p["inclusion_s"] and p["phase"] in ("P1-overload", "P4-max")]
    ax.semilogy([T(p["submit_utc"]) for p in pp], [F(p["inclusion_s"]) for p in pp], ".-", lw=0.4, ms=3, color=c, label=f"{m}x min feerate")
ax.set_ylabel("confirmation time, s (log)"); ax.grid(alpha=0.3)
ax2 = ax.twinx(); pm = [p for p in P if p["tier_x_min_feerate"] == "1" and p["mempool_at_cycle"]]
ax2.fill_between([T(p["submit_utc"]) for p in pm], [F(p["mempool_at_cycle"]) for p in pm], color="#999", alpha=0.18, lw=0, label="n0 mempool")
ax2.set_ylim(0, 120000); ax2.set_ylabel("n0 mempool (grey area)")
ax.axvline(T("2026-09-25 20:47:00"), color="k", lw=0.8, ls="--"); ax.text(T("2026-09-25 20:48:00"), 200, "storm fee 1.2x -> 2x", fontsize=8)
ax.xaxis.set_major_formatter(md.DateFormatter("%H:%M", tz=dt.timezone.utc)); ax.legend(loc="upper left", fontsize=8)
ax.set_title("Fee-tier probes over time, 25 Sep 2026 (UTC): cheap tiers wait when the mempool is deep", fontsize=10)
fig.text(0.01, 0.01, "Source: TN10 ops (stp's TN10 setup). data/sep_fee_tier_probes.csv (logs/overload/probes.jsonl)", fontsize=7, color="#555")
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(f"{H}/charts/2b-fee-tier-probes-over-time.png", dpi=110); plt.close(fig)
print("ok")
