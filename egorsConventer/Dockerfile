FROM python:3.11.4

WORKDIR /app

COPY function.py .
COPY models ./models
COPY temp ./temp

RUN pip install --upgrade pip
RUN pip install pillow && pip install tensorflow &&  pip install keras

CMD ["python", "function.py"]
