# Fogeth
Fogeth is a private PoA Ethereum environment tailored for CTF challenges. It restricts access to only whitelisted RPC methods and cleans transaction data from `eth_getBlockByHash` and `eth_getBlockByNumber` responses. This prevents players from searching through blockchain history to find and copy others' transactions and solutions, thereby ensuring fairness in CTF challenges.

## Getting Started

### Clone the Repository

```
git clone https://github.com/chainflag/solidctf.git
cd solidctf/fogeth
```

### Start the Node
```bash
docker build -t chainflag/fogeth .
docker run -d -p 8545:8545 -e ALLOC_ADDRESS_PRIVATE_KEY="private key" chainflag/fogeth
```
