FROM python:3.6-alpine as base

FROM base as builder
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN apk add --no-cache \
    gcc g++ make linux-headers musl-dev libffi-dev postgresql-dev gmp-dev
RUN pip install --upgrade pip && pip --version && \
    pip install --target=/install -r /requirements.txt

FROM base
COPY --from=builder /install /usr/local/lib/python3.6
COPY --from=builder /usr/lib/libpq.so.5 /usr/lib/libldap_r-2.4.so.2 \
    /usr/lib/liblber-2.4.so.2 /usr/lib/libsasl2.so.3 /usr/lib/
RUN mkdir /code/
WORKDIR /code/
COPY . /code/
RUN python manage.py collectstatic
EXPOSE 8000
ENV PATH="/usr/local/lib/python3.6/bin/:${PATH}"
CMD ["daphne", "bdn.asgi:application", "-b", "0.0.0.0", "-p", "8000"]
