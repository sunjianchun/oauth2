# oauth2


一：授权码模式、简化模式<br/>
1：http请求
![image](https://github.com/sunjianchun/oauth2/blob/master/md/image/code.jpeg)
参数及方法内容是否必须方法GET是response_typecode/token是client_idtest@test.com是client_secret123456是redirect_urihttp://127.0.0.1:8888/oauth2/showcode是scopesemail,id/idCard （多个权限以，号分割）否statesomestate是

测试用例：浏览器访问：http://127.0.0.1:9090/web/authorize/?response_type=token&client_id=family&redirect_uri=http://127.0.0.1:8888/oauth2/showcode&state=somestate&scopes=email,id/idCard,address/sex


2：用户授权后携带code去申请accesss_token(简化模式可以直接获得access_token)
http请求
参数及方法内容是否必须方法POST是grant_typeauthorization_code是client_idtest@test.com是client_secret123456是statesomestate是code7fc9e8dc-0d71-4044-92fd-a747b78f30c5是

2：curl 模拟访问
curl -XPOST 'http://127.0.0.1:9090/api/v1/tokens' -d "grant_type=authorization_code&client_id=test@test.com&client_secret=123456&state=state&code=7fc9e8dc-0d71-4044-92fd-a747b78f30c5"

输出：
{
"access_token": "71c85621-2051-4007-9a1a-882ce203bfa0",
"expire_in": 3600,
"token_type": "Bearer",
"scope": "email id/idCard address/sex",
"refresh_token": "03217e25-1c55-44a1-b167-15f7ca358943"
}

二：password模式
1：http请求
参数及方法内容是否必须方法POST是grant_typepassword是client_idtest@test.com是client_secret123456是statesomestate是usernameuser@test.com是password123456是scopesemail否


2：curl 请求 curl -XPOST 'http://127.0.0.1:9090/api/v1/tokens' -d "grant_type=password&client_id=test@test.com&client_secret=123456&state=state&username=user@test.com&password=123456"

{
"access_token": "f0f83809-6ac4-4d12-ba5e-ae849b7c8a81",
"expire_in": 3600,
"token_type": "Bearer",
"scope": "id/idCard",
"refresh_token": "2a7bbf77-f1ee-42fc-b930-c4314740d19d"
}

三：refresh_token的grant_type
1：http请求
参数及方法内容是否必须方法POST是grant_typerefresh_token是client_idtest@test.com是client_secret123456是statesomestate是refresh_token2a7bbf77-f1ee-42fc-b930-c4314740d19d是scopesemail否


2：curl 请求 curl -XPOST 'http://127.0.0.1:9090/api/v1/tokens' -d "grant_type=refresh_token&client_id=test@test.com&client_secret=123456&state=state&refresh_token=2a7bbf77-f1ee-42fc-b930-c4314740d19d"

{
"access_token": "731a7a20-5151-4720-88d3-58be454265fd",
"expire_in": 3600,
"token_type": "Bearer",
"scope": "id/idCard",
"refresh_token": "ed8729f4-eca1-4bb7-9467-ffb7c316035c"
}

四：客户端模式
1：http请求
参数及方法内容是否必须方法POST是grant_typeclient_credentials是client_idtest@test.com是client_secret123456是statesomestate是scopesemail否


2：curl 请求 curl -XPOST 'http://127.0.0.1:9090/api/v1/tokens' -d "grant_type=client_credentials&client_id=test@test.com&client_secret=123456&state=state"

{
"access_token": "ba041229-fac4-4202-b61f-33168e689a45",
"expire_in": 3600,
"token_type": "Bearer",
"scope": "id/idCard",
"refresh_token": "05acfbc4-a80c-4d62-82ae-e4dc21f185f5"
}
