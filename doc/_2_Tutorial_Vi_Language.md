# **Hướng dẫn cơ bản**
## **Tạo một dự án**
~~~terminal
>> python -m fstkmqtt <name project>
~~~

## **Tạo một ứng dụng**
Sau khi tạo dự án thành công, chúng ta truy cập vào đường dẫn file qua terminal sau đó:
~~~terminal
>> python tool.py --createapp <nameapp>
~~~

## **Tạo một liên kết cơ sở dữ liệu**
Tương tự với cách tạo ứng dụng. Nhưng chúng ta sẽ sử dụng tập lệnh sau:
~~~terminal
>> python tool.py --createconnect <dbname> [--host <host>, --port <port>, --dbpath <path to db sqlite>, --user <username>, --password <password>]
~~~

## **Dạng tổ chức của một dự án Fullstack MQTT**
Nhằm đề tối ưu hoá quá trình quản lý và nâng làm việc nhóm hiệu quả. FullstackMQTT hỗ trợ mô hình __MVVM__ (Model - View - View Model) - hay là mô hình _tam lớp_.<br><br>
__Cấu trúc chính của dự án__<br>
~~~
[project]
  '-- [view]
  |-- [viewmodel]
  |-- [model]
  |-- app.py
  '-- tool.py
~~~
Tệp tin app.py và tool.py sẽ được tự tạo sau khi tạo dự án. Tuy nhiên, bạn có thể chỉnh sửa cấu trúc theo sở thích của bạn hoặc chỉnh sửa định hướng (@app.route) theo mong muốn của bạn.

_lưu ý: file tool.py không được chỉnh sửa nhằm tránh sảy ra lỗi lầm._<br>
<br>
___1. Lớp View___:<br>
Lớp View có cấu trúc sau:
~~~
[view]
  '-- __init__.py
  |-- [app thứ 1]
  |     '-- __init__.py
  |     |-- [theme]  ; chứa tệp tin html
  |     |-- [style]  ; chứa tệp tin css
  |     |-- [code]   ; chứa tệp tin js
  |     '-- base.html ; có thể có hoặc không
  |--  ...
  |-- [app thứ n]
  |     '-- ...
  '-- tutorial.txt
~~~
Với các app được tạo ra qua các bước ở tạo một ứng dụng
<br><br>
___2. Lớp View Model___:<br>
Lớp View có cấu trúc sau:
~~~
[viewmodel]
  '-- __init__.py
  |-- [app thứ 1]
  |     '-- __init__.py
  |     '-- page.py ; Xử lý request, payload từ client, trả về giá trị bytes để gửi cho client
  |--  ...
  |-- [app thứ n]
  |     '-- ...
  '-- tutorial.txt
~~~
Với các app được tạo ra qua các bước ở tạo một ứng dụng<br>
<br>
___3. Lớp Model___:<br>
Lớp View có cấu trúc sau:
~~~
[model]
  '-- __init__.py
  |-- connect thứ 1.py
  |--  ...
  |-- connect thứ n.py
  '-- tutorial.txt
~~~
Lớp model chứa các mã nguồn kết nối đến cơ sở dữ liệu của bạn.

Như vậy, bạn đã nắm được tổ chức hệ thống dự án, Bây giờ chúng ta sẽ cùng tạo một <a href="_3_First_Project_Vi_Language.md">**dự án nhỏ**</a> về web để chứng mình Fullstack của nó.