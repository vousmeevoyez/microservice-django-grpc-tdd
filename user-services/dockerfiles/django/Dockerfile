FROM python:3.7 AS base
ARG dependencies=requirements
ENV dependencies=${dependencies}
COPY ./requirements /requirements
RUN pip install -r /requirements/${dependencies}.txt
WORKDIR /app
COPY . /app

# second stage build
FROM python:3.7-slim AS release
RUN apt-get update && apt-get install make
ARG dependencies=requirements
ENV dependencies=${dependencies}
COPY --from=base /app/requirements/ ./
COPY --from=base /root/.cache /root/.cache
RUN pip install -r ${dependencies}.txt
COPY --from=base /app ./
COPY ./dockerfiles/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
