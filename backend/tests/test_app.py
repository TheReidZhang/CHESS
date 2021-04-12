import unittest
from app import create_app
import os


class TestApp(unittest.TestCase):
    @staticmethod
    def remove_db_file():
        path_file = os.path.join(os.getcwd(), 'game.db')
        if os.path.exists(path_file):
            os.remove(path_file)

    def test_create_new_game(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        flask_app = create_app(db_url=db_url)
        client = flask_app.test_client()
        session_id_1 = client.post("/chess/new").get_json()["session_id"]
        session_id_2 = client.post("/chess/new").get_json()["session_id"]
        self.assertNotEqual(session_id_1, session_id_2)
        response = client.post("/chess/new").get_json()
        self.assertEqual(len(response), 1)
        TestApp.remove_db_file()

    def test_update_game(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        flask_app = create_app(db_url=db_url)
        client = flask_app.test_client()
        session_id_1 = client.post("/chess/new").get_json()["session_id"]
        response = client.post("/chess/update", json={"session_id": session_id_1, "src": "f2", "tar": "f4",
                                                      "role": "Queen"}).get_json()
        self.assertEqual(len(response), 4)
        self.assertEqual("game_status" in response, True)
        self.assertEqual("is_being_checked" in response, True)
        self.assertEqual("turn" in response, True)
        self.assertEqual("valid" in response, True)
        self.assertEqual(response["valid"], True)
        response = client.post("/chess/update", json={"session_id": session_id_1, "src": "f2", "tar": "f4",
                                                      "role": "Queen"}).get_json()
        self.assertEqual(response["valid"], False)
        TestApp.remove_db_file()

    def test_resume_game(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        flask_app = create_app(db_url=db_url)
        client = flask_app.test_client()
        client.post("/chess/new").get_json()["session_id"]
        client.post("/chess/new").get_json()["session_id"]
        client.post("/chess/new").get_json()["session_id"]
        lists = client.get("/resume").get_json()["resume_list"]
        self.assertEqual(len(lists), 3)
        self.assertEqual(len(lists[0]), 3)
        TestApp.remove_db_file()

    def test_get_chess_game_info(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        flask_app = create_app(db_url=db_url)
        client = flask_app.test_client()
        session_id = client.post("/chess/new").get_json()["session_id"]
        response = client.post("/chess/info", json={"session_id": session_id}).get_json()
        self.assertEqual(len(response), 4)
        self.assertEqual("fen" in response, True)
        TestApp.remove_db_file()

    def test_get_checked_moves_api(self):
        db_url = os.path.join('sqlite:///' + os.getcwd(), 'game.db')
        flask_app = create_app(db_url=db_url)
        client = flask_app.test_client()
        session_id = client.post("/chess/new").get_json()["session_id"]
        url = "/chess/"+str(session_id)+"/f2"
        response = client.get(url).get_json()
        self.assertEqual(len(response), 1)
        self.assertEqual(response["moves"], ["f3", "f4"])
        TestApp.remove_db_file()
