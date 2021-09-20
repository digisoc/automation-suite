# Python base image
FROM python:3.9-slim

# Upgrade pip
RUN pip install --upgrade pip

# Set up non-root permissions
RUN adduser --disabled-login worker
USER worker
ENV PATH="/home/worker/.local/bin:${PATH}"

# Set working directory
WORKDIR /home/worker/digibot

# Install pip dependencies
COPY --chown=worker:worker requirements.txt requirements.txt
run pip install --user -r requirements.txt

# Copy files to working directory
COPY --chown=worker:worker . .

# Copy environment variables from .env
CMD env

# Start server
# RUN python main.py
ENTRYPOINT ["python"]
CMD ["main.py"]
