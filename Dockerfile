FROM arm32v7/python:3.7.6-slim-stretch

####################################################################################################
# Install required libs for OpenCV
#
RUN  DEBIAN_FRONTEND=noninteractive  \
     apt-get -y update && \
     apt-get -y upgrade && \
     apt-get -yq install build-essential cmake pkg-config  \
                    libjpeg-dev libtiff5-dev libpng-dev  \
                    libavcodec-dev libavformat-dev libatlas-base-dev libswscale-dev libv4l-dev  \
                    libxvidcore-dev libx264-dev \
                    libatlas-base-dev gfortran \
                    python3-dev \
                    wget unzip


RUN mkdir /app
WORKDIR /app

RUN READTHEDOCS=True \
    pip3 install "picamera[array]" &&  \
    pip3 install numpy

####################################################################################################
# Download and compile OpenCV. I need to compile because the mp4 code is not part of the OpenCV distro per default
# I must compile with the "OPENCV_ENABLE_NONFREE" flag to get them
#
RUN cd ~  && \
    wget -O opencv.zip https://github.com/opencv/opencv/archive/4.2.0.zip && \
    wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.2.0.zip && \
    unzip opencv.zip && \
    unzip opencv_contrib.zip && \
    mv opencv-4.2.0 opencv && \
    mv opencv_contrib-4.2.0 opencv_contrib && \
    cd ~/opencv && \
    mkdir build && \
    cd build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
          -D CMAKE_INSTALL_PREFIX=/usr/local \
          -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
          -D ENABLE_NEON=ON \
          -D ENABLE_VFPV3=ON \
          -D BUILD_TESTS=OFF \
          -D INSTALL_PYTHON_EXAMPLES=OFF \
          -D OPENCV_ENABLE_NONFREE=ON \
          -D CMAKE_SHARED_LINKER_FLAGS=-latomic \
          -D BUILD_EXAMPLES=OFF ..  &&\
    make -j4 &&\
    make install &&\
    ldconfig

# Install helloworld
COPY ./src/ /app
COPY ./requirements.txt/ /app


# RUN pip install -r requirements.txt

CMD python main.py
