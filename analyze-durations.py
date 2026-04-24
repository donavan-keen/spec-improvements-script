#!/usr/bin/env python3
import csv
import sys
from datetime import datetime, timezone

def parse_dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def analyze(path):
    total_seconds = 0
    successes = 0
    failures = 0
    with open(path) as f:
        for row in csv.reader(f):
            if len(row) < 5:
                continue
            conclusion = row[2].strip()
            if conclusion not in ("success", "failure"):
                continue
            try:
                started = parse_dt(row[3].strip())
                updated = parse_dt(row[4].strip())
            except ValueError:
                continue
            total_seconds += (updated - started).total_seconds()
            if conclusion == "success":
                successes += 1
            else:
                failures += 1
    count = successes + failures
    avg = total_seconds / count if count else None
    failure_rate = failures / count if count else None
    return avg, failure_rate, count

def fmt(seconds):
    minutes, secs = divmod(int(abs(seconds)), 60)
    return f"{minutes}m {secs}s"

if __name__ == "__main__":
    files = sys.argv[1:] if len(sys.argv) > 1 else ["tmp/before.csv"]
    results = []
    for path in files:
        avg, failure_rate, count = analyze(path)
        if avg is None:
            print(f"{path}: no matching rows")
        else:
            print(f"{path}: avg duration = {fmt(avg)}  failure rate = {failure_rate*100:.1f}%  ({count} runs)")
        results.append((avg, failure_rate))

    if len(results) == 2 and all(r[0] is not None for r in results):
        before_avg, before_fr = results[0]
        after_avg, after_fr = results[1]

        dur_delta = after_avg - before_avg
        dur_pct = (dur_delta / before_avg) * 100

        fr_delta = (after_fr - before_fr) * 100
        fr_pct = (fr_delta / (before_fr * 100)) * 100

        print(f"\nchange: duration {dur_pct:+.1f}% ({fmt(dur_delta)})  failure rate {fr_delta:+.1f}pp ({fr_pct:+.1f}%)")
