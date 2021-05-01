from flask import Flask, request, json
from api.api import ChessAPI


def create_app(db_url="init"):
    app = Flask(__name__)
    driver = ChessAPI(db_url)

    @app.route('/chess/info', methods=['POST'])
    def fen():
        request_data = json.loads(request.data)
        ret = driver.get_info(request_data)
        return ret

    @app.route('/chess/new', methods=['POST'])
    def new():
        request_data = json.loads(request.data)
        mode = request_data["mode"]
        user = request_data["user"]
        ret = driver.create_game(user, mode)
        return ret

    @app.route('/chess/update', methods=['POST'])
    def result():
        request_data = json.loads(request.data)
        return driver.update_game(request_data)

    @app.route('/chess/<session_id>/<coordinate>', methods=['POST'])
    def show(session_id, coordinate):
        session_id = int(session_id)
        user = json.loads(request.data)["user"]
        ret = driver.get_checked_moves({"session_id": session_id, "coordinate": coordinate}, user)
        return ret

    @app.route('/resume', methods=['POST'])
    def resume():
        request_data = json.loads(request.data)
        return driver.resume_game(request_data["user"])

    @app.route('/replays', methods=['POST'])
    def replays():
        request_data = json.loads(request.data)
        return driver.replay_game(request_data["user"])

    @app.route('/undo', methods=['POST'])
    def undo():
        request_data = json.loads(request.data)
        return driver.undo(request_data["user"], request_data["session_id"])

    @app.route('/replay', methods=['POST'])
    def replay():
        request_data = json.loads(request.data)
        user = request_data["user"]
        session_id = request_data["session_id"]
        step = request_data["step"]
        return driver.replay(user, session_id, step)

    # for user account
    @app.route('/signup', methods=['POST'])
    def signup():
        request_data = json.loads(request.data)
        return driver.sign_up(request_data)

    @app.route('/login', methods=['POST'])
    def sign_in():
        request_data = json.loads(request.data)
        return driver.login(request_data)

    @app.route('/user', methods=['POST'])
    def user_info():
        request_data = json.loads(request.data)
        return driver.get_user_info(request_data["user"])

    return app


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5000)
