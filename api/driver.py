from chess.chess_game import ChessGame
from chess.piece.coordinate import Coordinate
from chess_ai.simple_ai import SimpleAI
import random
import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Boolean
import os


class Driver:
    def __init__(self):
        """
        Set up database using SQLite and put the db file under the same directory if db file does not exit.
        Connect to the database, fetch data and create dict sessions where key is session_id and value is
        chess game instance.
        """
        path = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        self.engine = create_engine(path, connect_args={'check_same_thread': False})
        meta = MetaData()

        self.current_game = Table(
            'game', meta,
            Column('session_id', Integer, primary_key=True),
            Column('fen', String),
            Column('status', String),
            Column('start_time', DateTime),
            Column('last_update', DateTime))

        self.history = Table(
            'history', meta,
            Column('session_id', Integer, primary_key=True),
            Column('step', Integer, primary_key=True),
            Column('src', String),
            Column('tar', String),
            Column('castling', Boolean),
            Column('en_passant', Boolean),
            Column('en_passant_target_notation', String),
            Column('half_move', Integer),
            Column('full_move', Integer))

        meta.create_all(self.engine)

        self.sessions = {}
        conn = self.engine.connect()
        sessions_info = conn.execute(self.current_game.select())
        for session in sessions_info:
            session_id = session["session_id"]
            fen = session["fen"]
            game = ChessGame(fen)
            self.sessions[session_id] = game

        for session_id in self.sessions:
            session_history = conn.execute(self.history.select().where(self.history.c.session_id == session_id).
                                           order_by(self.history.c.step))
            game = self.sessions[session_id]
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

    def create_game(self) -> dict:
        """
        Create a new chess game in put it in the dictionary, store the data in the database.
        :return: A dict where only has one key "session_id"
        """
        session_id = self.generate_unique_session_id()
        game = ChessGame()
        self.sessions[session_id] = game
        time = datetime.datetime.now()
        fen = game.get_fen()
        status = game.check_game_status()
        conn = self.engine.connect()
        conn.execute(self.current_game.insert(), {"session_id": session_id,
                                                  "status": status,
                                                  "fen": fen,
                                                  "start_time": time,
                                                  "last_update": time})
        conn.close()
        return {"session_id": session_id}

    def resume_game(self) -> dict:
        """
        Get all on-going unfinished sessions and their start time and last update time.
        :return: A dict which only has one key "resume-list" and value as a list of dict storing session id,
        start time, and last update
        """
        conn = self.engine.connect()
        ret = conn.execute(self.current_game.select())
        lst = []
        for ele in ret:
            session_id = ele[0]
            status = ele[2]
            start_time = ele[3]
            last_update = ele[4]
            if status == "Continue":
                lst.append({"session_id": session_id,
                            "start_time": start_time,
                            "last_update": last_update})
        conn.close()
        return {"resume_list": lst}

    def get_info(self, request: dict) -> dict:
        """
        Get the game info of a certain game.
        :param request: A dict with one key "session_id"
        :return: A dict with key "fen", "status", and "history"
        """
        session_id = request["session_id"]
        game = self.sessions[session_id]
        fen = game.get_fen()
        status = game.check_game_status()
        turn = game.get_turn()
        history = game.get_game_history()
        return {"fen": fen, "status": status, "turn": turn, "history": history}

    def update_game(self, request: dict) -> dict:
        """
        Update a certain game from source to target, and promotion role if occurred.
        :param request: A dict including session id, source coordinate, target coordinate, and promotion role.
        :return: A dict including info about update validation, whether being checked, game status and turn color.
        """
        session_id = request["session_id"]
        src = request["src"]
        tar = request["tar"]
        role = request["role"]
        src_coord = Coordinate.decode(src)
        tar_coord = Coordinate.decode(tar)
        game = self.sessions[session_id]

        valid = game.update(src_coord, tar_coord, role)
        if valid:
            self.update_history(session_id)
            self.update_current(session_id)
        is_being_checked = game.is_being_checked()
        status = game.check_game_status()
        turn = game.get_turn()
        # AI's turns
        if status == "Continue" and valid:
            ai = SimpleAI(game)
            src_row, src_col, tar_row, tar_col = ai.get_next_move()
            src = Coordinate(src_row, src_col)
            tar = Coordinate(tar_row, tar_col)
            valid = game.update(src, tar, "Queen")
            if valid:
                self.update_history(session_id)
                self.update_current(session_id)
            is_being_checked = game.is_being_checked()
            status = game.check_game_status()
            turn = game.get_turn()
        return {"valid": valid, "is_being_checked": is_being_checked, "game_status": status, "turn": turn}

    def get_checked_moves(self, request: dict) -> dict:
        """
        Get all valid moves which won't let you be checked in certain game for a coordinate.
        :param request: A dict including session id and piece coordinate
        :return: A dict which including all valid moves which won't let you be checked in certain game for a coordinate.
        """
        session_id = request["session_id"]
        coordinate = request["coordinate"]
        coordinate = Coordinate.decode(coordinate)
        game = self.sessions[session_id]
        return game.get_checked_moves(coordinate)

    def update_history(self, session_id: int) -> None:
        """
        Helper function which will update history table.
        :param session_id: Game session id which needs to update
        :return: None
        """
        game = self.sessions[session_id]
        game_history = game.get_history()
        if game_history:
            src = game_history["src"]
            tar = game_history["tar"]
            castling = game_history["castling"]
            en_passant = game_history["en_passant"]
            en_passant_target_notation = game_history["en_passant_target_notation"]
            half_move = game_history["half_move"]
            full_move = game_history["full_move"]
            step = game_history["step"]
            conn = self.engine.connect()
            conn.execute(self.history.insert(), {"session_id": session_id,
                                                 "src": src,
                                                 "tar": tar,
                                                 "castling": castling,
                                                 "en_passant": en_passant,
                                                 "en_passant_target_notation": en_passant_target_notation,
                                                 "half_move": half_move,
                                                 "full_move": full_move,
                                                 "step": step})
            conn.close()

    def update_current(self, session_id: int) -> None:
        """
        Helper function which will update game table.
        :param session_id: Game session id which needs to update
        :return: None
        """
        game = self.sessions[session_id]
        time = datetime.datetime.now()
        fen = game.get_fen()
        status = game.check_game_status()
        conn = self.engine.connect()
        conn.execute(self.current_game.update().where(self.current_game.c.session_id == session_id),
                     {"session_id": session_id,
                      "status": status,
                      "fen": fen,
                      "last_update": time})
        conn.close()
