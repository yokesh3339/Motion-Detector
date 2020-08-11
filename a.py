import cv2,time,pandas
from datetime import datetime
video=cv2.VideoCapture(0)
df=pandas.DataFrame(columns=('start','end'))
first_frame=None
status_list=[None,None]
time=[]
while True:
    status=0
    check,frame=video.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)
    if first_frame is None:
        first_frame=gray
        continue
    delta_frame=cv2.absdiff(first_frame,gray)
    thresh=cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
    thresh=cv2.dilate(thresh,None,iterations=2)
    (cnts,_)=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        if cv2.contourArea(c)<1000:
            continue
        status=1
        (x,y,w,h)=cv2.boundingRect(c)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    #cv2.imshow("Blur",gray)
    cv2.imshow("Capture",frame)
    #cv2.imshow("thresh",thresh)
    #cv2.imshow("delta_frame",delta_frame)
    status_list.append(status)
    status_list=status_list[-2:]
    if status_list[-1]==1 and status_list[-2]==0:
        time.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        time.append(datetime.now())
    key=cv2.waitKey(1)
    if key==ord('q'):
        if status==1:
            time.append(datetime.now())
        break
for i in range(0,len(time),2):
    df=df.append({'start':time[i],'end':time[i+1]},ignore_index=True)
df.to_csv('times.csv')
print(status_list)
print(time)
video.release()
cv2.destroyAllWindows()