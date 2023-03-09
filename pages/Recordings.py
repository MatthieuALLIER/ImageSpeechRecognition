import threading
import speech_recognition as sr
import io
import contextlib
from pynput.keyboard import Controller
import cv2
import datetime
import streamlit as st
import os

#st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
st.set_page_config(page_title='SL', page_icon=':guardsman:', layout='wide', initial_sidebar_state="auto", menu_items=None)

#SAM BEGIN#
#to store the videos
#create a tab to store recordings
video_dir = "C:/Users/ibtis/OneDrive/Documents/GitHub/ImageSpeechRecognition/"

video_files = [f for f in os.listdir(video_dir) if f.endswith('.avi')]

with st.sidebar:
    st.title("Recordings")
    selected_file = st.radio("Select a video file:",video_files)
    #st.write("Select a video file:",video_files)

# display the selected video file in the main Streamlit app area
#st.video(os.path.join(video_dir,selected_file))
#st.write(video_dir,selected_file)
#st.write(video_dir)
#st.write(selected_file)
               
#st.video("C:/Users/ibtis/OneDrive/Documents/GitHub/ImageSpeechRecognition/2023-03-08_15-59-55.avi")



# Open the video file
#cap = cv2.VideoCapture("C:/Users/ibtis/OneDrive/Documents/GitHub/ImageSpeechRecognition/2023-03-08_15-59-55.avi")

#gives images , si on veut des captures de la vidéo enregistrée

# Check if the video file was successfully opened
#if not cap.isOpened():
 #   st.write("Error opening video file")
#else:
    # Read the first frame of the video
    #ret, frame = cap.read()

    # Display the video frame-by-frame
    #while ret:
        # Convert the frame from BGR to RGB format
        #frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Display the frame in the Streamlit app
        #st.image(frame_rgb, channels="RGB")

        # Read the next frame
        #ret, frame = cap.read()


# import subprocess

# input_file = "C:/Users/ibtis/OneDrive/Documents/GitHub/ImageSpeechRecognition/2023-03-08_15-59-55.avi"
# output_file = "C:/Users/ibtis/OneDrive/Documents/GitHub/ImageSpeechRecognition/converted_video_py.mp4"

# cmd = ['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-crf', '23', '-c:a', 'aac', '-b:a', '128k', '-preset', 'slow', '-b:v', '5000k', output_file]

# subprocess.run(cmd)

#works with mp4 videos
video_file = open('C:/Users/ibtis/OneDrive/Documents/GitHub/ImageSpeechRecognition/2023-03-08_15-59-55.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes)

from moviepy.editor import VideoFileClip

input_file = "C:/Users/ibtis/OneDrive/Documents/GitHub/ImageSpeechRecognition/2023-03-08_15-59-55.avi"
output_file = "C:/Users/ibtis/OneDrive/Documents/GitHub/ImageSpeechRecognition/converted_video_py.mp4"

clip = VideoFileClip(input_file)
clip.write_videofile(output_file)




# import subprocess

# # Define the input and output file paths
# input_file = "C:/Users/ibtis/OneDrive/Documents/GitHub/ImageSpeechRecognition/2023-03-08_15-59-55.avi"
# output_file = "C:/Users/ibtis/OneDrive/Documents/GitHub/ImageSpeechRecognition/converted_video.mp4"

# Use ffmpeg to convert the video format
#subprocess.call(['ffmpeg', '-i', input_file, '-vcodec', 'libx264', '-acodec', 'aac', output_file])


#os.popen("ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}.mp4'".format(input = input_file, output = output_file))

from moviepy.editor import VideoFileClip
import os

# input_file = "C:/Users/ibtis/OneDrive/Documents/GitHub/ImageSpeechRecognition/2023-03-08_15-59-55.avi"
# output_file = "C:/Users/ibtis/OneDrive/Documents/GitHub/ImageSpeechRecognition/converted_video_py.mp4"

# clip = VideoFileClip(input_file)
# fps = 25#clip.fps
# clip.close()

# clip = VideoFileClip(input_file)
# clip.write_videofile(output_file, fps=fps, codec='libx264')
# clip.close()


#conversion which works, we should convert the avi video to mp4, that we get from the recording vocal command
from moviepy.editor import VideoFileClip

input_file = "C:/Users/ibtis/OneDrive/Documents/GitHub/ImageSpeechRecognition/2023-03-08_15-59-55.avi"
output_file = "C:/Users/ibtis/OneDrive/Documents/GitHub/ImageSpeechRecognition/converted_video_py.mp4"

clip = VideoFileClip(input_file)
clip.write_videofile(output_file, fps=30, verbose=True, codec='mpeg4')
#SAM END#