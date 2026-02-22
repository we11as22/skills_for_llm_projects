---
name: terminal-power-user
description: Advanced terminal usage patterns that LLMs often miss. Use for any task involving watching processes, monitoring logs, disk analysis, directory inspection, process management, file searching, and productive shell workflows. Always apply when running services, debugging output, or exploring unfamiliar directories.
---

# Terminal Power User

## Overview

LLMs tend to use only basic shell commands and miss powerful patterns that make debugging, monitoring, and exploration dramatically faster. This skill defines the full set of techniques to apply proactively.

## When to Apply

Apply this skill whenever:
- Starting or waiting for a service/process to become ready
- Debugging output or errors from a running process
- Exploring an unfamiliar project or directory
- Checking disk space, file sizes, or structure
- Searching for patterns across files or logs

---

## 1. Process and Service Monitoring

### Watch logs for patterns while a service starts
```bash
# Tail and grep — show only relevant lines
tail -f service.log | grep -E "(ERROR|WARN|ready|started|port)"

# Poll every 5 seconds until pattern appears (don't just sleep and hope)
while ! grep -q "Application started" service.log 2>/dev/null; do
  echo "$(date +%T) — waiting..."; sleep 5
done && echo "Service ready."

# Watch a command repeat every 2 seconds
watch -n 2 "curl -s localhost:8080/health | python3 -m json.tool"

# Count matched lines in log to track progress
grep -c "processed" job.log

# Follow multiple log files at once
tail -f logs/app.log logs/worker.log

# Follow log and timestamp each line
tail -f app.log | ts '%H:%M:%.S'
```

### Process inspection
```bash
# Find process by name and see full args
ps aux | grep python
pgrep -la uvicorn

# See what ports a process listens on
ss -tlnp | grep LISTEN
lsof -i :8080

# Watch CPU/memory of a specific process
watch -n 1 "ps -p $(pgrep uvicorn) -o %cpu,%mem,pid,cmd"

# Kill by port
kill $(lsof -t -i:8080)

# Show process tree
pstree -p $(pgrep python)
```

---

## 2. File and Directory Analysis

### Sizes and counts — always check before assuming
```bash
# Disk usage of a directory, sorted, human-readable
du -sh * | sort -h

# Top 10 largest files in tree
find . -type f | xargs du -sh 2>/dev/null | sort -rh | head 10

# Count lines in all Python files
find . -name "*.py" | xargs wc -l | sort -n | tail 20

# Count files by extension
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn

# Size of a Docker image layer by layer
docker history IMAGE_NAME --human --format "{{.Size}}\t{{.CreatedBy}}"

# How much space logs are taking
du -sh /var/log/*
```

### Directory structure — inspect before editing
```bash
# Tree view with depth limit (don't ls -la blindly on unknown dirs)
find . -maxdepth 3 -type d | sort | sed 's|[^/]*/|  |g'

# Tree with file counts per directory
find . -type d | while read d; do
  echo "$(find "$d" -maxdepth 1 -type f | wc -l) $d"
done | sort -rn | head 20

# Show recently modified files (last 10 minutes)
find . -type f -newer /tmp/ts -mmin -10 | sort

# Show all files changed today
find . -type f -newer $(date -d "today 00:00" +%Y-%m-%d) 2>/dev/null

# Locate a file by name fast (before running find on huge tree)
locate -r 'settings\.py$' 2>/dev/null || find . -name "settings.py"
```

---

## 3. Log and Output Search

### Grep patterns an LLM often misses
```bash
# Case-insensitive, with context before and after
grep -i -A 3 -B 3 "error" app.log

# Show only unique errors (deduplicate)
grep "ERROR" app.log | sort -u

# Count occurrences per unique line
grep "ERROR" app.log | sort | uniq -c | sort -rn | head 20

# Find first occurrence of a pattern
grep -n -m 1 "FATAL" app.log

# Match one of several patterns
grep -E "(TimeoutError|ConnectionRefused|OOM)" app.log

# Negative match — show lines WITHOUT a pattern
grep -v "DEBUG" app.log | tail -50

# Search across all log files in directory
grep -r "Exception" logs/ --include="*.log" -l

# Live grep across multiple rotating logs
tail -F logs/*.log | grep --line-buffered "ERROR"
```

### Extract and count specific fields
```bash
# Count HTTP status codes from access log
awk '{print $9}' access.log | sort | uniq -c | sort -rn

# Extract all IPs that hit 500
awk '$9 == "500" {print $1}' access.log | sort | uniq -c | sort -rn

# Show lines 100-200 of a big file (don't cat the whole thing)
sed -n '100,200p' bigfile.log

# Tail last 1000 lines and search
tail -1000 app.log | grep "WARN"
```

---

## 4. Networking and Connectivity

```bash
# Check if a port is open (don't assume service is up)
nc -zv localhost 5432 && echo "postgres up" || echo "postgres down"
curl -sf http://localhost:8080/health && echo ok || echo fail

# Trace where a request goes
traceroute -n google.com

# DNS lookup timing
time dig google.com +noall +answer

# Show active connections grouped by state
ss -s

# Monitor bandwidth per process
nethogs eth0   # if installed

# Check TLS cert expiry
echo | openssl s_client -connect myhost.com:443 2>/dev/null | openssl x509 -noout -dates
```

---

## 5. Productive Shell Patterns

### History and reuse
```bash
# Find a previously run command fast
history | grep docker | tail 20

# Run last command as root
sudo !!

# Repeat last argument of previous command
mkdir /some/deep/path && cd $_
```

### Safe and parallel execution
```bash
# Run command and time it
time python3 train.py

# Run in background, capture output
nohup python3 worker.py > worker.out 2>&1 &

# Run N things in parallel with xargs
cat urls.txt | xargs -P 4 -I{} curl -sf {}

# Run on each file in parallel
find . -name "*.py" | xargs -P 8 python3 -m py_compile
```

### Output control
```bash
# Show progress on long pipe
pv data.csv | python3 process.py

# Tee to file AND see in terminal
python3 run.py 2>&1 | tee run.log

# Colorize output by pattern
grep --color=always "ERROR\|WARN\|" app.log

# Don't scroll: paginate long output
python3 -m json.tool big.json | less -S
```

---

## Rules

- **Never** run `sleep 30 && check` once. Use a `while` loop with `grep -q` to poll until ready.
- **Always** check sizes with `du -sh` before assuming something is small.
- **Always** use `wc -l` to understand how big a file is before reading it fully.
- **Always** use `find . -maxdepth N` to explore structure before running broad operations.
- **Prefer** `grep -c` + `grep -m 1` for quick log triage before tailing the whole file.
- **Use** `2>&1 | tee` when running anything that might need debugging — never lose output.
- **Check** port availability with `nc` or `ss` before assuming a service is up or down.

## Output Format

1. State which pattern applies to the current task
2. Show the exact command(s) with explanation
3. Note any risks (e.g. commands that can fill disk, kill wrong process)
