import unittest

import oneid_auth

rsa_private_key = """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDPwlvSsvsxHHKkRFeMvrBPvfGio2TLEHBCsoZ34KBmpjrJHLpcvVQ7K3SX3bRfplWH2qPs5EI9zt+LQ6Jlr1rMj7Nh/ZlX698rShdBtsfLX5rlFyFlJrQPOLnX1d9lD1i2FWFrCYe/CwHqx8+Y25KIgci1lyU7CgQXD944+Hkqv1pmYrqZJvl12fTR3gx2fiC/iAsFEBTpdSWavleE6i3vKPdfsp+Ojs9bHcv5btkPIBLGVMV2oRGjHxZdDwRQSaHo9DwnSSv6p+S+xcdALHRLMUNonQ1R9hDFRLRt7/G8fB+4+OrA4I5hmYZWOV9zi8CJ/S57miPLLHcrMEa8fWSnAgMBAAECggEACxTl4EY1tHfnptq9BL/Yba3G/r19DyvFoSPJR7ROj0sckETyV9ICyn6AjefVytL3dZ30PRrWbFo60usnoAmLa/qE6fF58BZKZWe399mvrH8L/F47JMcSDEx39TWY4INstZb3BvDk3GF87QX9YmeL2Ft71jEasPHRfV1rpVmeNOkUEaV1hLYsf3l9AZ7Im8hN+2Aarp0m7oMdOY3QVZ5bQ4qlbYsjPT3aCaZIpHoUCmUrKuyqNQDpXqXYZ6imBgaU9SzYHROJ+etAxyef8d/DbshrZ77OkI+xO1Nq8OClqfOBLeKnT4tr1S0t31mBWE1fFf1590UKmovZ2mm+zrXD8QKBgQDpU0g5fUcWBdsOeL+I6VZwB+iQcRIid0XiKI1bB4mdS+cA3JNFszy5y8jHY+2amVZ7Wvorl3ZICaGMLJncdChz4e2yJ5icAmLpJ7RVNnFm5oqM+EcXW5mLS99d7GlauY0ORUdDytdfv0aWqFwkltMNV7Z1VY4C+O0X2wsPwIK2DwKBgQDj8wmTSF/P4q4vhl5VFHK5HR5KaTxZ09myd82Xl1MTADjV3E3MBkDUWGhnRYFmwLCmnuXuMBTdA6nLHEpDnWW6Q1Xtbmt5k1x9D8B9nwbA2Tmz9hGvN1l8MlYPt2Hu+E17Je6kMCdy5Iz1QUevXc3cR0DLZwFGRhgXAyIS8cg/6QKBgQCuswrK8MA+/xdrmIFg08VCkMlTDTZU1BVhJpfgZp5lRiWqgX1LnM6FFs44bNvE+7bDGfVimj+X5I4u1F5HsDlxuuIsmHUtqqPAi1f8zYzPTSLENkmUdaNbpu2R96dSpMe2vayEV+Y27JK/z0NeqgdQYDJfXDW+h/+N8xYvLycvhQKBgDezFW3ly3OywjlergJAIuBU2yf3mwWgHJvdZmFaWrRT449ua5wlEwZQLALAGySOhRvRzAFtwktXL9Avs33eIhNnjMGdr6lfdsQgazrG9xF8gvsUb7HO5pDQg/MHLmkER3qGBFAebCVI76CmOOwDEeB3kL+jBc60JgLJgzP53KKxAoGBANKZ9xIWiSyRICUIHwpWClizXj9dyXaHOl6INqd/Jj+1dqdizI7YoVufm6vDP0vKf467HKLwLm5mDlZr3j+j/Y/WkbZqluT8onPx4F7m5f8dJUu/OJtGBc1+OnfzyFt5xSAD0Q6NDAxDdKuKCV36znRdNbZu/WiICncDQIjaNCeQ
-----END PRIVATE KEY-----"""

