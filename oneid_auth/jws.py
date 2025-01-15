# coding=utf-8
import jwt, uuid

import oneid_auth.constant
from . import constant
from datetime import datetime
from calendar import timegm
from urlparse import urlparse, parse_qsl, urlunparse
from urllib import urlencode
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from .constant import DEFAULT_TOKEN_PARAM


class UserInfo:
    """
    用户信息

    :parameter user_id: 必填: 用户唯一标识
    :parameter name: 用户显示名
    :parameter username: 建议填写: 用户登录名，1-64个英文字符或数字，用户登录名、邮箱、手机号三者必须提供一个
    :parameter email: 选填: 邮箱，用户登录名、邮箱、手机号三者必须提供一个
    :parameter mobile: 选填: 手机号，用户登录名、邮箱、手机号三者必须提供一个
    :parameter extension: 其他需要放到id_token里的属性
    """
    def __init__(self, user_id, name, username=None, email=None, mobile=None, extension=None):
        if check_invalid_string(user_id):
            raise ValueError("user_id must not be empty")
        if check_invalid_string(name):
            raise ValueError("name must not be empty")

        if (check_invalid_string(username)
                and check_invalid_string(email)
                and check_invalid_string(mobile)):
            raise ValueError("username/email/mobile must not all empty")

        self.user_id = user_id.strip()
        self.name = name.strip()
        if username is not None:
            self.username = username.strip()
        if email is not None:
            self.email = email.strip()
        if mobile is not None:
            self.mobile = mobile.strip()
        self.extension = extension

    def as_claims(self):
        claims = {}
        if self.extension is not None:
            claims.update(self.extension)
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
    """
    初始化JWT认证签发器

    :parameter private_key: 私钥
    :parameter issuer: 发起登录方的应用标识
    :parameter login_base_url: OneID JWT认证源页面提供的登录链接
    :returns an JWT signer
    :raise Exception
    """
    def __init__(self, private_key, issuer, login_base_url, token_lifetime=constant.TOKEN_EXPIRE_SECOND):
        if check_invalid_string(private_key):
            raise ValueError("private_key must not be empty")
        if check_invalid_string(issuer):
            raise ValueError("issuer must not be empty")
        if check_invalid_string(login_base_url):
            raise ValueError("login_url must not be empty")
        parse_res = urlparse(login_base_url)
        if not all([parse_res.scheme, parse_res.netloc, parse_res.path]):
            raise ValueError("login_url is invalid")

        if token_lifetime <= 0 or token_lifetime > constant.TOKEN_EXPIRE_SECOND:
            raise ValueError("lifetime must be greater than 0 and less than or equal to 300 seconds")

        handled_key = self.__normalize_key(private_key)
        parsed_key = load_pem_private_key(handled_key.encode(), password=None)
        self.private_key = parsed_key
        self.issuer = issuer.strip()
        self.login_url = login_base_url.strip()
        self.token_key = DEFAULT_TOKEN_PARAM
        self.lifetime = token_lifetime

    """
    初始化JWT认证签发器

    :parameter private_key: 私钥文件路径
    :parameter issuer: 发起登录方的应用标识
    :parameter login_base_url: OneID JWT认证源页面提供的登录链接
    :returns an JWT signer
    :raise Exception
    """
    @classmethod
    def new_signer_from_key_file(cls, key_file_path, issuer, login_url,
                                 token_lifetime=constant.TOKEN_EXPIRE_SECOND):
        try:
            with open(key_file_path, "r") as key_file:
                private_key = key_file.read()
                return Signer(private_key, issuer, login_url, token_lifetime)
        except IOError:
            raise ValueError("key file not found")
        except Exception as e:
            raise e

    @classmethod
    def __normalize_key(cls, private_key):
        private_key = private_key.strip()
        prefix, suffix = "-----BEGIN PRIVATE KEY-----", "-----END PRIVATE KEY-----"
        if private_key.startswith(prefix):
            private_key = private_key[len(prefix):]
            private_key = private_key[:-len(suffix)]
        private_key = private_key.strip()

        return prefix + "\r\n" + private_key + "\r\n" + suffix

    def __gen_standard_claims(self):
        now = timegm(datetime.utcnow().utctimetuple())
        return {
            constant.CLAIM_JWT_ID: uuid.uuid4().hex,
            constant.CLAIM_ISSUER: self.issuer,
            constant.CLAIM_ISSUE_AT: now,
            constant.CLAIM_EXPIRY: now + self.lifetime,
            constant.CLAIM_AUDIENCE: constant.App_Tencent_OneID
        }

    def __new_token(self, user_info):
        # 校验参数并封装为payload
        cur_claims = {}
        if user_info is not None:
            if not isinstance(user_info, UserInfo):
                raise ValueError("invalid user_info")
            cur_claims.update(user_info.as_claims())
        # 配置参数封装
        cur_claims.update(self.__gen_standard_claims())
        # 执行签名
        return jwt.encode(cur_claims, self.private_key, algorithm='RS256')

    """
    为指定用户创建一个免登应用的url
     
    :parameter user 免登用户的信息
    :parameter app 免登应用的唯一标识
    :returns 免登链接
    :raise Exception
    """
    def new_login_url(self, user_info, app, params=None):
        # 获取url部分
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
        token = self.__new_token(user_info)
        query_params[self.token_key] = token
        if params is not None:
            if not isinstance(params, dict):
                raise ValueError("params must be None or dict")
            for k, v in params.items():
                if not isinstance(k, str) or not isinstance(v, str):
                    raise ValueError("params key/value must be str")
                if k != "" and v != "":
                    query_params[k] = v
        return urlunparse(parsed_url._replace(query=urlencode(query_params)))


# 校验是非法的字符串
def check_invalid_string(value):
    if not isinstance(value, str) or not bool(value.strip()):
        return True
    return False
