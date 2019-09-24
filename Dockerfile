FROM python:3

WORKDIR .

ENV FLASK_APP run.py

ENV DB_URI mysql:///site.db

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE $PORT

CMD gunicorn --bind 0.0.0.0:$PORT run:app
