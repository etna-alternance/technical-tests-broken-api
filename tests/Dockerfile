FROM python:3.9-slim-buster
WORKDIR /tests
COPY requirements.txt /tests/requirements.txt
RUN pip3 install --no-cache-dir -r /tests/requirements.txt
COPY . /tests/
CMD tail -f /dev/null
