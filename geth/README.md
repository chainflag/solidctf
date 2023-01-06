# Private PoA Ethereum Network for CTF Challenges

The solution is to use [Nginx](https://www.nginx.com/) as a reverse proxy and set up the whitelist of Ethereum RPC methods by using [njs](https://nginx.org/en/docs/njs/) for access control to the upstream private Proof-of-Authority Ethereum network, and thus implement an anti-plagiarism server-side environment.

## Background

It is unfair that some CTF blockchain challenge players can cheat by searching back the blockchain history, where all the transactions of those who have solved the challenges are recorded. These dishonest players can solve the challenges simply by replaying the transactions. The root cause of this problem is that all data in the permissionless blockchain is public and everyone can fetch it by querying the specified RPC methods.  

So the idea of this project is to disable several RPC methods (e.g. `eth_getBlockByHash`, `eth_getBlockByNumber`) of an Ethereum node and then use it as the challenge server-side environment. In this way, players on the client side have no longer any access to the transaction IDs of others. 

## Usage

### Clone the Repository

```
git clone https://github.com/chainflag/eth-challenge-base.git
cd eth-challenge-base/geth
```

### Configure the Node

Make a copy of `.env.example` named `.env`.

```bash
cp .env.example .env
```

Open `.env` with your editor of choice and fill out the environment variables listed inside that file.

### Operating the Node

#### Start

```bash
docker-compose up -d
```
#### Stop

```bash
docker-compose down
```

#### Open Ports

| Service                 | Port |
|-------------------------|------|
| json-rpc with whitelist | 8545 |   
| ether faucet            | 8080 |
