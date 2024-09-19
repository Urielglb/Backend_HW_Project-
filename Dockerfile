FROM python:3.12

WORKDIR /code

COPY ./requirements.txt .

EXPOSE 8000

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]