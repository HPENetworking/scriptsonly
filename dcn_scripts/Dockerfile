FROM ubuntu:latest
MAINTAINER Rick Kauffman "chewie@wookieware.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["views.py"]
