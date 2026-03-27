FROM ubuntu:latest
LABEL authors="senpaka"

ENTRYPOINT ["top", "-b"]