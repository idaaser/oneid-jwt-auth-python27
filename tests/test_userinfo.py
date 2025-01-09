import unittest

import oneid_auth


class TestUserinfo(unittest.TestCase):
    def test_empty_name(self):
        try:
            userinfo = oneid_auth.UserInfo("id", " ", username="test")
            self.assertIsNone(userinfo)
        except ValueError as err:
            self.assertIsNotNone(err)
            print(err)

    def test_empty_id(self):
        try:
            userinfo = oneid_auth.UserInfo(" ", "name", username="test")
            self.assertIsNone(userinfo)
        except ValueError as err:
            self.assertIsNotNone(err)
            print(err)

    def test_trimmed_id_and_name(self):
        try:
            userinfo = oneid_auth.UserInfo(" id ", "\nname\n", username="test")
            self.assertEqual("id", userinfo.user_id)
            self.assertEqual("name", userinfo.name)
        except ValueError as err:
            self.assertIsNone(err)

    def test_empty_username_and_mobile_and_email(self):
        try:
            user = oneid_auth.UserInfo("id", "name")
        except ValueError as err:
            self.assertIsNotNone(err)
            print(err)
