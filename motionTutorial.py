import time
import cv2,pandas
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__, static_folder='static')

# Your boolean data
boolean_data = True  # Replace this with your boolean data

@app.route('/')
def index():
    return render_template('index.html', boolean_data=boolean_data)

if __name__ == '__main__':
    app.run(debug=True)



first_frame = None
status_list = [None,None]
time_stamp=[]
df = pandas.DataFrame(columns=["Start", "End"])
video = cv2.VideoCapture(0)     
motion_threshold = 12000

amount_of_movement = 0
delay_seconds = 3
for i in range(delay_seconds, 0, -1):
    print(f"{i} seconds remaining, Get In Position!")
    time.sleep(1)  # Pause for 1 second
print("Start")

while True:

    
    check,color_frame=video.read()
    status=0
    gray=cv2.cvtColor(color_frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)
    
    if not check:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    if first_frame is None:
        first_frame = gray
        continue
    
    delta_frame=cv2.absdiff(first_frame, gray)
    thresh_frame=cv2.threshold(delta_frame, 150, 255, cv2.THRESH_BINARY)[1]
    
    
    thresh_frame=cv2.dilate(thresh_frame,None,iterations=3)
    (cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in cnts:
        if cv2.contourArea(contour) < motion_threshold:
            continue
        status=1
        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(color_frame,(x,y),(x+w,y+h),(0,0,255),2)
    
    status_list.append(status)
    
    if status_list[-1]==1 and status_list[-2]==0:
        time_stamp.append(datetime.now())
        print("Motion Detected")
        amount_of_movement+=1
        print(amount_of_movement) 
    if status_list[-1]==0 and status_list[-2]==1:
        time_stamp.append(datetime.now())
        
    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Colour Frame", color_frame)
    
    key=cv2.waitKey(1)
    if key==ord('q'):
        if status==1:
            time_stamp.append(datetime.now())
        break
    

print(status_list)
for i in range(0, len(time_stamp),2):
    df=df.append({"Start":time_stamp[i],"End":time_stamp[i+1]},ignore_index=True)
    
df.to_csv("All_Time_Stamp.csv")
video.release()
cv2.destroyAllWindows()

