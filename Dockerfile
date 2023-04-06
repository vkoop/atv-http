FROM python:3.12.0a7

RUN  apt-get update && apt-get install -y build-essential libssl-dev libffi-dev python-dev

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 8080
CMD python -u ./main.py