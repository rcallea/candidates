#
FROM python:3.10.9-slim

#
WORKDIR /code

#
RUN pip install --upgrade pip

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./src /code/src

#
CMD ["uvicorn", "src.application:app", "--host", "0.0.0.0", "--port", "8000"]