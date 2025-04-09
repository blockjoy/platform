FROM python:3.9

WORKDIR /app

# Install dependencies if needed
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy scripts
COPY test_roles_permissions.query .
COPY database-setup.py .

# Make sure the entrypoint script is executable
RUN chmod +x database-setup.py

CMD ["sleep", "initinity"]
