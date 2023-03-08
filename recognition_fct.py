import cv2
import streamlit as st
import datetime
from video_detection import pretrained_age

def opencam():
    ### CHARGER LE MODELE 
    #path = "/Users/titouanhoude/Documents/GitHub/ImageSpeechRecognition/video"
    path = "C:/Documents/GitHub/ImageSpeechRecognition/video"
    model = "/model/haarcascade_frontalface_default.xml"
    #faceCascade = cv2.CascadeClassifier(model)
    faceCascade = cv2.CascadeClassifier(path + model)

    # Charger le classificateur cascade pour la détection de visages
    video_capture = cv2.VideoCapture(0)
    
    frame_width = int(video_capture.get(3))
    frame_height = int(video_capture.get(4))
    size = (frame_width, frame_height)

    ageNet,genderNet,ageList,genderList,MODEL_MEAN_VALUES = pretrained_age()

    record=False
    out= None

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Extract face ROI
        face = frame[y:y+h, x:x+w]
        
        # Preprocess the face ROI
        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        
        # Pass the face through the age and gender nets
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]
        
        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]
        
        # Draw age and gender labels on the frame
        label = "{}, {}".format(gender, age)
        cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)       

        #write video
        if record:
            if out is None:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"{current_time}.avi"                
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                out = cv2.VideoWriter(filename, fourcc, 10, size)
            out.write(frame)
        
        # Display the resulting frame
        st.image(frame, channels='BGR', use_column_width=True)

        key = cv2.waitKey(1) & 0xFF

        # Check if the 'q' key was pressed to exit the program
        if key == ord('q'):
            break
        # Check if the 'r' key was pressed to start recording
        if key == ord('r'):
            record = True
        # Check if the 's' key was pressed to stop recording
        if key == ord('s'):
            record = False
            if out is not None:
                out.release()
                out = None
    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

opencam()