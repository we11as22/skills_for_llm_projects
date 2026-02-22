# Terminal Power User Reference

## Quick Decision Table

| Situation | Command family to reach for |
|-----------|----------------------------|
| Service starting, need to wait | `while ! grep -q PATTERN log; do sleep 5; done` |
| How big is this file/dir? | `du -sh`, `wc -l`, `wc -c` |
| What's in this directory? | `find . -maxdepth 3 -type d` |
| Where are errors? | `grep -c "ERROR"`, then `grep -B3 -A3 "ERROR"` |
| Is the port open? | `nc -zv host port` |
| What's eating disk? | `du -sh * \| sort -h` |
| Log too big to tail? | `tail -1000`, `sed -n '100,200p'` |
| Need to repeat until done | `watch -n 2 "cmd"` |
| Many files to process? | `xargs -P 4` |

## Common Mistakes to Avoid

- Using `sleep 60` then checking once → use a polling loop instead
- Running `cat bigfile` → check `wc -l` first, then `head`/`tail`/`sed`
- Running `find .` on `/` or huge dirs without `-maxdepth` → always limit depth first
- Assuming a service started because the process is running → check port with `nc` or `curl`
- Losing stderr output → always use `2>&1 | tee filename.log` for long jobs
- Running `kill -9` immediately → try `kill` (SIGTERM) first, wait 3s, then escalate
