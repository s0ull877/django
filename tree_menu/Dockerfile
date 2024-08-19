FROM python:3.10-slim

WORKDIR /app
COPY infra/requirements.txt .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
COPY app . 
RUN chmod +x start.sh
CMD ["/bin/bash", "-c", "./start.sh"]
