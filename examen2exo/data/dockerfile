FROM python:3.11-slim

WORKDIR /app
COPY backend.txt /app/

RUN pip install -r backend.txt

COPY app.py /app/
RUN pip install -r backend.txt
CMD ["python","app.py"]