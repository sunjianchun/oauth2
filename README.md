# oauth2


一：授权码模式、简化模式<br/>
1：http请求<br/>
![image](https://github.com/sunjianchun/oauth2/blob/master/md/image/code.jpeg)<br/>
测试用例：浏览器访问：http://127.0.0.1:9090/web/authorize/?response_type=token&client_id=family&redirect_uri=http://127.0.0.1:8888/oauth2/showcode&state=somestate&scopes=email,id/idCard,address/sex <br/>
![image](https://github.com/sunjianchun/oauth2/blob/master/md/image/web.png)<br/>

2：用户授权后携带code去申请accesss_token(简化模式可以直接获得access_token)<br/>
http请求<br/>

![image](https://github.com/sunjianchun/oauth2/blob/master/md/image/code1.jpeg)<br/>
2：curl 模拟访问<br/>
curl -XPOST 'http://127.0.0.1:9090/api/v1/tokens' -d "grant_type=authorization_code&client_id=test@test.com&client_secret=123456&state=state&code=7fc9e8dc-0d71-4044-92fd-a747b78f30c5"<br/>

输出：<br/>
{<br/>
"access_token": "71c85621-2051-4007-9a1a-882ce203bfa0",<br/>
"expire_in": 3600,<br/>
"token_type": "Bearer",<br/>
"scope": "email id/idCard address/sex",<br/>
"refresh_token": "03217e25-1c55-44a1-b167-15f7ca358943"<br/>
}<br/>

二：password模式<br/>
1：http请求<br/>



![image](https://github.com/sunjianchun/oauth2/blob/master/md/image/pass.jpeg)<br/>
2：curl 请求 curl -XPOST 'http://127.0.0.1:9090/api/v1/tokens' -d "grant_type=password&client_id=test@test.com&client_secret=123456&state=state&username=user@test.com&password=123456"<br/>

{<br/>
"access_token": "f0f83809-6ac4-4d12-ba5e-ae849b7c8a81",<br/>
"expire_in": 3600,<br/>
"token_type": "Bearer",<br/>
"scope": "id/idCard",<br/>
"refresh_token": "2a7bbf77-f1ee-42fc-b930-c4314740d19d"<br/>
}<br/>

三：refresh_token的grant_type<br/>
1：http请求<br/>

![image](https://github.com/sunjianchun/oauth2/blob/master/md/image/refresh_token.jpeg)<br/>

2：curl 请求 curl -XPOST 'http://127.0.0.1:9090/api/v1/tokens' -d "grant_type=refresh_token&client_id=test@test.com&client_secret=123456&state=state&refresh_token=2a7bbf77-f1ee-42fc-b930-c4314740d19d"<br/>

{<br/>
"access_token": "731a7a20-5151-4720-88d3-58be454265fd",<br/>
"expire_in": 3600,<br/>
"token_type": "Bearer",<br/>
"scope": "id/idCard",<br/>
"refresh_token": "ed8729f4-eca1-4bb7-9467-ffb7c316035c"<br/>
}<br/>

四：客户端模式<br/>
1：http请求<br/>

![image](https://github.com/sunjianchun/oauth2/blob/master/md/image/client.jpeg)<br/>
2：curl 请求 curl -XPOST 'http://127.0.0.1:9090/api/v1/tokens' -d "grant_type=client_credentials&client_id=test@test.com&client_secret=123456&state=state"<br/>

{<br/>
"access_token": "ba041229-fac4-4202-b61f-33168e689a45",<br/>
"expire_in": 3600,<br/>
"token_type": "Bearer",<br/>
"scope": "id/idCard",<br/>
"refresh_token": "05acfbc4-a80c-4d62-82ae-e4dc21f185f5"<br/>
}<br/>
