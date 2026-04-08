#Displays leaderboard for all games
#logic for sorting and main content of leaderboard
for game in "TicTacToe" "Othello" "Connect4" ; do
 echo  "Game: $game"
 echo "---------------------------------"
 printf "%-10s %-6s %-8s %-6s\n" "User" "Wins" "Losses" "Ratio"
 {
    for key in "${!wins[@]}"; do
    if [[ $key == "$game"* ]]; then
        user=$(echo "$key" | cut -d'|' -f2)
        win_count=${wins[$key]:-0}
        loss_count=${losses[$key]:-0}
        if [ $loss_count -eq 0 ]; then
            ratio="inf"
        else
            ratio=$(awk "BEGIN {printf \"%.2f\", $win_count/$loss_count}")
        fi
        printf "%-10s %-6d %-8d %-6s\n" "$user" "$win_count" "$loss_count" "$ratio"
    fi
    done
 } | sort -k"$sort_key","$sort_key"gr
 echo " "
 done 
