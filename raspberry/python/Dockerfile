# Step 1: Use an official Python runtime as a parent image
FROM python:latest

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container
COPY . /app

# Step 4: Create a virtual environment inside the container
RUN python -m venv raspberry_python_serial

# Step 5: Activate the virtual environment and install dependencies
RUN . raspberry_python_serial/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

# Step 6: Expose the port (if necessary, modify this if your app runs on a specific port)
EXPOSE 5000

# Step 7: Set the environment variable for the virtual environment activation (to make it active in subsequent commands)
ENV VIRTUAL_ENV=/app/raspberry_python_serial
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Step 8: Set the default command to run the Python app
CMD ["python3", "index.py"]
