FROM python:alpine
MAINTAINER Benjamin Kampmann <benjamin.kampmann@bewegung.jetzt>
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=services.py
RUN mkdir /code
WORKDIR /code
ADD scripts/sync /code
RUN pip install -r requirements.txt
CMD flask run --host=0.0.0.0
