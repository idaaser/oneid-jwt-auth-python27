# coding=utf-8
import jwt, uuid

import oneid_auth.constant
from . import constant
from datetime import datetime
from calendar import timegm
from urlparse import urlparse, parse_qsl, urlunparse
from urllib import urlencode


class UserInfo:
    def __init__(self, user_id, name, username=None, email=None, mobile=None, custom_attributes=None):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.email = email
        self.mobile = mobile
        self.custom_attributes = custom_attributes

    def validate(self):
        if check_invalid_string(self.user_id):
            raise ValueError("user_id must be required")

        if check_invalid_string(self.name):
            raise ValueError("name must be required")

        if (check_invalid_string(self.username)
                and check_invalid_string(self.email)
                and check_invalid_string(self.mobile)):
            raise ValueError("preferred_user_name/email/mobile must not all empty")

    def as_claims(self):
        claims = {}
        if self.custom_attributes is not None:
            claims.update(self.custom_attributes)
        claims[constant.CLAIM_SUBJECT] = self.user_id
        claims[constant.CLAIM_NAME] = self.name
        if self.username is not None and self.username != "":
            claims[constant.CLAIM_PREFERRED_USERNAME] = self.username
        if self.email is not None and self.email != "":
            claims[constant.CLAIM_EMAIL] = self.email
        if self.mobile is not None and self.mobile != "":
            claims[constant.CLAIM_PHONE_NUMBER] = self.mobile
        return claims


class Signer:
    def __init__(self, private_key, issuer, lifetime=constant.TOKEN_EXPIRE_SECOND, login_url=None,
                 token_key=constant.DEFAULT_TOKEN_PARAM):
        self.private_key = private_key
        self.issuer = issuer
        self.login_url = login_url
        self.token_key = token_key
        self.lifetime = lifetime

    def validate(self):
        if check_invalid_string(self.private_key):
            raise ValueError("invalid private_key")
        if check_invalid_string(self.issuer):
            raise ValueError("invalid issuer")

    def __gen_standard_claims(self):
        now = timegm(datetime.utcnow().utctimetuple())
        return {
            constant.CLAIM_JWT_ID: uuid.uuid4().hex,
            constant.CLAIM_ISSUER: self.issuer,
            constant.CLAIM_ISSUE_AT: now,
            constant.CLAIM_EXPIRY: now + self.lifetime,
            constant.CLAIM_AUDIENCE: constant.App_Tencent_OneID
        }

    def sign(self, user_info):
        self.validate()
        # 校验参数并封装为payload
        cur_claims = {}
        if user_info is not None:
            if not isinstance(user_info, UserInfo):
                raise ValueError("invalid user_info")
            user_info.validate()
            cur_claims.update(user_info.as_claims())
        # 配置参数封装
        cur_claims.update(self.__gen_standard_claims())
        # 执行签名
        return jwt.encode(cur_claims, self.private_key, algorithm='RS256')

    def generate_login_url(self, user_info, app, params=None):
        # 获取url部分
        if check_invalid_string(self.login_url):
            raise ValueError("invalid login_url")
        if check_invalid_string(app):
            raise ValueError("invalid app")
        if app != oneid_auth.constant.App_Tencent_Meeting and app != oneid_auth.constant.App_Tencent_Docs:
            raise ValueError("invalid app")

        base_url = self.login_url
        if constant.APP_TYPE_PARAM in base_url:
            base_url = base_url.replace(constant.APP_TYPE_PARAM, app)
        parsed_url = urlparse(base_url)
        query_params = dict(parse_qsl(parsed_url.query))
        # 获取参数部分
        token = self.sign(user_info)
        query_params[self.token_key] = token
        if params is not None:
            if not isinstance(params, dict):
                raise ValueError("params must be None or dict")
            query_params.update(params)
        return urlunparse(parsed_url._replace(query=urlencode(query_params)))


# 校验是非法的字符串
def check_invalid_string(value):
    if not isinstance(value, str) or not bool(value.strip()):
        return True
    return False
