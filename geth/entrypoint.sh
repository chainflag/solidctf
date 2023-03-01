#!/bin/sh
set -eu

GETH_DATA_DIR=/data
GETH_CHAINDATA_DIR=$GETH_DATA_DIR/geth/chaindata
GETH_KEYSTORE_DIR=$GETH_DATA_DIR/keystore

CHAIN_ID="${CHAIN_ID:-$((RANDOM + 10000))}"

if [ ! -d "$GETH_KEYSTORE_DIR" ]; then
    echo "$GETH_KEYSTORE_DIR missing, running account import"
    echo -n "${BLOCK_SIGNER_PRIVATE_KEY_PASSWORD:-chainflag}" >"$GETH_DATA_DIR"/password
    echo -n "$BLOCK_SIGNER_PRIVATE_KEY" >"$GETH_DATA_DIR"/block-signer-key
    BLOCK_SIGNER_ADDRESS_WITHOUT_0X=$(geth account import \
        --datadir="$GETH_DATA_DIR" \
        --password="$GETH_DATA_DIR"/password \
        "$GETH_DATA_DIR"/block-signer-key | grep -oE '[[:xdigit:]]{40}')
    echo "geth account import complete"
fi

if [ ! -d "$GETH_CHAINDATA_DIR" ]; then
    echo "$GETH_CHAINDATA_DIR missing, running init"
    sed "s/\${CHAIN_ID}/$CHAIN_ID/g; s/\${BLOCK_SIGNER_ADDRESS_WITHOUT_0X}/$BLOCK_SIGNER_ADDRESS_WITHOUT_0X/g" /genesis.json.template >/genesis.json
    geth init --datadir="$GETH_DATA_DIR" /genesis.json
    echo "geth init complete"
fi

exec geth \
    --datadir="$GETH_DATA_DIR" \
    --password="$GETH_DATA_DIR"/password \
    --allow-insecure-unlock \
    --unlock="$BLOCK_SIGNER_ADDRESS_WITHOUT_0X" \
    --mine \
    --networkid="$CHAIN_ID" --nodiscover \
    --http --http.addr=0.0.0.0 --http.port=8545 \
    --http.api=eth,net,web3 \
    --http.corsdomain='*' --http.vhosts='*'
