from flask_testing import TestCase
from app import create_app
import unittest

class TestClientUtils(TestCase):
    def create_app(self):
        return create_app()

    def test_assert_template_used_1(self):
        response = self.client.get("/list/")
        self.assertEqual(response.status_code, 200)

    def test_assert_template_used_2(self):
        response = self.client.get("/reg/signup/")
        self.assertEqual(response.status_code, 200)

    def test_assert_template_used_3(self):
        response = self.client.get("/reg/login/")
        self.assertEqual(response.status_code, 200)

    def test_assert_template_used_4(self):
        response = self.client.get("/user/mypage/")
        self.assertEqual(response.status_code, 302)

    def test_assert_template_used_5(self):
        response = self.client.get("/user/rec/")
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()