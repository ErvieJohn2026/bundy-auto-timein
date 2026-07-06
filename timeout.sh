#!/data/data/com.termux/files/usr/bin/bash

cd ~/bundy-auto-timein

mkdir -p logs

source .venv/bin/activate

LOGFILE=logs/timeout.log

echo "==================================" >> "$LOGFILE"
echo "Time In Started: $(date)" >> "$LOGFILE"

python main.py timeout >> "$LOGFILE" 2>&1

echo "Finished: $(date)" >> "$LOGFILE"
echo "" >> "$LOGFILE"
