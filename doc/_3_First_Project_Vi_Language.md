Chúng ta đã hiểu về những yếu tố cần thiết để tạo một dự án. Bây giờ chúng ta sẽ cùng nhau tạo ra một dự án nhỏ đầu tiên.

# **Dự án đầu tiên**
_Hãy nhớ cài package trước nhé. Nếu bạn chưa cài hãy_ <a href="_1_Introduction_Vi_Language.md">_xem lại nhé_</a>
<br>
__Bước 1: Mình di chuyển đến desktop__<br>
Mình thực hiện dòng lệnh sau:
~~~
>> python -m pyFMQTT --name firstproject
~~~
Sau đó:
~~~
>> cd firstproject
~~~
Và hiện tại là:
~~~
.../firstproject>>
~~~
__Bước 2: Mình tạo 2 ứng dụng mới là hello và name__<br>
Mình thực hiện 2 dòng lệnh sau:
~~~
.../firstproject>> python tool.py --createapp hello
.../firstproject>> python tool.py --createapp name
~~~
__Bước 3: Chỉnh sửa nội dung__<br>
Mình chỉnh sửa các file ở .../firstproject/view/hello/theme/index.html và .../firstproject/view/name/theme/index.html thành như sau:<br><br>
Với index.html của app hello:
~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello</title>
</head>
<body>
    <h1>Hello</h1>
    <a href="name">Move to name</a>
</body>
</html>
~~~
Với index.html của app name:
~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Name</title>
</head>
<body>
    <h1>Name</h1>
    <a href="hello">Move to Hello</a>
</body>
</html>
~~~

Tiếp theo đó, mình sẽ sửa nội dung trong viewmodel cho 2 app.
Tại viewmodel/hello/page.py mình sửa thành:
~~~python
....

def page_hello_process(request, *args, **kwargs):
	value, _ = GetRender.Render(filehtml = allfile['theme/index'])
	value = value.decode()
	res = """
HTTP/1.1 200 OK
Date: Mon, 27 Jul 2009 12:28:53 GMT
Server: FullstackMQTT/0.0.1a (Win32)
Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
Content-Type: text/html\n\n"""
	res += value
	return res.encode()
~~~
Tại viewmodel/name/page.py mình sửa thành:
~~~python
....

def page_name_process(request, *args, **kwargs):
	value, _ = GetRender.Render(filehtml = allfile['theme/index'])
	value = value.decode()
	res = """
HTTP/1.1 200 OK
Date: Mon, 27 Jul 2009 12:28:53 GMT
Server: FullstackMQTT/0.0.1a (Win32)
Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
Content-Type: text/html\n\n"""
	res += value
	return res.encode()
~~~

__Bước 4: Chạy ứng dụng__<br>
Quay lại firstproject ta dùng lệnh sau:
~~~terminal
.../firstproject>> python app.py
~~~

__À hèm, chúc mừng bạn__