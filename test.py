import cv2
import sys
import face_recognition as fr

print("***********\n")
print("OpenCV version:", cv2.__version__)
print("Python version:", sys.version)
print(sys.executable)
print("***********")

txt_result = 'Unmatched'
faceDis = 1

imgLearn = fr.load_image_file("C:/Users/kinle/Downloads/OpenCV/KinLee-05Sep2021.jpg")
imgLearn = cv2.cvtColor(imgLearn,cv2.COLOR_BGR2RGB)

imgFind = fr.load_image_file("C:/Users/kinle/Downloads/OpenCV/kinlee-1.jpg")
imgFind = cv2.cvtColor(imgFind,cv2.COLOR_BGR2RGB)

faceLoc = fr.face_locations(imgLearn)[0]
encodeLearn = fr.face_encodings(imgLearn)[0]
cv2.rectangle(imgLearn,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)

faceLocFind = fr.face_locations(imgFind)[0]
encodeFind = fr.face_encodings(imgFind)[0]
cv2.rectangle(imgFind,(faceLocFind[3],faceLocFind[0]),(faceLocFind[1],faceLocFind[2]),(0,0,255),2)

results = fr.compare_faces([encodeLearn],encodeFind)
faceDis = fr.face_distance([encodeLearn],encodeFind)
print(results,faceDis) 

faceDis = round((1-faceDis[0])*100,2)

cv2.putText(imgFind,'Matched' f'{results} {faceDis}%',(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),1)

cv2.imshow('Machine Learning',imgLearn)

if results:
    outputText = 'Matched'

cv2.imshow(outputText,imgFind)

cv2.waitKey(0)