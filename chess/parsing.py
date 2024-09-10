import pandas as pd
import chess.pgn
import datetime

# Function to parse PGN file and extract required information
def parse_pgn(file_path):
    games_data = []
    with open(file_path, 'r') as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break
            
            # Extract game information
            game_info = {}
            game_info['Date'] = game.headers.get('Date', 'Unknown')
            game_info['Time'] = game.headers.get('Time', 'Unknown')
            game_info['Opening'] = game.headers.get('Opening', 'Unknown')
            game_info['White'] = game.headers.get('White', 'Unknown')
            game_info['Black'] = game.headers.get('Black', 'Unknown')
            
            # Determine the color of 'marcosdedeu'
            if game_info['White'] == 'marcosdedeu':
                game_info['Color'] = 'White'
            elif game_info['Black'] == 'marcosdedeu':
                game_info['Color'] = 'Black'
            else:
                game_info['Color'] = 'Unknown'
            
            # Calculate time between each move
            moves = list(game.mainline_moves())
            move_times = []
            for move in moves:
                # Here we would calculate the time between moves if we had timestamps
                # For now, we will just append a placeholder
                move_times.append('N/A')
            game_info['MoveTimes'] = move_times
            
            games_data.append(game_info)
    
    return pd.DataFrame(games_data)

# Parse the PGN file
pgn_file_path = 'lichess_marcosdedeu_2024-09-10.pgn'
games_df = parse_pgn(pgn_file_path)

# Display the head of the dataframe
games_df.head()
