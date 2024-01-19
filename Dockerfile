FROM python:3.12.1-bookworm

RUN  apt-get update  \
     && apt-get install -y build-essential libssl-dev libffi-dev \
     && apt-get clean \
     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 8080
CMD python -u ./main.py