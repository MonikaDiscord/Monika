FROM python

COPY requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt

ADD . /Monika

WORKDIR /Monika

CMD ["python3","/Monika/monika.py"]
