from flask import Flask, request, json, session
from api.api import ChessAPI


def create_app(db_url="init"):
    app = Flask(__name__)
    app.secret_key = "TEAM5"
    driver = ChessAPI(db_url)

    @app.route('/chess/info', methods=['POST'])
    def fen():
        if "user" in session:
            request_data = json.loads(request.data)
            ret = driver.get_info(request_data, session["user"])
            return ret
        return {"valid": False}

    @app.route('/chess/new', methods=['POST'])
    def new():
        if "user" in session:
            mode = json.loads(request.data)["mode"]
            ret = driver.create_game(session["user"], mode)
            return ret
        return {"valid": False}

    @app.route('/chess/update', methods=['POST'])
    def result():
        if "user" in session:
            request_data = json.loads(request.data)
            ret = driver.update_game(request_data, session["user"])
            return ret
        return {"valid": False}

    @app.route('/chess/<session_id>/<coordinate>', methods=['GET'])
    def show(session_id, coordinate):
        if "user" in session:
            session_id = int(session_id)
            ret = driver.get_checked_moves({"session_id": session_id, "coordinate": coordinate}, session["user"])
            return ret
        return {"valid": False}

    @app.route('/resume', methods=['GET'])
    def resume():
        if "user" in session:
            return driver.resume_game(session["user"])
        return {"valid": False}

    @app.route('/replays', methods=['GET'])
    def replays():
        if "user" in session:
            return driver.replay_game(session["user"])
        return {"valid": False}

    @app.route('/undo', methods=['POST'])
    def undo():
        if "user" in session:
            request_data = json.loads(request.data)
            return driver.undo(session["user"], request_data["session_id"])
        return {"valid": False}

    @app.route('/replay', methods=['POST'])
    def replay():
        if "user" in session:
            request_data = json.loads(request.data)
            return driver.replay(session["user"], request_data["session_id"], request_data["step"])
        return {"valid": False}

    # for user account
    @app.route('/signup', methods=['POST'])
    def signup():
        request_data = json.loads(request.data)
        ret = driver.sign_up(request_data)
        return ret

    @app.route('/login', methods=['POST'])
    def sign_in():
        request_data = json.loads(request.data)
        ret = driver.login(request_data)
        if ret["valid"]:
            session["user"] = request_data["username"]
        return ret

    @app.route('/logout', methods=['GET'])
    def logout():
        session.pop("user", None)
        return {"msg": "logged out"}

    @app.route('/user', methods=['GET'])
    def user_info():
        if "user" in session:
            ret = driver.get_user_info(session["user"])
            return ret
        return {"valid": False}

    return app


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5000)
