import matplotlib.pyplot as plt
import os
curr_dir=os.path.dirname(os.path.abspath(__file__))
history_path=os.path.join(curr_dir,"..","history.csv")
games=["TicTacToe","Connect4","Othello"]
with open(history_path, "r") as file:
    data = file.readlines()
    total_wincount={}
    game_count_dict={game:0 for game in games}
    for line in data:
        parts=line.strip().split(",")
        if len(parts)!=4:
            continue
        winner,loser,date,game=parts
        if winner!="draw" and loser!="draw":
            total_wincount[winner]=total_wincount.get(winner,0)+1
        if game in game_count_dict:
            game_count_dict[game]+=1
        game_count=[game_count_dict[game] for game in games]
    plt.subplot(1,2,1)
    top5=sorted(total_wincount.items(),key=lambda x:x[1],reverse=True)[:5]#contains pairs of top5 players and their win count
    top_5_players=[player for player, count in top5]
    win_count=[count for player, count in top5]
    plt.bar(top_5_players,win_count,color='r',width=0.5)
    plt.subplot(1,2,2)
    plt.pie(game_count,labels=games,autopct='%1.1f%%')
    plt.tight_layout()
    plt.show()
