FROM python:3.11.9
COPY requierements.txt /app/requirements.txt
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uwsgi", "--ini", "uwsgi.ini"]
