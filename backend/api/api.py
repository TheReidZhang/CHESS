from api.chess_game import ChessGame
from api.simple_ai import SimpleAI
from api.piece.utility import Utility
from api.advanced_ai import AdvancedAI
import random
import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Float, and_, select


class ChessAPI:
    """
    Requests received from the flask server will be sent to ChessAPI and ChessAPI will call appropriate functions
    in ChessGame as well as maintain different game sessions.
    """
    def __init__(self, db_url="init"):
        """
        Set up database using db_url. Connect to the database, fetch data and create dict sessions where key is
        session_id and value is chess (game instance, username).
        :param db_url: if db_url is "init", the db_url is
            'postgresql+psycopg2://postgres:cmsc435team5@chess.czqnldjtsqip.us-east-2.rds.amazonaws.com:5432'
        Otherwise, db_url can be the value of the parameter passed in
        """
        if db_url == "init":
            db_url = 'postgresql+psycopg2://postgres:cmsc435team5@chess.czqnldjtsqip.us-east-2.rds.amazonaws.com:5432'
        self.engine = create_engine(db_url)
        meta = MetaData()

        self.current_game = Table(
            'game', meta,
            Column('username', String),
            Column('session_id', Integer, primary_key=True),
            Column('fen', String),
            Column('status', String),
            Column('mode', String),
            Column('start_time', DateTime),
            Column('last_update', DateTime))

        self.history = Table(
            'history', meta,
            Column('session_id', Integer, primary_key=True),
            Column('step', Integer, primary_key=True),
            Column('src', String),
            Column('tar', String),
            Column('fen', String))

        self.users = Table(
            'users', meta,
            Column('username', String, primary_key=True),
            Column('password', String),
            Column('total_hours', Float),
            Column('score', Integer)
        )

        meta.create_all(self.engine)

        self.sessions = {}
        self.modes = {}
        conn = self.engine.connect()
        sessions_info = conn.execute(self.current_game.select())
        for session in sessions_info:
            session_id = session["session_id"]
            fen = session["fen"]
            game = ChessGame(fen)
            self.sessions[session_id] = (game, session["username"])
            self.modes[session_id] = session["mode"]

        for session_id in self.sessions:
            session_history = conn.execute(self.history.select().where(self.history.c.session_id == session_id).
                                           order_by(self.history.c.step)).all()
            game = self.sessions[session_id][0]
            game.init_history(session_history)
        conn.close()

    def generate_unique_session_id(self) -> int:
        """
        Generate unique session id.
        :return: A unique session id
        """
        find_unique_session_id = False
        random_session_id = 0
        while find_unique_session_id is False:
            random_session_id = random.randint(1, 100000)
            find_unique_session_id = True
            for session_id in self.sessions:
                if session_id == random_session_id:
                    find_unique_session_id = False
                    break
        return random_session_id

    def create_game(self, username: str, mode: str) -> dict:
        """
        Create a new chess game in put it in the dictionary, store the data in the database.
        :param username: username of the user playing the game
        :param mode: the mode of the game. "easy": easy AI game; "advanced": advanced AI game; "pvp": player vs player
        :return: A dict where only has one key "session_id"
        """
        session_id = self.generate_unique_session_id()
        game = ChessGame()
        self.sessions[session_id] = (game, username)
        self.modes[session_id] = mode
        time = datetime.datetime.now()
        fen = game.get_fen()
        status = game.check_game_status()
        conn = self.engine.connect()
        conn.execute(self.current_game.insert(), {"username": username,
                                                  "session_id": session_id,
                                                  "status": status,
                                                  "fen": fen,
                                                  "mode": mode,
                                                  "start_time": time,
                                                  "last_update": time})
        conn.close()
        return {"session_id": session_id, "valid": True}

    def resume_game(self, username: str) -> dict:
        """
        Get all on-going unfinished sessions and their start time and last update time.
        :param username: username of the user playing the game
        :return: A dict which has key "resume_list" and value as a list of dict storing session id,
        start time, last update and mode
        """
        conn = self.engine.connect()
        ret = conn.execute(self.current_game.select().where(self.current_game.c.username == username).
                           order_by(self.current_game.c.last_update.desc()))
        lst = []
        for ele in ret:
            session_id = ele[1]
            status = ele[3]
            start_time = ele[5]
            last_update = ele[6]
            if status == "Continue":
                lst.append({"session_id": session_id,
                            "start_time": start_time,
                            "last_update": last_update,
                            "mode": self.modes[session_id]})
        conn.close()
        return {"resume_list": lst, "valid": True}

    def replay_game(self, username: str) -> dict:
        """
        Get all sessions that could be replayed
        :param username: username of the user playing the game
        :return: A dict which has key "replay_list" and value as a list of dict storing session id,
        start time, last update and mode
        """
        conn = self.engine.connect()
        ret = conn.execute(self.current_game.select().where(self.current_game.c.username == username).
                           order_by(self.current_game.c.last_update.desc()))
        lst = []
        for ele in ret:
            session_id = ele[1]
            start_time = ele[5]
            last_update = ele[6]

            lst.append({"session_id": session_id,
                        "start_time": start_time,
                        "last_update": last_update,
                        "mode": self.modes[session_id]})
        conn.close()
        return {"replay_list": lst, "valid": True}

    def get_info(self, request: dict) -> dict:
        """
        Get the game info of a certain game.
        :param request: A dict with one key "session_id" and "user"
        :return: A dict with key "fen", "status", "history", "turn" and "mode" and corresponding values
        """
        session_id = request["session_id"]
        username = request["user"]
        if session_id in self.sessions and self.sessions[session_id][1] == username:
            game = self.sessions[session_id][0]
            fen = game.get_fen()
            status = game.check_game_status()
            turn = game.get_turn()
            mode = self.modes[session_id]
            history = game.get_game_history()
            return {"fen": fen, "status": status, "turn": turn, "history": history, "valid": True, "mode": mode}
        return {"valid": False}

    def update_game(self, request: dict) -> dict:
        """
        Update a certain game from source to target, and promotion role if occurred.
        :param request: A dict including session id, source coordinate, target coordinate,current logged in user and
        promotion role.
        :return: A dict including info about update validation, whether being checked, game status and turn color.
        """
        session_id = request["session_id"]
        username = request["user"]
        if self.sessions[session_id][1] == username:
            src = request["src"]
            tar = request["tar"]
            role = request["role"]
            src_coord = Utility.decode(src)
            tar_coord = Utility.decode(tar)
            game = self.sessions[session_id][0]
            valid = game.update(src_coord, tar_coord, role)

            if valid:
                self.update_history(session_id)
                self.update_current(session_id)
            is_being_checked = game.is_being_checked()
            status = game.check_game_status()
            turn = game.get_turn()
            # AI's turns
            if status == "Continue" and valid and self.modes[session_id] != "pvp":
                if self.modes[session_id] == 'easy':
                    ai = SimpleAI(game)
                elif self.modes[session_id] == 'advanced':
                    ai = AdvancedAI(game)

                # noinspection PyUnboundLocalVariable
                src_row, src_col, tar_row, tar_col = ai.get_next_move()
                src = (src_row, src_col)
                tar = (tar_row, tar_col)
                valid = game.update(src, tar, "Queen")
                if valid:
                    self.update_history(session_id)
                    self.update_current(session_id)
                is_being_checked = game.is_being_checked()
                status = game.check_game_status()
                turn = game.get_turn()

            if status in ["WhiteLoss", "BlackLoss"] and valid and self.modes[session_id] != "pvp":
                self.update_score(session_id, username, status)

            return {"valid": valid, "is_being_checked": is_being_checked, "game_status": status, "turn": turn,
                    "validSession": True}

        return {"valid": False, "validSession": False}

    def get_checked_moves(self, request: dict, username: str) -> dict:
        """
        Get all valid moves which won't let you be checked in certain game for a coordinate.
        :param request: A dict including session id and piece coordinate
        :param username: logged in user
        :return: A dict which including all valid moves which won't let you be checked in certain game for a coordinate.
        """
        session_id = request["session_id"]
        if session_id in self.sessions and self.sessions[session_id][1] == username:
            coordinate = request["coordinate"]
            coordinate = Utility.decode(coordinate)
            game = self.sessions[session_id][0]
            ret = game.get_checked_moves(coordinate)
            ret["valid"] = True
            return ret
        return {"valid": False}

    def update_history(self, session_id: int) -> None:
        """
        Helper function which will update history table.
        :param session_id: Game session id which needs to update
        :return: None
        """
        game = self.sessions[session_id][0]
        game_history = game.get_history()
        if game_history:
            src = game_history["src"]
            tar = game_history["tar"]
            step = game_history["step"]
            fen = game_history["fen"]
            conn = self.engine.connect()
            conn.execute(self.history.insert(), {"session_id": session_id,
                                                 "src": src,
                                                 "tar": tar,
                                                 "step": step,
                                                 "fen": fen})
            conn.close()

    def update_current(self, session_id: int) -> None:
        """
        Helper function which will update game table.
        :param session_id: Game session id which needs to update
        :return: None
        """
        game = self.sessions[session_id][0]
        time = datetime.datetime.now()
        fen = game.get_fen()
        status = game.check_game_status()
        conn = self.engine.connect()
        conn.execute(self.current_game.update().where(self.current_game.c.session_id == session_id),
                     {"status": status,
                      "fen": fen,
                      "last_update": time})
        conn.close()

    def sign_up(self, request: dict) -> dict:
        """
        Sign a user up
        :param request: A dict with key "username" and "password"
        :return: A dict with key "valid" indicates whether successfully sign the user up
        """
        conn = self.engine.connect()
        if conn.execute(self.users.select().where(self.users.c.username == request["username"])).all():
            return {"valid": False}
        conn.execute(self.users.insert(), {"username": request["username"],
                                           "password": request["password"],
                                           "total_hours": 0})
        conn.close()
        return {"username": request["username"], "valid": True}

    def login(self, request: dict) -> dict:
        """
        For user to login their account
        :param request: A dict with key "username" and "password" of a registered user
        :return: A dict with key "valid" indicates whether successfully log the user in
        """
        conn = self.engine.connect()
        result = conn.execute(self.users.select().where(
            and_(self.users.c.username == request["username"],
                 self.users.c.password == request["password"]))).all()
        conn.close()
        if len(result) > 0:
            return {"valid": True}
        return {"valid": False}

    def get_user_info(self, username: str) -> dict:
        """
        Get information associated with the logged in user
        :param username: username of the user playing the game
        :return: A dict with key "username", "total_hours", "valid" and corresponding values
        """
        conn = self.engine.connect()
        result = conn.execute(self.users.select().where(self.users.c.username == username))
        user = result.all()
        conn.close()
        return {"username": user[0]["username"],
                "total_hours": user[0]["total_hours"],
                "score": user[0]["score"],
                "valid": True}

    def undo(self, username: str, session_id: int) -> dict:
        """
        Undo one step in the game, will delete history in both game() and database table
        :param username: username of the user playing the game
        :param session_id: session_id of the game
        :return: A dict with information of the game after undo
        """
        if session_id in self.sessions and self.sessions[session_id][1] == username:
            game = self.sessions[session_id][0]
            game.undo()
            conn = self.engine.connect()
            steps = conn.execute(self.history.select().where(self.history.c.session_id == session_id).
                                 order_by(self.history.c.step)).all()
            if len(steps) == 0:
                return {"valid": False, "validSession": True}
            conn.execute(self.history.delete().where(
                and_(self.history.c.session_id == session_id,
                     self.history.c.step == len(steps))))

            time = datetime.datetime.now()
            fen = game.get_fen()
            status = game.check_game_status()
            conn.execute(self.current_game.update().where(self.current_game.c.session_id == session_id),
                         {"status": status,
                          "fen": fen,
                          "last_update": time})
            conn.close()
            turn = game.get_turn()
            history = game.get_game_history()
            return {"fen": fen, "status": status, "turn": turn, "history": history, "valid": True, "validSession": True}
        return {"valid": False, "validSession": False}

    def replay(self, username: str, session_id: int, step: int) -> dict:
        """
        Get information of certain game after certain step
        :param username: username of the user playing the game
        :param session_id: session_id of the game
        :param step:
        :return: A dict with key "fen", "history" and "valid" with corresponding values
        """
        if session_id in self.sessions and self.sessions[session_id][1] == username:
            if step == 0:
                return {"fen": "start", "history": {}, "valid": True}
            conn = self.engine.connect()
            result = conn.execute(self.history.select().where(and_(self.history.c.session_id == session_id,
                                                                   self.history.c.step == step))).all()
            conn.close()
            if result:
                result = result[0]
                history = {"src": result["src"],
                           "tar": result["tar"]}
                return {"fen": result["fen"], "history": history, "valid": True, "validSession": True}
            else:
                return {"valid": False, "validSession": True}
        return {"valid": False, "validSession": False}

    def update_score(self, session_id: int, username: str, status: str) -> None:
        """
        Update user's score in PvE game.
        If a user win(lose to) easy AI player, the user will earn(lose) 5 points.
        If a user win(lose to) advanced AI player, the user will earn(lose) 10 points.
        If a user win(lose) a game within 10 moves, the user will earn(lose) extra 10 points.
        If a user win(lose) a game within 20 moves, the user will earn(lose) extra 5 points.
        If a game is a draw, the user will earn 0 points.
        :param session_id: session_id of the game
        :param username: username of the user playing the game
        :param status: status of the current game. "WhiteLoss" means the player who moves first is lost. Otherwise, the
        player who move second is lost.
        :return: None
        """
        current_score = self.get_user_info(username)["score"]
        delta = 0
        step = self.sessions[session_id][0].get_history()["step"]

        if self.modes[session_id] == 'easy':
            delta += 5
        if self.modes[session_id] == 'advanced':
            delta += 10
        if step <= 10:
            delta += 10
        elif step <= 20:
            delta += 5

        if status == "WhiteLoss":
            current_score -= delta
        else:
            current_score += delta
        conn = self.engine.connect()
        conn.execute(self.users.update().where(self.users.c.username == username), {"score": current_score})
        conn.close()

    def get_rankings(self) -> dict:
        """
        Get a ranking of users' score from database. Only include the first 5 users.
        An example of a ranking:
        {"rankings": [["UserA", 50], ["UserB", 40], ["UserC", 20], ["UserD", 20], ["UserE, 10]], "valid": True}
        :return: a dictionary with two keys. One is "rankings" and its value is a list of username and score.
        Another is "valid" and its value is True
        """
        conn = self.engine.connect()
        rankings = conn.execute(select(self.users.c.username, self.users.c.score)
                                .order_by(self.users.c.score.desc())).all()[:5]
        conn.close()
        ret = []
        for ranking in rankings:
            ret.append([ranking[0], ranking[1]])
        return {"rankings": ret, "valid": True}
