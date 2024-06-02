FROM ubuntu:latest
LABEL authors="imse"

ENTRYPOINT ["top", "-b"]