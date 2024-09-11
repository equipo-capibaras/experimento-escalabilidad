FROM python:3.12-alpine

# Set the working directory
WORKDIR /app

COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

EXPOSE 3030

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]