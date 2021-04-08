from chess.chess_game import ChessGame
from chess.piece.coordinate import Coordinate
from chess_ai.simple_ai import SimpleAI
import random
import api.sql_execute as ex
import mysql.connector
import time
import datetime


class Driver:
    def __init__(self):
        self.sessions = {}
        self.my_db = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,  # change to your port
            user="root",
            password="zzj991203",  # change to your password
            auth_plugin='mysql_native_password'
        )

        self.my_cursor = self.my_db.cursor()
        ex.execute_script(self.my_cursor, r"SQ.sql")
        self.my_cursor.execute("SELECT * FROM current_game")
        r = self.my_cursor.fetchall()
        for ele in r:
            session_id = ele[0]
            fen = ele[1]
            game = ChessGame(fen)
            self.sessions[session_id] = game

        for session in self.sessions:
            sql = "SELECT * FROM history WHERE session=" + str(session) + " ORDER BY step"
            self.my_cursor.execute(sql)
            r = self.my_cursor.fetchall()
            self.sessions[session].init_history(r)
            self.my_db.commit()

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
        sql = "insert into current_game (session, start_time, last_update, fen, status) Values (%s,%s,%s,%s,%s)"
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        fen = game.get_fen()
        status = game.check_game_status()
        self.my_cursor.execute(sql, (session_id, timestamp, timestamp, fen, status))
        self.my_db.commit()
        return {"session_id": session_id}

    def resume_game(self) -> dict:
        self.my_cursor.execute("SELECT * FROM current_game")
        r = self.my_cursor.fetchall()
        lst = []
        for ele in r:
            session_id = ele[0]
            status = ele[2]
            start_time = ele[3]
            last_update = ele[4]
            if status == "Continue":
                lst.append({"session_id": session_id,
                            "start_time": start_time,
                            "last_update": last_update})
        self.my_db.commit()
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
        his = game.get_history()
        if his:
            sql = "INSERT INTO history (src, tar, src_piece, tar_piece, castling, " \
                  "en_passant, en_passant_target_notation, half_move, full_move, step, session) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s)"
            val = (his["src"], his["tar"], his["src_piece"], his["tar_piece"], his["castling"], his["en_passant"],
                   his["en_passant_target_notation"], his["half_move"], his["full_move"], his["step"], session_id)
            self.my_cursor.execute(sql, val)
            self.my_db.commit()

    def update_current(self, session_id):
        game = self.sessions[session_id]
        sql = "INSERT INTO current_game (fen, status, last_update, session) VALUES (%s, %s, %s, %s)" \
              "ON DUPLICATE KEY UPDATE" \
              " fen=VALUES(fen)," \
              "status=VALUES(status), last_update=VALUES(last_update)"
        status = game.check_game_status()
        fen = game.get_fen()
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.my_cursor.execute(sql, (fen, status, timestamp, session_id))
        self.my_db.commit()
