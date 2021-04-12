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
        session = api.create_game()["session_id"]
        cursor = conn.execute(api.current_game.select().where(api.current_game.c.session_id == session))
        session_from_sql = cursor.fetchall()[0][0]
        conn.close()
        self.assertEqual(session, session_from_sql)
        ChessAPITestCase.remove_db_file()

    def test_resume_game(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        api = ChessAPI(db_url=db_url)
        session = api.create_game()["session_id"]
        resume_lst = api.resume_game()["resume_list"]
        exist = False
        for ele in resume_lst:
            if ele["session_id"] == session:
                exist = True
        self.assertTrue(exist)
        ChessAPITestCase.remove_db_file()

    def test_get_info(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        api = ChessAPI(db_url=db_url)
        session = api.create_game()["session_id"]
        init_info = api.get_info({"session_id": session})
        self.assertEqual(init_info["status"], "Continue")
        ChessAPITestCase.remove_db_file()

    def test_get_checked_moves(self):
        coord = Coordinate(1, 1).encode()
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        api = ChessAPI(db_url=db_url)

        session_id = api.create_game()["session_id"]
        checked = api.get_checked_moves({"session_id": session_id, "coordinate": coord})
        self.assertEqual(checked, {'moves': ['b3', 'b4']})
        ChessAPITestCase.remove_db_file()

    def test_update_game(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        api = ChessAPI(db_url=db_url)
        conn = api.engine.connect()
        src = Coordinate(1, 0)
        tar = Coordinate(3, 0)
        session_id = api.create_game()["session_id"]
        api.update_game({"session_id": session_id, "src": src.encode(), "tar": tar.encode(), "role": "Pawn"})
        ret = conn.execute(api.history.select().where(api.history.c.session_id == session_id))
        updated_src = ret.fetchall()[0][2]
        conn.close()
        self.assertEqual("(1,0)", updated_src)
        ChessAPITestCase.remove_db_file()
