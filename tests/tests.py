
import requests
import psycopg2
import unittest

connection = psycopg2.connect(user="cs162_user",
                                  password="cs162_password",
                                  host="localhost",
                                  port="5432",
                                  database="cs162")
cursor = connection.cursor()

class TestCase(unittest.TestCase):
    def test_connection(self):
        response = requests.post('http://127.0.0.1:5000/add',data={'expression':'2+2'})
        assert response.status_code == 200

    def test_post(self):
        cursor.execute("SELECT * FROM Expression WHERE text='2+2' LIMIT 1")
        es = cursor.fetchall()
        assert es is not None
        assert es[0] is not None
        assert es[0][2] == 4

    def test_err(self):
        response = requests.post('http://127.0.0.1:5000/add', data={'expression':'2/0'})
        assert response.status_code == 500

    def test_db(self):
        cursor.execute("SELECT * FROM Expression ORDER BY id DESC LIMIT 1")
        es = cursor.fetchall()
        assert es is not None
        assert es[0] is not None
        assert es[0][1] == '2+2'

if __name__ == '__main__':
    unittest.main()
