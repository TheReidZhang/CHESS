import unittest
from api.piece.coordinate import Coordinate
from api.api import ChessAPI
import os


class ChessAPITestCase(unittest.TestCase):
    @staticmethod
    def remove_db_file() -> None:
        path_file = os.path.join(os.getcwd(), 'game.db')
        if os.path.exists(path_file):
            os.remove(path_file)

    def test_unique_session(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        api = ChessAPI(db_url=db_url)
        session_set = set()
        for i in range(1000):
            session_id = api.generate_unique_session_id()
            session_set.add(session_id)
            api.sessions[session_id] = None

        self.assertEqual(len(session_set), 1000)
        ChessAPITestCase.remove_db_file()

    def test_create_game(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        api = ChessAPI(db_url=db_url)
        conn = api.engine.connect()
        session = api.create_game("hu4396", "pvp")["session_id"]
        cursor = conn.execute(api.current_game.select().where(api.current_game.c.session_id == session))
        session_from_sql = cursor.fetchall()[0][1]
        conn.close()
        self.assertEqual(session, session_from_sql)
        ChessAPITestCase.remove_db_file()

    def test_resume_game(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        api = ChessAPI(db_url=db_url)
        session = api.create_game("hu4396", "pvp")["session_id"]
        resume_lst = api.resume_game("hu4396")["resume_list"]
        exist = False
        for ele in resume_lst:
            if ele["session_id"] == session:
                exist = True
        self.assertTrue(exist)
        ChessAPITestCase.remove_db_file()

    def test_get_info(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        api = ChessAPI(db_url=db_url)
        session = api.create_game("hu4396", "pvp")["session_id"]
        init_info = api.get_info({"session_id": session}, "hu4396")
        self.assertEqual(init_info["status"], "Continue")
        ChessAPITestCase.remove_db_file()

    def test_get_checked_moves(self):
        coord = Coordinate(1, 1).encode()
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        api = ChessAPI(db_url=db_url)

        session_id = api.create_game("hu4396", "pvp")["session_id"]
        checked = api.get_checked_moves({"session_id": session_id, "coordinate": coord}, "hu4396")
        self.assertEqual(checked, {'moves': ['b3', 'b4'], 'valid': True})
        ChessAPITestCase.remove_db_file()

    def test_update_game(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        api = ChessAPI(db_url=db_url)
        conn = api.engine.connect()
        src = Coordinate(1, 0)
        tar = Coordinate(3, 0)
        session_id = api.create_game("hu4396", "pvp")["session_id"]
        api.update_game({"session_id": session_id, "src": src.encode(), "tar": tar.encode(), "role": "Pawn"}, "hu4396")
        ret = conn.execute(api.history.select().where(api.history.c.session_id == session_id))
        updated_src = ret.fetchall()[0]["src"]
        conn.close()
        self.assertEqual("a2", updated_src)
        ChessAPITestCase.remove_db_file()

    def test_invalid_replay(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        api = ChessAPI(db_url=db_url)
        session_id = api.create_game("hu4396", "pvp")["session_id"]
        ret = api.replay("hu", session_id, 0)
        self.assertEqual(ret, {"valid": False})

        ret = api.replay("hu", session_id, -10)
        self.assertEqual(ret, {"valid": False})

        ret = api.replay("hu", session_id, 1000)
        self.assertEqual(ret, {"valid": False})
        ChessAPITestCase.remove_db_file()

    def test_undo_takes_back_a_step(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        api = ChessAPI(db_url=db_url)
        session_id = api.create_game("hu4396", "pvp")["session_id"]
        ret = api.undo("hu4396", session_id)
        self.assertEqual(ret["fen"], 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        api.update_game({"session_id": session_id, "src": "a2", "tar": "a4", "role": "Pawn"}, "hu4396")
        ret = api.undo("hu4396", session_id)
        self.assertEqual(ret["fen"], 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        ChessAPITestCase.remove_db_file()

    def test_get_user_info(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        api = ChessAPI(db_url=db_url)
        api.sign_up({"username": "admin", "password": "admin"})
        ret = api.get_user_info("admin")
        self.assertEqual(ret["valid"], True)
        self.assertEqual(ret["username"], "admin")

    def test_refuses_to_execute_invalid_request(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        api = ChessAPI(db_url=db_url)
        session_id = api.create_game("hu4396", "pvp")["session_id"]
        ret = api.undo("admin", session_id)
        self.assertEqual(ret["valid"], False)

        ret = api.login({"username": "1", "password": "1"})
        self.assertEqual(ret["valid"], False)

        ret = api.update_game({"session_id": session_id}, "admin")
        self.assertEqual(ret["valid"], False)