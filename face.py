import face_recognition
import time
import os
from os.path import basename
import socketserver

girls_info = []
count = 0

dst_path = 'e:/img/'
for file in os.listdir(dst_path):
    #print(file)

    girl = {}
    girl['name'] = basename(file)
    #print(girl['name'])
    
    picture_of_me = face_recognition.load_image_file(dst_path + file)
    result = face_recognition.face_encodings(picture_of_me)
    if len(result) == 0:
        print('can not indify image', file)
        continue
    
    girl['face_encoding'] = result[0]
    girls_info.append(girl)
    count += 1
    #print(count)


def get_girl_name(path):
    unknown_picture = face_recognition.load_image_file(path)
    result = face_recognition.face_encodings(unknown_picture)
    if len(result) == 0:
        print('can not find you face', path)
        return 'can not find you face'

    name_of_girl = 'can not find this girl'
    mini_distance = 1
    unknown_face_encoding = result[0]
    for girl in girls_info:
        results = face_recognition.compare_faces([girl['face_encoding']], unknown_face_encoding)
        if results[0] == True:
            #print(girl['name'])
            face_distances = face_recognition.face_distance([girl['face_encoding']], unknown_face_encoding)
            print(face_distances)
            if face_distances < mini_distance:
                mini_distance = face_distances
                name_of_girl = girl['name']
                
    print('result distance is ', mini_distance)
    return name_of_girl

get_girl_name('e:/facenet-master/src/2.jpg')

# class MyTCPHandler(socketserver.BaseRequestHandler):
    
#     def handle(self):
#         # self.request is the TCP socket connected to the client
#         self.data = self.request.recv(1024).strip()
#         print("{} wrote:".format(self.client_address[0]))
#         #print(self.data)

#         path = 'f:/test-code/' + self.data.decode('utf-8')
#         print(path)
        
#         result = get_girl_name(path)
#         print(result)
#         self.request.sendall(bytes(result, 'utf-8'))

        
# HOST, PORT = "localhost", 9999
# #server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
# server = socketserver.ThreadingTCPServer(( 'localhost', 9999), MyTCPHandler)
# server.serve_forever()
