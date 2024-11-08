FROM python:3.12.2-alpine

WORKDIR /code
COPY ./requirement /code/requirement
RUN pip install --no-cache-dir --upgrade -r /code/requirement/local.txt

COPY ./src /code/src

EXPOSE 8080