from flask import Flask, render_template, request, jsonify
from chess_logic import ChessVar

app = Flask(__name__)
game = ChessVar()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_board', methods=['GET'])
def get_board():
    perspective = request.args.get("perspective", "audience")
    if perspective == "current":
        perspective = game._player_turn
    board = game.get_board(perspective)
    return jsonify({
        'board': board,
        'game_state': game.get_game_state(),
        'turn': game._player_turn
    })

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    source = data['source']
    target = data['target']
    fog = data.get('fog', False)

    start = f"{chr(int(source['col']) + 97)}{8 - int(source['row'])}"
    end = f"{chr(int(target['col']) + 97)}{8 - int(target['row'])}"

    valid = game.make_move(start, end)
    perspective = game._player_turn if fog else 'audience'
    board = game.get_board(perspective)

    return jsonify({
        'success': valid,
        'board': board,
        'game_state': game.get_game_state(),
        'turn': game._player_turn
    })

@app.route('/reset', methods=['POST'])
def reset():
    global game
    game = ChessVar()
    return jsonify({'message': 'Game reset'})

if __name__ == '__main__':
    # Optional: set a custom port here if needed
    app.run()