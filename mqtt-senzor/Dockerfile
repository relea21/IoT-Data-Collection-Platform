FROM python:3.8-slim
WORKDIR /senzor
COPY . /senzor
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "senzor.py"]