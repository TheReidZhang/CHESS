import unittest
from app import create_app
import os


class TestApp(unittest.TestCase):
    @staticmethod
    def remove_db_file() -> None:
        path_file = os.path.join(os.getcwd(), 'game.db')
        if os.path.exists(path_file):
            os.remove(path_file)

    def test_create_new_game(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        flask_app = create_app(db_url=db_url)
        client = flask_app.test_client()
        client.post("/signup", json={"username": "admin", "password": "admin"})
        client.post("/login", json={"username": "admin", "password": "admin"})
        session_id_1 = client.post("/chess/new", json={"mode": "easy", "user": "admin"}).get_json()["session_id"]
        session_id_2 = client.post("/chess/new", json={"mode": "pvp", "user": "admin"}).get_json()["session_id"]
        self.assertNotEqual(session_id_1, session_id_2)
        response = client.post("/chess/new", json={"mode": "pvp", "user": "admin"}).get_json()
        self.assertEqual(len(response), 2)
        TestApp.remove_db_file()

    def test_update_game(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        flask_app = create_app(db_url=db_url)
        client = flask_app.test_client()
        client.post("/signup", json={"username": "admin", "password": "admin"})
        client.post("/login", json={"username": "admin", "password": "admin"})
        session_id_1 = client.post("/chess/new", json={"mode": "easy", "user": "admin"}).get_json()["session_id"]
        response = client.post("/chess/update", json={"session_id": session_id_1, "src": "f2", "tar": "f4",
                                                      "role": "Queen", "user": "admin"}).get_json()

        self.assertEqual(len(response), 5)
        self.assertEqual("game_status" in response, True)
        self.assertEqual("is_being_checked" in response, True)
        self.assertEqual("turn" in response, True)
        self.assertEqual("valid" in response, True)
        self.assertEqual(response["valid"], True)
        response = client.post("/chess/update", json={"session_id": session_id_1, "src": "f2", "tar": "f4",
                                                      "role": "Queen", "user": "admin"}).get_json()
        self.assertEqual(response["valid"], False)
        TestApp.remove_db_file()

    def test_resume_game(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        flask_app = create_app(db_url=db_url)
        client = flask_app.test_client()
        client.post("/signup", json={"username": "admin", "password": "admin"})
        client.post("/login", json={"username": "admin", "password": "admin"})
        client.post("/chess/new", json={"mode": "easy", "user": "admin"})
        client.post("/chess/new", json={"mode": "easy", "user": "admin"})
        client.post("/chess/new", json={"mode": "pvp", "user": "admin"})
        lists = client.post("/resume", json={"user": "admin"}).get_json()["resume_list"]
        self.assertEqual(len(lists), 3)
        self.assertEqual(len(lists[0]), 4)
        TestApp.remove_db_file()

    def test_get_chess_game_info(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        flask_app = create_app(db_url=db_url)
        client = flask_app.test_client()
        client.post("/signup", json={"username": "admin", "password": "admin"})
        client.post("/login", json={"username": "admin", "password": "admin"})
        session_id = client.post("/chess/new", json={"mode": "easy", "user": "admin"}).get_json()["session_id"]
        response = client.post("/chess/info", json={"session_id": session_id, "user": "admin"}).get_json()
        self.assertEqual(len(response), 6)
        self.assertEqual("fen" in response, True)
        TestApp.remove_db_file()

    def test_get_checked_moves_api(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        flask_app = create_app(db_url=db_url)
        client = flask_app.test_client()
        client.post("/signup", json={"username": "admin", "password": "admin"})
        client.post("/login", json={"username": "admin", "password": "admin"})
        session_id = client.post("/chess/new", json={"mode": "easy", "user": "admin"}).get_json()["session_id"]
        url = "/chess/"+str(session_id)+"/f2"
        response = client.post(url, json={"user": "admin"}).get_json()
        self.assertEqual(len(response), 2)
        self.assertEqual(response["moves"], ["f3", "f4"])
        TestApp.remove_db_file()

    def test_get_user_info(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        flask_app = create_app(db_url=db_url)
        client = flask_app.test_client()
        client.post("/signup", json={"username": "admin", "password": "admin"})
        client.post("/login", json={"username": "admin", "password": "admin"})
        response = client.post("/user", json={"user": "admin"}).get_json()
        self.assertEqual(response["total_hours"], 0)
        self.assertEqual(response["valid"], True)
        TestApp.remove_db_file()

    def test_api_refuses_request_if_user_does_not_match_with_session(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        flask_app = create_app(db_url=db_url)
        client = flask_app.test_client()
        result = client.post("/undo", json={"user": "admin", "session_id": 1}).get_json()
        self.assertEqual(result["valid"], False)

        result = client.post("/replay", json={"user": "admin", "session_id": 1, "step": 0}).get_json()
        self.assertEqual(result["valid"], False)

        result = client.post("/chess/1/a4", json={"user": "admin"}).get_json()
        self.assertEqual(result["valid"], False)

        result = client.post("/chess/info", json={"user": "admin", "session_id": 1}).get_json()
        self.assertEqual(result["valid"], False)
        TestApp.remove_db_file()
