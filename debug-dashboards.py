#!/usr/bin/env python3
import json

# Load the working dashboard as template
with open('dashboards/honeypot-attacks.json', 'r') as f:
    working = json.load(f)

# Extract a working panel and target structure
working_panel_stat = working['panels'][0]  # First stat panel
working_target = working_panel_stat['targets'][0]

print("Working target structure:")
print(json.dumps(working_target, indent=2))
print("\n" + "="*60 + "\n")

# Load our broken dashboard
with open('dashboards/ssh-attacks.json', 'r') as f:
    broken = json.load(f)

broken_panel = broken['panels'][0]
broken_target = broken_panel['targets'][0]

print("Broken target structure:")
print(json.dumps(broken_target, indent=2))
print("\n" + "="*60 + "\n")

print("Key differences:")
print(f"Cache duration: {working_target.get('cacheDurationSeconds')} vs {broken_target.get('cacheDurationSeconds')}")
print(f"Field order in target: {list(working_target.keys())} vs {list(broken_target.keys())}")
