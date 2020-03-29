import cv2 
import time
import os
import stat

from socket import *
import select

serverName = '127.0.0.1'
serverPort = 9946
BUFSIZ = 1024
ADDR = (serverName,serverPort)
count = 0;

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(ADDR)
print("send");
clientSocket.send(str(count%10).encode('utf-8'))

#capture = cv2.VideoCapture(0)
capture = cv2.VideoCapture("./yinghua.flv")

last_time = time.time()
detect_data_file_path = "/mnt/wsyRamdisk/detect_data.txt"
camera_data_file_path = "/mnt/wsyRamdisk/camera_data.jpg"

ret, frame = capture.read()
cv2.imwrite(camera_data_file_path,frame)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(ADDR)
print("send");
clientSocket.send(str(count%10).encode('utf-8'))
count += 1
pos = []

while(True):
    ret, frame = capture.read()
    data = None
    r_list, w_list, e_list = select.select([clientSocket], [clientSocket], [clientSocket], 1)
    for event in r_list:
        try:
            data = event.recv(1024)
        except Exception as e:
            print(e)
        if data:
            print("rev:",chr(data[0]))
            clientSocket.close()
            
            if os.path.exists(detect_data_file_path):
                with open(detect_data_file_path) as f: #get detect data
                    org_data = f.read().strip()
                    if org_data:
                        #print(org_data)
                        pos = org_data.split('\n')
                        #print(pos)
                        pos = [x.strip().split(',')  for x in pos]
                        #print(pos)
                    else:
                        pos = None

                    f.close()
                    os.remove(detect_data_file_path)
                    
            if os.path.exists(camera_data_file_path):
                os.remove(camera_data_file_path)
                print("save picture",camera_data_file_path)
                cv2.imwrite(camera_data_file_path,frame)
                os.chmod(camera_data_file_path, stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)
            
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect(ADDR)
            print("send");
            clientSocket.send(str(count%10).encode('utf-8'))
            count += 1
            

        else:
            print("远程断开连接")
            #r_inputs.clear()
    '''
    if os.path.exists(detect_data_file_path):
        with open(detect_data_file_path) as f: #get detect data
            print(f.read())
            f.close()
            os.remove(detect_data_file_path)
            
    if os.path.exists(camera_data_file_path):
        os.remove(camera_data_file_path)
    print("save picture",camera_data_file_path)
    cv2.imwrite(camera_data_file_path,frame)
    '''
    if pos:
        for p in pos:
            cv2.rectangle(frame, (int(p[0]), int(p[2])), (int(p[1]), int(p[3])), (0, 255, 0), 4)

    cv2.imshow('frame', frame)

        
    if cv2.waitKey(50) == ord('q'):
        break
        





