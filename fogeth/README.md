# Fogeth
Fogeth is a private PoA Ethereum environment tailored for CTF challenges. It restricts access to only whitelisted RPC methods and cleans transaction data from `eth_getBlockByHash` and `eth_getBlockByNumber` responses. This prevents players from searching through blockchain history to find and copy others' transactions and solutions, thereby ensuring fairness in CTF challenges.

## Usage

### Clone the Repository

```
git clone https://github.com/chainflag/solidctf.git
cd solidctf/fogeth
```

### Configure the Node

To configure the node, make a copy of `.env.example` named `.env`, then open it with your preferred text editor and fill out the alloc address private key.

### Operating the Node

To start the node, run:

```bash
docker-compose up -d
```
To stop the node, use:

```bash
docker-compose down
```

### Open ports

| Service    | Port |
|------------|------|
| JSON-RPC   | 8545 |   
| eth-faucet | 8080 |
