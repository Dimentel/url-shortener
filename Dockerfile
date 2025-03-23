FROM python:3.12

RUN mkdir /url-shortener

WORKDIR /url-shortener

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

CMD ["./docker/app.sh"]
#WORKDIR src

#CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000