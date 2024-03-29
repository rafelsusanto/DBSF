# Use an official Kali Linux runtime as a parent image
FROM kalilinux/kali-rolling

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system packages
RUN apt-get update && apt-get install -y default-libmysqlclient-dev python3 python3-pip nmap sqlmap hydra python3-scapy odat 
#RUN apt-get install -y kali-linux-headless


# Set work directory
WORKDIR /code
#RUN /bin/bash -c "source /DBSF/env/bin/activate"

# Install dependencies
COPY requirements.txt /code/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Install Python libraries
#RUN pip3 install mysqlclient colorlog termcolor pycrypto passlib python-libnmap alien python3-pip cx_Oracle
#RUN pip3 install argcomplete && sudo activate-global-python-argcomplete
# Copy project
COPY . /code/

# Run Django management commands
#RUN python3 /code/DBSF/src/manage.py makemigrations
#RUN python3 /code/DBSF/src/manage.py migrate