FROM python:3.11
WORKDIR /fastapi_app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN chmod a+x docker/*.sh
CMD [ "/fastapi_app/docker/app.sh" ]