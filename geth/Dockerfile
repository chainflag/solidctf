FROM ethereum/client-go:v1.10.17

COPY genesis.json.template /genesis.json.template
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8545

ENTRYPOINT ["/entrypoint.sh"]
