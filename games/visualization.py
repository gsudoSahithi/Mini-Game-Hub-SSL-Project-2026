import matplotlib.pyplot as plt
import os
# Top 5 players by wins (bar chart)
# Game distribution (pie chart)
# Get current directory path
curr_dir = os.path.dirname(os.path.abspath(__file__))

history_path = os.path.join(curr_dir, "..", "history.csv")

#List of games in project
games = ["TicTacToe", "Connect4", "Othello"]

#Read game history file
with open(history_path, "r") as file:
    data = file.readlines()

    #Dictionary to store total wins per player
    total_wincount = {}

    # Dictionary to store number of matches per game
    game_count_dict = {game: 0 for game in games}
    for line in data:
        parts = line.strip().split(",")

        #Skip invalid rows
        if len(parts) != 4:
            continue

        winner, loser, date, game = parts

        #Count wins 
        if winner != "draw" and loser != "draw":
            total_wincount[winner] = total_wincount.get(winner, 0) + 1

        #Count number of games played per game type
        if game in game_count_dict:
            game_count_dict[game] += 1

    #Convert game counts into list for plotting
    game_count = [game_count_dict[game] for game in games]
    plt.subplot(1, 2, 1)

    #Get top 5 players sorted by win count
    top5 = sorted(total_wincount.items(), key=lambda x: x[1], reverse=True)[:5]

    #Separate names and win counts
    top_5_players = [player for player, count in top5]
    win_count = [count for player, count in top5]

    #Bar chart for top players
    plt.bar(top_5_players, win_count, color='r', width=0.5)
    plt.title("Top 5 Players")
    #Pie chart
    plt.subplot(1, 2, 2)

    #Pie chart showing distribution of games played
    plt.pie(game_count, labels=games, autopct='%1.1f%%')
    plt.title("Games Played Distribution")

    #Adjust layout to avoid overlap
    plt.tight_layout()

    #Show final plots
    plt.show()
