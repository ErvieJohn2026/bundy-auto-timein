#!/data/data/com.termux/files/usr/bin/bash

cd ~/bundy-auto-timein

mkdir -p logs

source .venv/bin/activate

LOGFILE=logs/timein.log

echo "==================================" >> "$LOGFILE"
echo "Time In Started: $(date)" >> "$LOGFILE"

python main.py timein >> "$LOGFILE" 2>&1

echo "Finished: $(date)" >> "$LOGFILE"
echo "" >> "$LOGFILE"
