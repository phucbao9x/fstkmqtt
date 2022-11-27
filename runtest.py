# from fstkmqtt.algorithms.asymetric import rsa

# rsa.createPEM(4096)

# from fstkmqtt import MySQL
# from fstkmqtt import merginhmacsha256

# def run():
#     a = MySQL.MySQL()
#     a.config(
#         host = '127.0.0.1',
#         user = 'root',
#         password= 'pbao0219@',
#         database = 'CongTy1'
#     )
#     a.connect()
#     fmt = 'INSERT INTO AccountSys (Username, Passw, Hashlogin) VALUES (\'%s\', \'%s\', \'%s\')'
#     data = [
#         ('admin1', 'passadmin1', merginhmacsha256('', ['admin1', 'passadmin1'])),
#         ('admin2', 'passadmin2', merginhmacsha256('', ['admin2', 'passadmin2'])),
#         ('admin3', 'passadmin3', merginhmacsha256('', ['admin3', 'passadmin3'])),
#         ('admin4', 'passadmin4', merginhmacsha256('', ['admin4', 'passadmin4'])),
#     ]
#     try: a.executemany(fmt, data)
#     except: pass
#     a.disconnect()
#     a.reconnect()
#     fmt2 = 'SELECT * FROM AccountSys;'
#     print(a.execute(fmt2, iscommit = False))
#     a.disconnect()

#     a.poolConnect('pooltest1', 5, True)
#     a.poolInsert('AccountSys', 
#         columns = ('Username', 'Passw' ,'Hashlogin'), 
#         data = ('admin5', 'admin5pass', merginhmacsha256('', ['admin5', 'admin5pass'])))
#     a.poolDisconnect()

# run()

# from fstkmqtt.database.warehouse.warehouseconnect import warehouseconnect
# def r1():
#     a = warehouseconnect()
#     a.config((2022, 11, 23),nameproject = 'test')
#     a.connect()
#     a.execute('create table accountsys (ID INTEGER PRIMARY KEY, username VARCHAR(50) UNIQUE, password VARCHAR(50))', data=(), iscommit = True)
#     a.execute('insert into accountsys (ID,username,password) values(1, \'admin\', \'passwordadmin\')', data=(), iscommit = True)
#     print(a.execute('select * from accountsys;', data=(), isdata = True))
#     a.disconnect()
# def r2():
#     a = warehouseconnect()
#     a.config((2022, 11, 23),nameproject = 'test')
#     a.connect()
#     print(a.execute('select * from accountsys;', data=(), iscommit = True, isdata = True))
#     a.disconnect()
# r1()
# r2()



# from fstkmqtt.network.TCPServer.tcpserver import loop_forever_tcp_server
# loop_forever_tcp_server('localhost', 80)






# from fstkmqtt.render import GetRender

# print(
# GetRender._render_with_base_html(
#     """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta http-equiv="X-UA-Compatible" content="IE=edge">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Document</title>
# </head>
# <body>
#     %asfsfd%
#     %adfsdf%
#     %fsudhfiu%
# </body>
# </html>""",
# """
# %begin asfsfd%
#     <div></div>
# %end asfsfd%
# """,
# js= '',
# css=''
# ))

# from fstkmqtt.security.Database import SQL
# try:
#     print(SQL.injectionFromQuery("SELECT COUNT(*) FROM accountsys WHERE username='' AND password='1'", 
#     'SELECT COUNT(*) FROM accountsys WHERE username=\'%s\' AND password=\'%s\''))
# except Exception as e:
#     print(e)

from fstkmqtt.TrafficApp import TrafficApp

tmp = TrafficApp()
tmp.config(
    ca_file = 'C://Users//Admin//Desktop//certificate//ca_server.crt',
    key_file = 'C://Users//Admin//Desktop//certificate//ca_server_pri.pem')
@tmp.route('/')
def haha(request, *args, **kwargs):
    return b"""HTTP/1.1 200 OK
Date: Mon, 27 Jul 2009 12:28:53 GMT
Server: FullstackMQTT/0.0.1a (Win32)
Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
Content-Type: text/html

<html>
<body>
<h1>Hello, World!</h1>
</body>
</html>"""

@tmp.route('/hello')
def asdf( *args, **kwargs):
    return b"""HTTP/1.1 200 OK
Date: Mon, 27 Jul 2009 12:28:53 GMT
Server: FullstackMQTT/0.0.1a (Win32)
Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
Content-Type: text/html

<html>
<body>
<h1>Hello, My name is Bao</h1>
</body>
</html>"""

tmp.run()

# # #handling_func -> default 
# from fstkmqtt.network.HTTPServer.httpserver import loop_forever_http_server
# # loop_forever_http_server(
# #     'localhost', 
# #     8080, 
# #     ca_file = 'C://Users//Admin//Desktop//certificate//ca_server.crt', 
# #     key_file= 'C://Users//Admin//Desktop//certificate//ca_server_pri.pem')
# loop_forever_http_server(
#     'localhost', 
#     3445)