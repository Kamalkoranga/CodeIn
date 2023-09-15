FROM python:3.11-alpine
WORKDIR /usr/src/codehub
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN python3 -m venv env
COPY . .
RUN env/bin/pip install --upgrade pip
RUN env/bin/pip install -r requirements.txt
RUN cat .env
RUN chmod +x boot.sh
ENV FLASK_APP codein.py
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]