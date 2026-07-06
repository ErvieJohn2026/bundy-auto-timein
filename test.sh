#!/data/data/com.termux/files/usr/bin/bash

cd ~/bundy-auto-timein

mkdir -p logs

source .venv/bin/activate

echo "======================================" >> logs/test.log
echo "Started: $(date)" >> logs/test.log

python test.py >> logs/test.log 2>&1

echo "Finished: $(date)" >> logs/test.log
echo "" >> logs/test.log
