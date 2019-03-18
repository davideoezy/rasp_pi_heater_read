FROM jfloff/alpine-python:3.6-onbuild 
COPY requirements.txt /tmp 
WORKDIR /tmp 
RUN pip install -r requirements.txt 
WORKDIR /.
ADD observations_polling.py /
CMD [ "python", "./observations_polling.py" ]