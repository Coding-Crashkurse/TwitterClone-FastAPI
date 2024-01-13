FROM python:3.10

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5555"]