FROM python:3.7-alpine:3.8

COPY . .

RUN pip install -r ./requirement.txt

WORKDIR atd_test

CMD python -m unittest discover -v