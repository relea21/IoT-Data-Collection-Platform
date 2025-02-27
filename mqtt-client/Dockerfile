FROM python:3.8-slim
WORKDIR /adaptor
COPY . /adaptor
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "adaptor.py"]