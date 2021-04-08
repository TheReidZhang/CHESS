from flask import Flask, request, json
from chess.driver import Driver

app = Flask(__name__)
driver = Driver()


@app.route('/chess/info', methods=['POST'])
def fen():
    request_data = json.loads(request.data)
    ret = driver.get_info(request_data)
    return ret


@app.route('/chess/new', methods=['POST'])
def new():
    ret = driver.create_game()
    return ret


@app.route('/chess/update', methods=['POST'])
def result():
    request_data = json.loads(request.data)
    ret = driver.update_game(request_data)
    return ret


@app.route('/chess/<session>/<coordinate>', methods=['GET'])
def show(session, coordinate):
    session_id = int(session)
    ret = driver.get_checked_moves({"session_id": session_id, "coordinate": coordinate})
    return ret


@app.route('/resume', methods=['GET'])
def resume():
    return driver.resume_game()


if __name__ == '__main__':
    app.run(debug=True)
