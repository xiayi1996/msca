#!/bin/sh

# Script for following up *.result files of short assembly calculations

session="short"

# set up tmux
tmux start-server

# check if the session exists, discarding output
# we can check $? for the exit status (zero for success, non-zero for failure)
tmux has-session -t $session 2>/dev/null

if [ $? != 0 ]; then

  # view pane titles at the top
  tmux set pane-border-status top
  tmux set pane-border-format ' #{pane_index} #{pane_title} '

  # create a new tmux session
  tmux new-session -d -s $session

  # select pane 0 and split horizontally by 50%
  tmux selectp -t 0
  tmux splitw -h -p 50

  # select pane 1 and split vertically by 50%
  tmux selectp -t 1
  tmux splitw -v -p 50

  # select pane 0 and split vertically by 50%
  tmux selectp -t 0
  tmux splitw -v -p 50

  tmux selectp -t 0 -T "ASSEMBLY_A_SHORT"
  tmux send-keys "tail -f -n +1 $(ls -td -- /tmp/ASSEMBLY_A_SHORT/output*/ | head -n 1)*.result | nl" C-m
  tmux selectp -t 1 -T "ASSEMBLY_B_SHORT"
  tmux send-keys "tail -f -n +1 $(ls -td -- /tmp/ASSEMBLY_B_SHORT/output*/ | head -n 1)*.result | nl" C-m
  tmux selectp -t 2 -T "ASSEMBLY_C_SHORT"
  tmux send-keys "tail -f -n +1 $(ls -td -- /tmp/ASSEMBLY_C_SHORT/output*/ | head -n 1)*.result | nl" C-m
  tmux selectp -t 3 -T "ASSEMBLY_D_SHORT"
  tmux send-keys "tail -f -n +1 $(ls -td -- /tmp/ASSEMBLY_D_SHORT/output*/ | head -n 1)*.result | nl" C-m
  # return to main window
  tmux selectp -t 0
  tmux select-window -t $session:0

fi

# finished setup, attach to the tmux session
tmux attach-session -t $session
