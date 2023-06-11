# Use an official Kali Linux runtime as a parent image
FROM kalilinux/kali-rolling

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system packages
RUN apt-get update && apt-get install -y default-libmysqlclient-dev python3 python3-pip

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Install Python libraries
RUN pip3 install mysqlclient

# Copy project
COPY . /code/

# Run Django management commands
RUN source /env/bin/activate
RUN chmod +x /code/DBSF/Scripts/setup.sh
RUN /code/DBSF/Scripts/setup.sh
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate