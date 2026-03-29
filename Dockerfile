FROM python:3.12-slim
LABEL authors="senpaka"

ENTRYPOINT ["top", "-b"]