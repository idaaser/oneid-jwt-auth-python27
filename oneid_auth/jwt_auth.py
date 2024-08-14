# coding=utf-8
import model
import jwt
import urllib
import constant


def generate_token(jwt_config, user_info=None, claims=None):
    # 校验配置jwt_config
    if jwt_config is None or not isinstance(jwt_config, model.JwtConfig):
        raise ValueError("invalid jwt_config")
    jwt_config.validate()
    # 校验参数并封装为payload
    if user_info is None and claims is None:
        raise ValueError("user_info/claims must not all empty")
    cur_claims = {}
    if user_info is not None:
        if not isinstance(user_info, model.UserInfo):
            raise ValueError("invalid user_info")
        user_info.validate()
        cur_claims.update(user_info.as_claims())
    if claims is not None:
        if not isinstance(claims, dict):
            raise ValueError("invalid claims")
        cur_claims.update(claims)
    # 配置参数封装
    cur_claims.update(jwt_config.as_claims())
    # 执行签名
    return jwt.encode(cur_claims, jwt_config.private_key, algorithm='RS256')


def generate_login_url(jwt_config, user_info=None, claims=None, app=None, params=None):
    # 获取url部分
    if not isinstance(jwt_config.login_url, basestring) or not bool(jwt_config.login_url.strip()):
        raise ValueError("invalid login_url")
    base_url = jwt_config.login_url
    if constant.APP_TYPE_PARAM in base_url:
        if not isinstance(app, basestring) or not bool(app.strip()):
            raise ValueError("invalid app")
        base_url = base_url.replace(constant.APP_TYPE_PARAM, app)
    # 获取参数部分
    token = generate_token(jwt_config, user_info, claims)
    query_param = {
        jwt_config.token_param: token
    }
    if params is not None:
        if not isinstance(params, dict):
            raise ValueError("params must be None or dict")
        query_param.update(params)
    cur_params = urllib.urlencode(query_param)
    return base_url + "?" + cur_params


