FROM python:3.7

COPY requirements.txt . 

RUN pip3 install -r requirements.txt

COPY app.py .

EXPOSE 5003

ENTRYPOINT [ "gunicorn", "--workers=4" ,"--bind=0.0.0.0:5003", "app:app" ]