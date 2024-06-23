#Build Stage

FROM python:3.8.10-alpine AS builder
WORKDIR /app
COPY ./requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt && \
  rm ./requirements.txt
COPY . .
RUN python3 -m compileall .

# Deploy stage

#Could FROM scratch but couldn't create a gunicorn binary to copy
FROM python:3.8.10-alpine
#USER 1000:1000
LABEL authors="yossi"
EXPOSE 5000
WORKDIR /home/bonji/app
RUN mkdir -p /home/bonji/app/data && \
    chmod -R 755 /home/bonji/app
COPY --from=builder /app /home/bonji/app
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

ENV BG_COLOR=#f0f0f0

ENTRYPOINT ["gunicorn"]
CMD ["--workers", "3", "--bind", "0.0.0.0:5000", "wsgi:app"]

