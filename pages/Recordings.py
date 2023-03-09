import streamlit as st
import os

#st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
st.set_page_config(page_title='SL', page_icon=':guardsman:', layout='wide', initial_sidebar_state="auto", menu_items=None)

#SAM BEGIN#
#to store the videos
#create a tab to store recordings
video_files = [f for f in os.listdir() if f.endswith('.mp4')]

with st.sidebar:
    st.title("Recordings")
    selected_file = st.radio("Select a video file:", video_files)
    #st.write("Select a video file:",video_files)


video_file=open(f'{selected_file}','rb')
video_bytes = video_file.read()

st.video(video_bytes)

