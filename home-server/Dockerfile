FROM python:3.10-slim
WORKDIR /app
COPY ./home_infra/requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir
COPY ./home .
RUN chmod +x start.sh
CMD ["./start.sh"]