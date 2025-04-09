FROM golang:1.23.1 AS go-builder

RUN go install github.com/caddyserver/xcaddy/cmd/xcaddy@latest && \
    cd / && \
    xcaddy build --with github.com/caddy-dns/cloudflare@1fb64108d4debf196b19d7398e763cb78c8a0f41 --with github.com/blockjoy/request-decompressor

FROM caddy:2-alpine

COPY --from=go-builder /caddy /usr/bin/caddy
COPY ./Caddyfile /etc/caddy/
