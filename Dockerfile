MAINTAINER Benjamin Kampmann <benjamin.kampmann@bewegung.jetzt>
FROM python:alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD scripts/sync /code
RUN pip install -r requirements.txt