# Use an official Python runtime as a parent image
FROM python:3.9-slim
ADD . /python-service

# Set the working directory to /python-service
WORKDIR /python-service

# Copy the current directory contents into the container at /python-service
COPY . /python-service

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "app.py"]