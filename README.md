# Website Health Monitor

A Python script that checks whether websites are up. It runs once and exits. On macOS, `launchd` starts that same command again every 5 minutes.

## Run

From the project folder, pass the URL list:

```bash
.venv/bin/python main.py urls.txt
```

`urls.txt` has one address per line. Blank lines are skipped. The file in this repo uses `https://example.com` as a sample. Replace it with the sites you want to check.

## Result

Each check is appended to `websites_health.log`.

The script exits with a status code:

| Code | Meaning |
| --- | --- |
| 0 | Every website is healthy |
| 1 | At least one website failed |
| 2 | This computer has no network, so the list was not checked |

Code `2` comes from a separate probe, `http://captive.apple.com`. That address is not in `urls.txt`.

## Schedule on macOS

`com.website-health.plist` runs the check every 300 seconds. The script exits after each check, so the schedule does not use `KeepAlive`.

`launchd` does not expand `~`, and it does not know where this folder is on your computer. The plist uses this placeholder five times:

```text
/path/to/website-health-monitor
```

Replace that text with the full path of this folder. It appears in the Python path, `main.py`, `urls.txt`, `WorkingDirectory`, and `StandardErrorPath`.

Copy the edited file where `launchd` reads schedules, then load it:

```bash
cp com.website-health.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.website-health.plist
```

To remove the schedule:

```bash
launchctl bootout gui/$(id -u)/com.website-health
```
