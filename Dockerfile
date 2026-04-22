FROM alpine:3.19

RUN apk add --no-cache curl python3 dcron

WORKDIR /app
COPY github-trending-daily.py .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
