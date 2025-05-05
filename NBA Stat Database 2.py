
import tkinter as tk
from tkinter import messagebox
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
import pandas as pd
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Add requirements.txt"
git push



def fetch_player_id(player_name):
    # Search for the player using the nba_api static players module
    player_list = players.find_players_by_full_name(player_name)
    if not player_list:
        return None
    return player_list[0]['id']  # Return the first match's ID

def fetch_last_10_games(player_name, stat_type, stat_value):
    try:
        # Get player ID
        player_id = fetch_player_id(player_name)
        if not player_id:
            messagebox.showerror("Error", f"Player '{player_name}' not found!")
            return

        # Fetch the most recent game logs (up to 10 games)
        game_log = playergamelog.PlayerGameLog(player_id=player_id)
        games_df = game_log.get_data_frames()[0]

        # Ensure we're getting the latest 10 games
        last_10_games = games_df.head(10)

        # Check the selected stat type
        if stat_type == "Points":
            stat_column = "PTS"
        elif stat_type == "Rebounds":
            stat_column = "REB"
        elif stat_type == "Assists":
            stat_column = "AST"
        elif stat_type == "PRA":
            stat_column = "PTS"  # Combine points, rebounds, and assists
            last_10_games['PRA'] = last_10_games['PTS'] + last_10_games['REB'] + last_10_games['AST']
            stat_column = "PRA"

        # Filter games where the stat exceeds the threshold
        try:
            stat_value = int(stat_value) if stat_value.isdigit() else 0
        except ValueError:
            stat_value = 0
        high_stat_games = last_10_games[last_10_games[stat_column] >= stat_value]
        high_stat_count = high_stat_games.shape[0]

        # Display the games
        result_text.delete(1.0, tk.END)
        for index, row in last_10_games.iterrows():
            game_info = (
                f"Date: {row['GAME_DATE']}\n"
                f"Opponent: {row['MATCHUP']}\n"
                f"Points: {row['PTS']}, Rebounds: {row['REB']}, Assists: {row['AST']}, PRA: {row.get('PRA', 'N/A')}\n\n"
            )
            result_text.insert(tk.END, game_info)

        # Display the count of games above the threshold
        highlight_text.set(f"Games with {stat_value}+ {stat_type}: {high_stat_count} / 10")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")

# GUI Setup
root = tk.Tk()
root.title("NBA Player Last 10 Games Stats")

# Label and Textbox for player input
tk.Label(root, text="Enter Player Name:").grid(row=0, column=0, padx=5, pady=5)
player_name_entry = tk.Entry(root, width=30)
player_name_entry.grid(row=0, column=1, padx=5, pady=5)

# Label and Dropdown for stat selection
tk.Label(root, text="Select Stat:").grid(row=1, column=0, padx=5, pady=5)
stat_options = ["Points", "Rebounds", "Assists", "PRA"]
stat_dropdown = tk.StringVar(value=stat_options[0])  # Default to Points
stat_menu = tk.OptionMenu(root, stat_dropdown, *stat_options)
stat_menu.grid(row=1, column=1, padx=5, pady=5)

# Label and Textbox for stat threshold input
tk.Label(root, text="Enter Threshold Value:").grid(row=2, column=0, padx=5, pady=5)
threshold_entry = tk.Entry(root, width=10)
threshold_entry.grid(row=2, column=1, padx=5, pady=5)

# Fetch Button
fetch_button = tk.Button(
    root, 
    text="Fetch Stats", 
    command=lambda: fetch_last_10_games(player_name_entry.get(), stat_dropdown.get(), threshold_entry.get())
)
fetch_button.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

# Highlight Text for stat threshold
highlight_text = tk.StringVar()
highlight_label = tk.Label(root, textvariable=highlight_text)
highlight_label.grid(row=4, column=0, columnspan=3, pady=5)

# Result Display
result_text = tk.Text(root, height=20, width=50)
result_text.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Exit Button
exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.grid(row=6, column=1, pady=5)

root.mainloop()


# In[ ]:





# In[ ]:




