#!/bin/bash
#Leaderboard script for game results
#Calculating Wins, Losses, Win/Loss Ratio
metric=$1

# Decide sorting column based on metric
if [ "$metric" == "wins" ]; then
    sort_key=2
elif [ "$metric" == "losses" ]; then
    sort_key=3
elif [ "$metric" == "ratio" ]; then
    sort_key=4
else
    echo "Invalid metric. Use 'wins', 'losses', or 'ratio'."
    exit 1
fi

#Print leaderboard header
echo "================================="
echo "          LEADERBOARD          "
echo "================================="

#Declare associative arrays to store stats
declare -A wins
declare -A losses
#Read history.csv and computes stats
while IFS="," read -r winner loser date game; do

    # Ignore draw games
    if [[ "$winner" != "draw" && "$loser" != "draw" ]]; then

        # Increase win count for winner
        ((wins["$game|$winner"]++))

        # Increase loss count for loser
        ((losses["$game|$loser"]++))
    else
        continue
    fi

#Skip header row using tail
done < <(tail -n +2 history.csv)
#Print leaderboard game by game
for game in "TicTacToe" "Othello" "Connect4"; do

    echo "Game: $game"
    echo "---------------------------------"

    #Table header
    printf "%-10s %-6s %-8s %-6s\n" "User" "Wins" "Losses" "Ratio"

    {
        #Loop through all recorded wins
        for key in "${!wins[@]}"; do

            # Filter only current game entries
            if [[ $key == "$game"* ]]; then

                # Extract username from key (game|user)
                user=$(echo "$key" | cut -d'|' -f2)

                # Get stats (default 0 if not found)
                win_count=${wins[$key]:-0}
                loss_count=${losses[$key]:-0}

                # Compute win/loss ratio
                if [ $loss_count -eq 0 ]; then
                    ratio="inf"
                else
                    ratio=$(awk "BEGIN {printf \"%.2f\", $win_count/$loss_count}")
                fi

                # Print formatted row
                printf "%-10s %-6d %-8d %-6s\n" "$user" "$win_count" "$loss_count" "$ratio"
            fi
        done

    # Sort based on selected metric
    } | sort -k"$sort_key","$sort_key"gr

    echo " "
done
echo "================================="
echo "Sorted by: $metric"
