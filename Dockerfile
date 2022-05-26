FROM python:3.9-slim-buster
#Permet d'executer une commande linux
RUN apt-get update              
RUN apt-get -y install gcc
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt
COPY . /app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
