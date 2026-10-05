#!/usr/bin/env python3
"""Build the small CSV extracts in data/ from the raw TN10 storm logs on stp's box.
Raw inputs (not in this repo, sizes in README):
  Oct storm  : stress-tests/data/{runner1-4,p2w1-8}.out ('rep' lines every 10 s), host.jsonl (15 s),
               storm-watch.jsonl (15 s), api-health-min.jsonl (120 s)
  Sept storm : tn10-break-test-2026-09-25/logs/overload/probes.jsonl (fee-tier probes, every 30 s),
               logs/tps12h/nettps.jsonl (network included tx/s)
All times written in CEST (UTC+2). Nothing is estimated: every value is a logged value, a difference
of logged cumulative counters, or a min/median/max of logged samples."""
import json, glob, csv, os, sys, statistics as st, datetime as dt, collections
OCT = sys.argv[1] if len(sys.argv) > 1 else "/workspace/artifacts/stress-tests/data"
SEP = sys.argv[2] if len(sys.argv) > 2 else "/workspace/tn10-break-test-2026-09-25/logs"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
CEST = dt.timezone(dt.timedelta(hours=2))
def E(s):
    s = s.replace("Z", "+00:00")
    if len(s) > 5 and s[-5] in "+-" and s[-3] != ":": s = s[:-2] + ":" + s[-2:]
    return dt.datetime.fromisoformat(s).timestamp()
def C(ts, fmt="%Y-%m-%d %H:%M:%S"): return dt.datetime.fromtimestamp(ts, CEST).strftime(fmt)
def jl(path):
    for l in open(path):
        if l.startswith("{"):
            try: yield json.loads(l)
            except Exception: pass

# ---------- 1. runner segments (restart = cumulative 'submitted' goes down, or a 'final' line) ----------
segs = []; tgt = collections.defaultdict(list); paus = collections.Counter()
for f in sorted(glob.glob(f"{OCT}/runner[0-9].out")) + sorted(glob.glob(f"{OCT}/p2w[0-9].out")):
    cur = None
    for j in jl(f):
        ev = j.get("ev")
        if ev == "rep":
            t = E(j["t"]); s, a = j.get("submitted", 0), j.get("accepted", 0)
            if cur is None or cur["final"] or s < cur["pts"][-1][1]:
                if cur: segs.append(cur)
                cur = dict(file=os.path.basename(f), tag=j["tag"], pts=[], final=False, fr=[], lat=None)
            cur["pts"].append((t, s, a)); cur["fr"].append(j.get("feerate"))
            mm = int(t) - int(t) % 60; tgt[(mm, j["tag"])].append(0 if j.get("paused") else (j.get("rate") or 0)); paus[mm] += 1 if j.get("paused") else 0
            if j.get("lat_p50") is not None: cur["lat"] = (t, j["lat_p50"], j["lat_p95"], a)
        elif ev == "final" and cur and not cur["final"]:
            t = E(j["t"]); cur["pts"].append((t, j["submitted"], max(j["accepted_seen_vcc"], cur["pts"][-1][2]))); cur["final"] = True
    if cur: segs.append(cur)

# spread each interval's increments evenly over its seconds, then sum per minute
sub = collections.Counter(); acc = collections.Counter(); active = collections.defaultdict(set)
for g in segs:
    pts = [(g["pts"][0][0] - 10, 0, 0)] + g["pts"]
    for (t0, s0, a0), (t1, s1, a1) in zip(pts, pts[1:]):
        t0, t1 = int(t0), int(t1)
        if t1 <= t0: continue
        ds, da = max(0, s1 - s0) / (t1 - t0), max(0, a1 - a0) / (t1 - t0)
        for x in range(t0, t1):
            m = x - x % 60; sub[m] += ds; acc[m] += da
            if ds > 0: active[m].add(g["tag"])

# host.jsonl: n0 mempool + n0 processed tx/s (all senders, block bodies) per minute
mp = collections.defaultdict(list); proc = collections.defaultdict(list); disk = collections.defaultdict(list)
for j in jl(f"{OCT}/host.jsonl"):
    if j.get("type") != "host": continue
    t = int(E(j["ts"])); m = t - t % 60
    if j.get("mempool") is not None: mp[m].append(j["mempool"])
    r = (j.get("rate") or {}).get("tx_processed_per_s")
    if r is not None: proc[m].append(r)
    if j.get("disk_free_gb") is not None: disk[m].append(j["disk_free_gb"])
pauses = collections.defaultdict(list)
for j in jl(f"{OCT}/storm-watch.jsonl"):
    if j.get("pause"):
        t = int(E(j["t"])); pauses[t - t % 60].append(j["pause"])