headless_key = "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDPwlvSsvsxHHKkRFeMvrBPvfGio2TLEHBCsoZ34KBmpjrJHLpcvVQ7K3SX3bRfplWH2qPs5EI9zt+LQ6Jlr1rMj7Nh/ZlX698rShdBtsfLX5rlFyFlJrQPOLnX1d9lD1i2FWFrCYe/CwHqx8+Y25KIgci1lyU7CgQXD944+Hkqv1pmYrqZJvl12fTR3gx2fiC/iAsFEBTpdSWavleE6i3vKPdfsp+Ojs9bHcv5btkPIBLGVMV2oRGjHxZdDwRQSaHo9DwnSSv6p+S+xcdALHRLMUNonQ1R9hDFRLRt7/G8fB+4+OrA4I5hmYZWOV9zi8CJ/S57miPLLHcrMEa8fWSnAgMBAAECggEACxTl4EY1tHfnptq9BL/Yba3G/r19DyvFoSPJR7ROj0sckETyV9ICyn6AjefVytL3dZ30PRrWbFo60usnoAmLa/qE6fF58BZKZWe399mvrH8L/F47JMcSDEx39TWY4INstZb3BvDk3GF87QX9YmeL2Ft71jEasPHRfV1rpVmeNOkUEaV1hLYsf3l9AZ7Im8hN+2Aarp0m7oMdOY3QVZ5bQ4qlbYsjPT3aCaZIpHoUCmUrKuyqNQDpXqXYZ6imBgaU9SzYHROJ+etAxyef8d/DbshrZ77OkI+xO1Nq8OClqfOBLeKnT4tr1S0t31mBWE1fFf1590UKmovZ2mm+zrXD8QKBgQDpU0g5fUcWBdsOeL+I6VZwB+iQcRIid0XiKI1bB4mdS+cA3JNFszy5y8jHY+2amVZ7Wvorl3ZICaGMLJncdChz4e2yJ5icAmLpJ7RVNnFm5oqM+EcXW5mLS99d7GlauY0ORUdDytdfv0aWqFwkltMNV7Z1VY4C+O0X2wsPwIK2DwKBgQDj8wmTSF/P4q4vhl5VFHK5HR5KaTxZ09myd82Xl1MTADjV3E3MBkDUWGhnRYFmwLCmnuXuMBTdA6nLHEpDnWW6Q1Xtbmt5k1x9D8B9nwbA2Tmz9hGvN1l8MlYPt2Hu+E17Je6kMCdy5Iz1QUevXc3cR0DLZwFGRhgXAyIS8cg/6QKBgQCuswrK8MA+/xdrmIFg08VCkMlTDTZU1BVhJpfgZp5lRiWqgX1LnM6FFs44bNvE+7bDGfVimj+X5I4u1F5HsDlxuuIsmHUtqqPAi1f8zYzPTSLENkmUdaNbpu2R96dSpMe2vayEV+Y27JK/z0NeqgdQYDJfXDW+h/+N8xYvLycvhQKBgDezFW3ly3OywjlergJAIuBU2yf3mwWgHJvdZmFaWrRT449ua5wlEwZQLALAGySOhRvRzAFtwktXL9Avs33eIhNnjMGdr6lfdsQgazrG9xF8gvsUb7HO5pDQg/MHLmkER3qGBFAebCVI76CmOOwDEeB3kL+jBc60JgLJgzP53KKxAoGBANKZ9xIWiSyRICUIHwpWClizXj9dyXaHOl6INqd/Jj+1dqdizI7YoVufm6vDP0vKf467HKLwLm5mDlZr3j+j/Y/WkbZqluT8onPx4F7m5f8dJUu/OJtGBc1+OnfzyFt5xSAD0Q6NDAxDdKuKCV36znRdNbZu/WiICncDQIjaNCeQ"

issuer = "http://www.example.com"
login_url = "https://oauth2.ci-731.account.tencentcs.com/v1/sso/jwtp/1102878596482998272/1151383032381308928/kit/{app_type}"


class TestJWS(unittest.TestCase):
    def setUp(self):
        self.signer = oneid_auth.Signer(rsa_private_key, issuer, login_url)
        self.signer_from_key_file = oneid_auth.Signer.new_signer_from_key_file("./private.key", issuer, login_url)
        self.signer_with_token_key = oneid_auth.Signer(rsa_private_key, issuer, login_url, token_key="jwt")
        self.signer_with_lifetime = oneid_auth.Signer(rsa_private_key, issuer, login_url, lifetime=200)
        self.signer_with_headless_key = oneid_auth.Signer(headless_key, issuer, login_url, lifetime=200)

    def test_smaller_token_lifetime(self):
        try:
            signer = oneid_auth.Signer(rsa_private_key, issuer, login_url, lifetime=0)
        except ValueError as err:
            self.assertIsNotNone(err)
            print(err)

    def test_greater_token_lifetime(self):
        try:
            signer = oneid_auth.Signer(rsa_private_key, issuer, login_url, lifetime=301)
        except ValueError as err:
            self.assertIsNotNone(err)
            print(err)

    def test_invalid_key(self):
        try:
            signer = oneid_auth.Signer("", issuer, login_url)
        except Exception as e:
            self.assertIsNotNone(e)
            print(e)

    def test_generate_token(self):
        custom_attr = {
            "employee_number": "001"
        }
        try:
            user_info = oneid_auth.UserInfo("user_id1", "test1", username="test1", custom_attributes=custom_attr)
            token = self.signer.sign(user_info)
            self.assertIsNot(token, "")
            print(token)
        except Exception as e:
            self.assertIsNone(e)

    def test_generate_token_with_specific_lifetime(self):
        try:
            user = oneid_auth.UserInfo("user_id1", "test1", username="test1")
            token = self.signer_with_lifetime.sign(user)
            self.assertIsNot(token, "")
            print(token)
        except Exception as e:
            self.assertIsNone(e)

    def test_generate_token_from_key_file(self):
        try:
            user_info = oneid_auth.UserInfo("user_id1", "test1", username="test1")
            token = self.signer_from_key_file.sign(user_info)
            self.assertIsNot(token, "")
            print(token)
        except Exception as e:
            self.assertIsNone(e)

    def test_generate_token_with_headless_key(self):
        try:
            user_info = oneid_auth.UserInfo("user_id1", "test1", username="test1")
            token = self.signer_with_headless_key.sign(user_info)
            self.assertIsNot(token, "")
            print(token)
        except Exception as e:
            self.assertIsNone(e)

    def test_generate_url(self):
        params = {
            "meeting_common": "https://meeting.tencent.com/"
        }
        try:
            user_info = oneid_auth.UserInfo("user_id1", "test1", username="test1")
            url = self.signer.generate_login_url(user_info, oneid_auth.App_Tencent_Meeting, params=params)
            self.assertIsNot(url, "")
            print(url)
        except Exception as e:
            self.assertIsNone(e)

    def test_generate_url_with_token_key(self):
        params = {
            "meeting_common": "https://meeting.tencent.com/"
        }
        try:
            user_info = oneid_auth.UserInfo("user_id1", "test1", username="test1")
            url = self.signer_with_token_key.generate_login_url(user_info, oneid_auth.App_Tencent_Meeting, params=params)
            self.assertIsNot(url, "")
            print(url)
        except Exception as e:
            self.assertIsNone(e)

if __name__ == '__main__':
    unittest.main()
