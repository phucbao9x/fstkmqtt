def request(sock, buffer) -> bytes:
    data = b''
    while True:
        tmp = sock.recv(buffer)
        data += tmp
        if len(tmp) < buffer: break
    return data

def response(sock, data : bytes, buffer = -1) :
    if buffer > 0:
        dtl = []
        for i in range(len(data) // buffer):
            dtl.append(data[i*buffer:i*buffer + buffer])
        else:
            if len(data) % buffer: dtl.append(data[i*buffer + buffer:])
        for i in dtl:
            sock.send(i)
    else:
        sock.send(data)