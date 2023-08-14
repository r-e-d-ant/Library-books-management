FROM python:latest

COPY . /ws
RUN cd /ws && pip install -r requirements.txt

WORKDIR /ws
EXPOSE 5000
CMD python3 run.py
