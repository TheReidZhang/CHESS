from chess.chess_game import ChessGame
from chess.piece.coordinate import Coordinate
from chess_ai.simple_ai import SimpleAI
import random
import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Boolean
import os


class Driver:
    def __init__(self):
        path = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        engine = create_engine(path, connect_args={'check_same_thread': False})
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

        meta.create_all(engine)
        self.conn = engine.connect()

        self.sessions = {}
        sessions_info = self.conn.execute(self.current_game.select())
        for session in sessions_info:
            session_id = session["session_id"]
            fen = session["fen"]
            game = ChessGame(fen)
            self.sessions[session_id] = game

        for session_id in self.sessions:
            session_history = self.conn.execute(self.history.select().where(self.history.c.session_id == session_id).
                                                order_by(self.history.c.step))
            game = self.sessions[session_id]
            game.init_history(session_history)

    def generate_unique_session_id(self) -> int:
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

    def create_game(self):
        session_id = self.generate_unique_session_id()
        game = ChessGame()
        self.sessions[session_id] = game
        time = datetime.datetime.now()
        fen = game.get_fen()
        status = game.check_game_status()
        self.conn.execute(self.current_game.insert(), {"session_id": session_id,
                                                       "status": status,
                                                       "fen": fen,
                                                       "start_time": time,
                                                       "last_update": time})
        return {"session_id": session_id}

    def resume_game(self) -> dict:
        ret = self.conn.execute(self.current_game.select())
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
        return {"resume_list": lst}

    def get_info(self, request: dict) -> dict:
        session_id = request["session_id"]
        game = self.sessions[session_id]
        fen = game.get_fen()
        status = game.check_game_status()
        turn = game.get_turn()
        history = game.get_game_history()
        return {"fen": fen, "status": status, "turn": turn, "history": history}

    def update_game(self, request: dict):
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
            # print(str(src_row) + " " + str(src_col) + " " + str(tar_row) + " " + str(tar_col))
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
        session_id = request["session_id"]
        coordinate = request["coordinate"]
        coordinate = Coordinate.decode(coordinate)
        game = self.sessions[session_id]
        return game.get_checked_moves(coordinate)

    def update_history(self, session_id):
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

            self.conn.execute(self.history.insert(), {"session_id": session_id,
                                                      "src": src,
                                                      "tar": tar,
                                                      "castling": castling,
                                                      "en_passant": en_passant,
                                                      "en_passant_target_notation": en_passant_target_notation,
                                                      "half_move": half_move,
                                                      "full_move": full_move,
                                                      "step": step})

    def update_current(self, session_id):
        game = self.sessions[session_id]
        time = datetime.datetime.now()
        fen = game.get_fen()
        status = game.check_game_status()
        self.conn.execute(self.current_game.update().where(self.current_game.c.session_id == session_id),
                          {"session_id": session_id,
                           "status": status,
                           "fen": fen,
                           "last_update": time})
