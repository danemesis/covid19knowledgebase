FROM python:3.8.1

LABEL Author="Vladimir Kovalenko"
LABEL E-mail="proladge@gmail.com"
LABEL version="1.0.0"

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_ENV "development"
# ENV FLASK_DEBUG True
ARG PORT
ENV PORT ${PORT:-5000}

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD flask run --host=0.0.0.0 --port=$PORT