lo = min(list(sub) + list(mp)); hi = max(list(sub) + list(mp))
# restrict to the storm days 1-3 Oct
lo = max(lo, int(E("2026-10-01T20:00:00+02:00"))); hi = min(hi, int(E("2026-10-03T02:00:00+02:00")))
with open(f"{OUT}/oct_box_submitted_vs_accepted_1min.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    tgt_m = collections.Counter()
    for (mm, tag), v in tgt.items(): tgt_m[mm] += st.mean(v)
    w.writerow(["minute_cest", "box_target_rate_tx_s", "runner_reps_paused", "box_submitted_tx_s", "box_accepted_tx_s", "runners_sending", "n0_mempool_min", "n0_mempool_median", "n0_mempool_max",
                "n0_processed_tx_s_all_senders", "disk_free_gb_min", "storm_watch_pause_flags"])
    for m in range(lo, hi + 1, 60):
        mm = mp.get(m, []); pp = proc.get(m, []); dd = disk.get(m, [])
        w.writerow([C(m, "%Y-%m-%d %H:%M"), round(tgt_m[m]), paus[m], round(sub[m] / 60, 1), round(acc[m] / 60, 1), len(active[m]),
                    min(mm) if mm else "", int(st.median(mm)) if mm else "", max(mm) if mm else "",
                    round(st.mean(pp), 1) if pp else "", min(dd) if dd else "", len(pauses.get(m, []))])

# runner latency: lat_p50/p95 in a 'rep' line are percentiles over ALL txs the process saw accepted since it started
with open(f"{OUT}/oct_runner_latency_cumulative_by_segment.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["file", "tag", "segment_start_cest", "segment_end_cest", "feerate_sompi_per_gram_first", "feerate_last", "submitted", "accepted_seen_on_n0_virtual_chain",
                "last_rep_cest", "lat_p50_s_cumulative", "lat_p95_s_cumulative"])
    for g in segs:
        if not g["lat"] or g["pts"][-1][1] < 10000: continue
        fr = [x for x in g["fr"] if x is not None]
        w.writerow([g["file"], g["tag"], C(g["pts"][0][0] - 10), C(g["pts"][-1][0]), fr[0] if fr else "", fr[-1] if fr else "",
                    g["pts"][-1][1], g["pts"][-1][2], C(g["lat"][0]), round(g["lat"][1] / 1000, 2), round(g["lat"][2] / 1000, 2)])

