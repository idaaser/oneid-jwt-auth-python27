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
> 使用案例参考：tests/test_jws.py
1. 初始化配置：
- 私钥以String形式提供
```python
jwt_signer = oneid_auth.Signer(private_key, issuer, login_url)
```
- 私钥以文件形式提供
```python
jwt_signer = oneid_auth.Signer.new_signer_from_key_file(key_file_path, issuer, login_url)
```
2. 生成免登url：
- 通过用户信息UserInfo生成(UserInfo中user_id和name为必传字段，username、email、mobile三个属性至少存在一个)

```python
user_info = oneid_auth.UserInfo("f99530d4-8317-4900-bd02-0127bb8c44de", "张三",
                                username="zhangsan",
                                email="zhangsan@example.com",
                                mobile="+86 13411112222")

login_url = jwt_signer.new_login_url(user_info, oneid_auth.App_Tencent_Meeting,
                                     params={"meeting_common": "https://meeting.tencent.com"})
```
