#!/bin/bash
#Design for leaderboard
metric=$1
if [ $metric == "wins" ]; then
    sort_key=2
elif [ $metric == "losses" ]; then
    sort_key=3
elif [ $metric == "ratio" ]; then
    sort_key=4
else
    echo "Invalid metric. Use 'wins', 'losses', or 'ratio'."
    exit 1
fi
echo =================================
echo "          LEADERBOARD          "
echo =================================
#logic for storing wins and loses of a player in a particular game
declare -A wins
declare -A losses
while IFS="," read -r winner loser date game; do
    ((wins["$game|$winner"]++))
    ((losses["$game|$loser"]++))
 done < <(tail -n +2 history.csv)

 echo "================================="
 echo "Sorted by: $metric"
