FROM python:3

ADD requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

ADD . /code

ENTRYPOINT [ "python3", "/code/main.py" ]

