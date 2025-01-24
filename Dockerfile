# Use an official base image
#FROM #<put this image here> https://hub.docker.com/layers/library/python/3.10.13-slim/images/sha256-842b562f35aa0809773044fe8c2266544f3d32ec6afc6af26b85d3e40ddab1d4?context=explore

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Install necessary packages
# use apt to install tesseract-ocr in this container
# see instructions here: https://tesseract-ocr.github.io/tessdoc/Installation.html
# RUN apt-get update # <your code here> #Checkout documentation on RUN here: https://docs.docker.com/engine/reference/builder/#run

RUN apt-get -y install poppler-utils ffmpeg libsm6 libxext6 && \ 
    pip3 --no-cache-dir install --upgrade pip && \ 
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY /src /app
COPY requirements.txt /app

# Set the working directory
WORKDIR /app

# Install with pip any needed packages specified in requirements.txt
# RUN <insert your code here>

# Run the script
# CMD ["python", <insert your arguments here>] #Checkout documentation on CMD here: https://docs.docker.com/engine/reference/builder/#cmd

