FROM python:3.7

COPY requirements.txt . 

RUN pip3 install -r requirements.txt

COPY app.py .

EXPOSE 5002

ENTRYPOINT [ "gunicorn", "--workers=4" ,"--bind=0.0.0.0:5002", "app:app" ]