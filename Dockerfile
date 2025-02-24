# Use the official Python 3.13 image from the Docker Hub
FROM python:3.13

# Update apt and install git and bash
RUN apt-get update 
RUN apt-get full-upgrade -y
RUN apt-get install -y git bash tzdata

# Set the timezone
ARG TZ
ENV TZ=${TZ:-"UTC"}

# Set the working directory in the container
RUN mkdir -p /app
WORKDIR /app

# Copy requirements file to the container
COPY ./requirements.txt .

# Install the dependencies
RUN python3 -m pip install -r requirements.txt --no-cache-dir

# Copy the rest of the files to the container
COPY . .
