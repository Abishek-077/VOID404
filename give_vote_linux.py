from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
import pyttsx3  # Replaced win32com
from datetime import datetime

# Initialize Text-to-Speech Engine for Linux
def speak(str1):
    engine = pyttsx3.init()
    # Optional: adjust speed (rate) or volume
    engine.setProperty('rate', 150) 
    engine.say(str1)
    engine.runAndWait()

video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

if not os.path.exists('data/'):
    os.makedirs('data/')

# Ensure these files exist from your previous data collection script
with open('data/names.pkl', 'rb') as f:
    LABELS = pickle.load(f)

with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

# Ensure background.png exists in your folder
imgBackground = cv2.imread("background.png")

COL_NAMES = ['NAME', 'VOTE', 'DATE', 'TIME']

def check_if_exists(value):
    try:
        if not os.path.isfile("Votes.csv"):
            return False
        with open("Votes.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and row[0] == value:
                    return True
    except Exception as e:
        print(f"Error reading CSV: {e}")
    return False

while True:
    ret, frame = video.read()
    if not ret:
        break
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    output = None 
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)
        
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
        cv2.putText(frame, str(output[0]), (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        
    # UI Overlay (Adjust coordinates if background.png size differs)
    if imgBackground is not None:
        imgBackground[370:370 + 480, 225:225 + 640] = frame
        cv2.imshow('frame', imgBackground)
    else:
        cv2.imshow('frame', frame)
        
    k = cv2.waitKey(1)
    
    if output is not None:
        voter_name = str(output[0])
        voter_exist = check_if_exists(voter_name)
        
        if voter_exist:
            speak("YOU HAVE ALREADY VOTED")
            time.sleep(2)
            break

        # Voting Logic
        party = None
        if k == ord('1'): party = "BJP"
        if k == ord('2'): party = "CONGRESS"
        if k == ord('3'): party = "AAP"
        if k == ord('4'): party = "NOTA"

        if party:
            speak("YOUR VOTE HAS BEEN RECORDED")
            exist = os.path.isfile("Votes.csv")
            with open("Votes.csv", "a") as csvfile:
                writer = csv.writer(csvfile)
                if not exist:
                    writer.writerow(COL_NAMES)
                attendance = [voter_name, party, date, timestamp]
                writer.writerow(attendance)
            
            speak("THANK YOU FOR PARTICIPATING IN THE ELECTIONS")
            time.sleep(2)
            break

video.release()
cv2.destroyAllWindows()
