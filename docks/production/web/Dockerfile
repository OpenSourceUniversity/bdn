FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN apk add --no-cache gcc g++ make linux-headers musl-dev libffi-dev postgresql-dev gmp-dev
RUN pip install -r requirements.txt
ADD . /code/
EXPOSE 8000
CMD ["daphne", "bdn.asgi:application", "-b", "0.0.0.0", "-p", "8000"]
