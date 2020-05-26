import socket

HOST = '192.168.0.13'
PORT = 9999

Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
networkType = input("소켓 타입(sever/client): ")

if networkType == "server":
    Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    Socket.bind(('', PORT))
    Socket.listen()

    Connection_Socket, addr = Socket.accept()
    print('Connected by ', addr)
    print('종료를 원하면 Q를 입력하세요.')

    while True:
        #메시지 수신
        recv_msg = Connection_Socket.recv(1024)
        if recv_msg == 'Q':
            print('상대방이 통신을 종료했습니다.')
            break
        print('상대방: ', recv_msg.decode('utf-8'))

        #메시지 전송
        send_msg = input("나: ")
        Connection_Socket.send(send_msg.encode('utf-8'))
        if send_msg == 'Q':
            break

    Connection_Socket.close()

elif networkType == "client":
    Socket.connect((HOST, PORT))
    print('종료를 원하면 Q를 입력하세요.')

    while True:
        #메시지 전송
        send_msg = input("나: ")
        Connection_Socket.send(send_msg.encode('utf-8'))
        if send_msg == 'Q':
            break

        #메시지 수신
        recv_msg = Connection_Socket.recv(1024)
        if recv_msg == 'Q':
            print('상대방이 통신을 종료했습니다.')
            break
        print('상대방: ', recv_msg.decode('utf-8'))

Socket.close()
