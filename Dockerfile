FROM ubuntu:latest
RUN apt-get update -y --fix-missing
RUN apt-get install -y net-tools curl vim
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN pip install boto3

ADD stream-simu.py /stream-simu.py
RUN chmod u+x /stream-simu.py
CMD /stream-simu.py