# ---------- 3. api-tn10 indexer health, with box accepted tx/s and n0 processed tx/s at the same minute ----------
with open(f"{OUT}/oct_api_tn10_health_2min.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["time_cest", "http", "error", "indexer_lag_s_acceptedTxBlockTimeDiff", "db_isSynced", "stall_suspected", "box_accepted_tx_s_that_minute", "n0_processed_tx_s_that_minute"])
    for j in jl(f"{OCT}/api-health-min.jsonl"):
        if j.get("type") != "health": continue
        t = int(E(j["ts"])); m = t - t % 60
        if not (lo <= t <= hi): continue
        pp = proc.get(m, [])
        w.writerow([C(t), j.get("http", ""), (j.get("error") or "")[:40], j.get("acceptedTxBlockTimeDiff", ""), j.get("db_isSynced", ""), j.get("stall_suspected", ""),
                    round(acc[m] / 60, 1), round(st.mean(pp), 1) if pp else ""])

# ---------- 2. Sept fee-tier probes ----------
P = list(jl(f"{SEP}/overload/probes.jsonl")); s_ = {}; a_ = {}
for r in P:
    if r["ev"] == "submit": s_[r["id"]] = r
    elif r["ev"] == "accepted": a_[r["id"]] = r
cyc = sorted((E(r["t"]), int(r["mempool"])) for r in P if r["ev"] == "cycle")
def mp_at(t):
    best = None
    for tc, m in cyc:
        if tc <= t + 1: best = m
        else: break
    return best
with open(f"{OUT}/sep_fee_tier_probes.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["submit_cest", "phase", "storm_feerate_sompi_g", "tier_x_min_feerate", "probe_feerate_sompi_g", "tier_vs_storm_fee", "mass", "ok", "accepted", "inclusion_s", "mempool_at_cycle"])
    for i, r in sorted(s_.items()):
        stf = 120 if r["phase"].startswith("P1") else (200 if r["phase"].startswith("P4") else "")
        a = a_.get(i)
        fr = int(r["fee"]) / int(r["mass"])
        w.writerow([C(E(r["t"])), r["phase"], stf, r["mult"], round(fr), round(fr / stf, 2) if stf else "", r["mass"], r["ok"], bool(a),
                    a["lat_s"] if a else "", mp_at(E(r["t"]))])
# kaspad "Processed" tx/s (block-body count, not unique) during the Sept probe window, per minute
nt = collections.defaultdict(list)
t_lo, t_hi = E("2026-09-25T21:45:00+02:00"), E("2026-09-25T23:55:00+02:00")
for j in jl(f"{SEP}/tps12h/nettps.jsonl"):
    t = E(j["t"])
    if t_lo <= t <= t_hi and j.get("net_tps") is not None: nt[int(t - t % 60)].append(j["net_tps"])
with open(f"{OUT}/sep_network_processed_tx_s_1min.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["minute_cest", "network_processed_tx_s_block_bodies_mean", "samples"])
    for m in sorted(nt): w.writerow([C(m, "%Y-%m-%d %H:%M"), round(st.mean(nt[m]), 1), len(nt[m])])
print("segments", len(segs), "minutes", (hi - lo) // 60 + 1)

# ---------- summary tables used in the README ----------
def pct(a, p):  # same linear interpolation as analyze-overload.py
    a = sorted(a); k = (len(a) - 1) * p / 100; f = int(k); c = min(f + 1, len(a) - 1)
    return round(a[f] + (a[c] - a[f]) * (k - f), 2)
rows = list(csv.DictReader(open(f"{OUT}/sep_fee_tier_probes.csv")))
with open(f"{OUT}/sep_fee_tier_summary.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["phase", "window_cest", "storm_feerate", "tier_x_min", "probe_feerate", "tier_vs_storm_fee", "sent", "accepted", "p50_s", "p90_s", "max_s", "over_30s", "over_60s"])
    for ph, win in (("P1-overload", "21:48:41-22:46:14"), ("P4-max", "22:47:26-23:50:41")):
        for m in ("1", "1.2", "2", "5", "10", "100"):
            s = [r for r in rows if r["phase"] == ph and r["tier_x_min_feerate"] == m]; l = [float(r["inclusion_s"]) for r in s if r["inclusion_s"]]
            w.writerow([ph, win, s[0]["storm_feerate_sompi_g"], m, s[0]["probe_feerate_sompi_g"], s[0]["tier_vs_storm_fee"], len(s), len(l), pct(l, 50), pct(l, 90), max(l), sum(x > 30 for x in l), sum(x > 60 for x in l)])
hr = list(csv.DictReader(open(f"{OUT}/oct_api_tn10_health_2min.csv"))); B = collections.defaultdict(lambda: [0, 0, 0])
for r in hr:
    p = r["n0_processed_tx_s_that_minute"]
    if p == "": continue
    k = min(int(float(p) // 1000) * 1000, 7000); lag = float(r["indexer_lag_s_acceptedTxBlockTimeDiff"] or 0)
    B[k][0] += 1; B[k][1] += r["http"] != "200"; B[k][2] += (r["http"] == "200" and lag > 120)
with open(f"{OUT}/oct_api_bad_samples_by_n0_processed_tps.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["n0_processed_tx_s_bin", "health_samples", "non_200_or_timeout", "http200_but_lag_over_120s", "bad_share_pct"])
    for k in sorted(B): n, a, b = B[k]; w.writerow([f"{k}-{k+999}" if k < 7000 else "7000+", n, a, b, round(100 * (a + b) / n)])

# ---------- sequencing: send order vs accept order among the 25 Sep probes (same tier) ----------
# accept time = submit time (ms) + lat_s; acceptance was polled every 1 s, so a pair counts as reversed only if
# the later-sent probe was accepted more than 1.0 s before the earlier-sent one.
import itertools
with open(f"{OUT}/sep_probe_order_by_tier.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["phase", "tier_x_min_feerate", "tier_vs_storm_fee", "probes", "consecutive_pairs", "consecutive_reversed", "consecutive_reversed_pct",
                "all_pairs", "all_pairs_reversed", "all_pairs_reversed_pct", "probes_overtaken_by_a_later_probe", "stalled_behind_2plus_later_probes", "max_overtake_s"])
    for ph in ("P1-overload", "P4-max"):
        stf = 120 if ph.startswith("P1") else 200
        for m in (1, 1.2, 2, 5, 10, 100):
            v = sorted((E(s_[i]["t"]), E(s_[i]["t"]) + a_[i]["lat_s"]) for i in s_ if s_[i]["phase"] == ph and s_[i]["mult"] == m and i in a_)
            cons = sum(1 for (s1, x1), (s2, x2) in zip(v, v[1:]) if x2 < x1 - 1.0)
            allp = list(itertools.combinations(v, 2)); rev = [(x1 - x2) for (s1, x1), (s2, x2) in allp if x2 < x1 - 1.0]
            over = sum(1 for k, (s1, x1) in enumerate(v) if any(x2 < x1 - 1.0 for s2, x2 in v[k + 1:]))
            stall = sum(1 for k, (s1, x1) in enumerate(v) if sum(1 for s2, x2 in v[k + 1:] if x2 < x1 - 1.0) >= 2)
            w.writerow([ph, m, round(m * 100 / stf, 2), len(v), len(v) - 1, cons, round(100 * cons / (len(v) - 1), 1), len(allp), len(rev),
                        round(100 * len(rev) / len(allp), 2), over, stall, round(max(rev), 1) if rev else 0])
