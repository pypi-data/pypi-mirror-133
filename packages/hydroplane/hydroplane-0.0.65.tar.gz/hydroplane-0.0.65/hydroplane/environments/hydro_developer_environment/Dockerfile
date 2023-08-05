# FROM python:3.9.9-alpine3.14
# RUN apk update && apk --no-cache add postgresql-dev gcc python3-dev musl-dev curl gcc g++

FROM python:3.9.9

RUN pip3 install -r requirements.txt

COPY . /hydro_app 
WORKDIR /hydro_app   

# CMD hydro start -n "hydroPLANE" -p 8053
CMD python3 hydro_dashboard.py
# CMD gunicorn hydro_dashboard:hydro.server -b :8000