import unittest
from api.driver import Driver
from chess.piece.coordinate import Coordinate

class DriverTestCase(unittest.TestCase):
    def test_unique_session(self):
        driver = Driver()
        session_set = set()
        for i in range(1000):
            session_id = driver.generate_unique_session_id()
            session_set.add(session_id)
            driver.sessions[session_id] = None
        print(len(session_set))
        self.assertEqual(len(session_set), 1000)

    def test_create_game(self):
        driver = Driver()
        conn = driver.conn
        session = driver.create_game()["session_id"]
        cursor = conn.execute(driver.current_game.select().where(driver.current_game.c.session_id == session))
        session_from_sql = cursor.fetchall()[0][0]
        self.assertEqual(session, session_from_sql)

    def test_resume_game(self):
        driver = Driver()
        session = driver.create_game()["session_id"]
        resume_lst = driver.resume_game()["resume_list"]
        exist = False
        for ele in resume_lst:
            if ele["session_id"] == session:
                exist = True
        self.assertTrue(exist)

    def test_get_info(self):
        driver = Driver()
        session = driver.create_game()["session_id"]
        init_info = driver.get_info({"session_id": session})
        self.assertEqual(init_info["status"], "Continue")

    def test_get_checked_moves(self):
        coord = Coordinate(1,1).encode()
        driver = Driver()

        session_id = driver.create_game()["session_id"]
        checked = driver.get_checked_moves({"session_id": session_id, "coordinate": coord})
        self.assertEqual(checked, {'moves': ['b3', 'b4']})

    def test_update_game(self):
        driver = Driver()
        src = Coordinate(1, 0)
        tar = Coordinate(3, 0)
        session_id = driver.create_game()["session_id"]
        driver.update_game({"session_id": session_id,"src": src.encode(), "tar": tar.encode(), "role": "Pawn" })
        conn = driver.conn
        ret = conn.execute(driver.history.select().where(driver.history.c.session_id == session_id))
        updated_src = ret.fetchall()[0][2]
        self.assertEqual("(1,0)", updated_src)

