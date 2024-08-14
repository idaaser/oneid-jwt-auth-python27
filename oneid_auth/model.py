# coding=utf-8
import time

import constant


class UserInfo:
    def __init__(self, user_id, name=None, preferred_username=None, email=None, mobile=None, extension=None):
        self.user_id = user_id
        self.name = name
        self.preferred_username = preferred_username
        self.email = email
        self.mobile = mobile
        self.extension = extension

    def validate(self):
        if check_invalid_string(self.user_id):
            raise ValueError("user_id must be required")

        if (check_invalid_string(self.preferred_username)
                and check_invalid_string(self.email)
                and check_invalid_string(self.mobile)):
            raise ValueError("preferred_user_name/email/mobile must not all empty")

    def as_claims(self):
        claims = {}
        if self.extension is not None:
            claims.update(self.extension)
        claims[constant.ATTRIBUTE_SUBJECT] = self.user_id
        claims[constant.ATTRIBUTE_NAME] = self.name
        claims[constant.ATTRIBUTE_PREFERRED_USERNAME] = self.preferred_username
        claims[constant.ATTRIBUTE_EMAIL] = self.email
        claims[constant.ATTRIBUTE_PHONE_NUMBER] = self.mobile
        return claims


class JwtConfig:
    def __init__(self, private_key, issuer, login_url=None, token_param=constant.DEFAULT_TOKEN_PARAM):
        self.private_key = private_key
        self.issuer = issuer
        self.login_url = login_url
        self.token_param = token_param

    def validate(self):
        if check_invalid_string(self.private_key):
            raise ValueError("invalid private_key")
        if check_invalid_string(self.issuer):
            raise ValueError("invalid issuer")

    def as_claims(self):
        cur_time = time.time()
        return {
            constant.ATTRIBUTE_ISSUER: self.issuer,
            constant.ATTRIBUTE_IAT_TIME: cur_time,
            constant.ATTRIBUTE_EXPIRE_TIME: cur_time + constant.TOKEN_EXPIRE_SECOND
        }


# 校验是非法的字符串
def check_invalid_string(value):
    if not isinstance(value, basestring) or not bool(value.strip()):
        return True
    return False
