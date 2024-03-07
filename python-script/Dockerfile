FROM python:3.9-slim

# Install cron
RUN apt-get update && apt-get install -y cron

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY script.py .
COPY crontab /etc/cron.d/my-cron-job

# Give execution rights on the cron job and script
RUN chmod 0644 /etc/cron.d/my-cron-job \
    && chmod +x script.py \
    && crontab /etc/cron.d/my-cron-job

# Create the log file to output cron log
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
