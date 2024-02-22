FROM python:3.10-alpine AS base

FROM base AS build

WORKDIR /hurdle-archive

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pymysql

FROM build AS runtime

WORKDIR /hurdle-archive

COPY app app
COPY migrations migrations
COPY db db
COPY config.py hurdle-archive.py entrypoint.sh ./
RUN chmod +x ./entrypoint.sh

ENV FLASK_APP hurdle-archive.py
EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
