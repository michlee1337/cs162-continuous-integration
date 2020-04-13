import requests
import unittest
from sqlalchemy import create_engine

class TestCase(unittest.TestCase):
    def test_connection(self):
        r = requests.post('http://127.0.0.1:5000/add',data={'expression':'2+2'})
        self.assertEqual(r.status_code, 200)

    def test_post(self):
        r = requests.post('http://127.0.0.1:5000/add', data={'expression':'5+5'})
        engine = create_engine('postgresql://cs162_user:cs162_password@127.0.0.1:5432/cs162', echo = True)

        with engine.connect() as con:
            rs = con.execute("SELECT * FROM Expression WHERE text = '5+5'")
            rows = rs.fetchall()

        self.assertNotEqual(len(rows), 0)

    def test_err(self):
        r = requests.post('http://127.0.0.1:5000/add', data={'expression':'2/0'})
        self.assertNotEqual(r.status_code, 200)

    def test_db(self):
        engine = create_engine('postgresql://cs162_user:cs162_password@127.0.0.1:5432/cs162', echo = True)

        with engine.connect() as con:
            rs = con.execute("SELECT * FROM Expression WHERE text = '5+5'")
            rows = rs.fetchall()

        lastId = rows[0][0]
        with engine.connect() as con:
            rs2 = con.execute("SELECT * FROM Expression WHERE id > lastId")
            rows2 = rs.fetchall()
        self.assertEqual(len(rows2), 0)

if __name__ == '__main__':
    unittest.main()
