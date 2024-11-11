FROM python:3.12.2-alpine

WORKDIR /jares
COPY ./requirement /jares/requirement
RUN pip install --no-cache-dir --upgrade -r /jares/requirement/prod.txt

COPY ./src /jares/src

EXPOSE 8080