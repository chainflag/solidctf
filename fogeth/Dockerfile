FROM nginx:1.22-alpine

COPY proxy/eth-jsonrpc-access.js /etc/nginx
COPY proxy/nginx.conf /etc/nginx

COPY genesis.json.template /genesis.json.template
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY --from=ethereum/client-go:v1.10.26 /usr/local/bin/geth /usr/local/bin/

EXPOSE 8545

ENTRYPOINT ["/entrypoint.sh"]
