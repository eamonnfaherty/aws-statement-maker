FROM python:2.7-alpine3.8

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY statement_maker.py /usr/src/app/

RUN chmod 777 /usr/src/app/statement_maker.py

ENTRYPOINT ["/usr/src/app/statement_maker.py"]