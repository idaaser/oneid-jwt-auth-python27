# oneid-jwt-auth-python27

OneID JWT auth sdk for python
> 仅支持Python2.7版本

## 使用步骤
### 集成SDK
使用 `pip`安装SDK
```python
    # 安装最新版本
    pip install git+https://github.com/idaaser/oneid-jwt-auth-python27.git
    # 安装指定版本
    pip install git+https://github.com/idaaser/oneid-jwt-auth-python27.git@`版本号`
```

### 使用SDK
> 使用案例参考：test/idp_test.py
1. 初始化配置：
```pythpn
jwt_config = oneid_auth.JwtConfig(testPrivKey, testIssuer, testLoginBaseURL)
```
2. 生成免登url：
- 通过用户信息UserInfo生成(UserInfo中preferred_username、email、mobile三个属性至少存在一个)
```python
user_info = oneid_auth.UserInfo("user_id_123", name="jinrruan", email="jinrruan@qq.com")

login_url = oneid_auth.generate_login_url(jwt_config, 
                                          user_info=user_info,
                                          app=oneid_auth.App_Tencent_Meeting, 
                                          params={"name": "1+2", "age": 18, "email": "123@qq.com"})
```
- 通过自定义claims生成
```python
cur_claims = {"user_id": "user_id_123", "name": "jinrruan",
                  "email": "jinrruan@qq.com",
                  "haha": "====", "iss": "jinrruan"}

login_url = oneid_auth.generate_login_url(jwt_config,
                                          claims=cur_claims,
                                          app=oneid_auth.App_Tencent_Docs,
                                          params={"name": "1+2", "age": 18, "email": "123@qq.com"})
```