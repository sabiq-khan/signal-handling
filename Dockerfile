# docker build . -t signal-handling-example
# CONTAINER_ID=$(docker run -d signal-handling-example)
# docker stop $CONTAINER_ID
# docker logs $CONTAINER_ID

FROM python:3.11.9-alpine
RUN mkdir /app/
WORKDIR /app/
COPY ./src/signal_handling_example/ .
ENTRYPOINT ["/usr/bin/env", "python3", "main.py"]
