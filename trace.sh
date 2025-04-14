#!/bin/bash

sudo trace-cmd start -p function_graph -e sched*
python run.py &
PID=$!
#
echo $PID | sudo tee /sys/kernel/debug/tracing/set_ftrace_pid

wait $PID

# sudo trace-cmd show
sudo trace-cmd stop
sudo trace-cmd extract
sudo trace-cmd report
