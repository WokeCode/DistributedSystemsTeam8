# Using official python runtime base image
FROM python:3.10

# Set the app directory
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements to container and install
#COPY requirements.txt requirements.txt
#RUN pip install -r requirements.txt
 RUN pip3 install aiohttp==3.6.2 &&\
    pip3 install requests==2.31.0
# Upgrade pip
RUN pip install --upgrade pip

# Copy all to current dir
COPY . .

# Make port 8080 available for api
EXPOSE 8080

# This will print python logs to output
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8

# Define the command to be run when launching the container
CMD ["python", "-u", "./app.py"]