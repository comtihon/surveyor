FROM continuumio/miniconda3

RUN mkdir /opt/surveyor
ADD . /opt/surveyor
WORKDIR /opt/surveyor
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["catcher", "script/tests"]