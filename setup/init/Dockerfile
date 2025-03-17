FROM python:3.9

WORKDIR /app

# Install dependencies if needed
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy scripts
COPY database-setup.py .
COPY init.sh .

# Make sure the entrypoint script is executable
RUN chmod +x init.sh

ENTRYPOINT ["./init.sh"]
