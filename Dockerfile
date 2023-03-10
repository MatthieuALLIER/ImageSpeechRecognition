FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
	python3-dev \
	flac \
	python-dev \
	python3-pip \
	cmake \ 
	portaudio19-dev \
	python3-pyaudio
	
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt ./requirements.txt

RUN pip3 install -U pip
RUN pip3 install -U wheel
RUN pip3 install -U setuptools
RUN pip3 install -r requirements.txt
RUN pip3 install dlib

COPY app.py app.py
COPY model ./app/model
COPY pages ./app/pages
COPY photos_featured ./app/photos_featured
COPY photos_trained ./app/photos_trained
COPY photos_trained ./app/photos_trained

COPY utils.py utils.py
COPY add_photos.py add_photos.py
COPY video_detection.py video_detection.py

CMD ["streamlit", "run", "app.py"]