FROM python:3.9

RUN  apt-get update && apt-get install -y build-essential libssl-dev libffi-dev python-dev

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
CMD python ./main.py