# eth-challenge-base

![Docker CI](https://img.shields.io/github/workflow/status/chainflag/eth-challenge-base/Docker%20Image%20CI/main)
![Docker size](https://badgen.net/docker/size/chainflag/eth-challenge-base/latest?color=cyan)
![Latest tag](https://badgen.net/github/tag/chainflag/eth-challenge-base)
![License: MIT](https://badgen.net/github/license/chainflag/eth-challenge-base?color=yellow)

xinetd docker for building ethereum contract challenges in capture the flag (CTF).

## Getting Started

### Quick Demo

```bash
docker run -it -p 20000:20000 -e WEB3_PROVIDER_URI=https://ropsten.infura.io/v3/YOUR-PROJECT-ID chainflag/eth-challenge-base
nc 127.0.0.1 20000
```

## Usage

### Create challenge project based on [example](https://github.com/chainflag/eth-challenge-base/tree/main/example)
* `contracts` is the challenge contract directory, you should code [isSolved()](https://github.com/chainflag/eth-challenge-base/blob/main/example/contracts/Example.sol#L18) function for the contract to check if it is solved
* `challenge.yml` is the config for specifying challenge description, flag, contract name, constructor, gas limit etc. See comments in this file for more detail
* `.env` is used to set environment variables of docker container, including web3 provider, token secret and proof of work difficulty

**Environment variable defaults**

| Name              | Default Value
| ----------------- | ----------------------------------
| TOKEN_SECRET      | [openssl rand](https://github.com/chainflag/eth-challenge-base/blob/main/entrypoint.sh#L16)
| POW_DIFFICULTY    | 0(no proof of work)

>You can build multi-contract challenges by deploying contracts in a setup contract's constructor

### Start serving your contract challenge
```bash
docker run -d -p 20000:20000 --env-file .env -v `pwd`/contracts:/home/ctf/contracts -v `pwd`/challenge.yml:/home/ctf/challenge.yml chainflag/eth-challenge-base:0.9.3
```

or

```bash
docker-compose up -d
```

## Advance

### Use private PoA Ethereum network as challenge environment
1. Launch an anti-plagiarism PoA network by referring [here](https://github.com/chainflag/eth-challenge-base/tree/main/geth)
2. Keep the web3 provider defaults in the `.env` file
3. Run the docker container using the following command
```bash
docker run -d -p 20000:20000 --network geth_default --env-file .env -v `pwd`/contracts:/home/ctf/contracts -v `pwd`/challenge.yml:/home/ctf/challenge.yml chainflag/eth-challenge-base:0.9.3
```

## Development

### Prerequisites
* Python3
* Packages
```bash
pip install -r requirements.txt
```

### Run in dev mode
```bash
python develop.py
```

### Format python source
```bash
pip install -r requirements-dev.txt
make format
```

## License

Distributed under the MIT License. See LICENSE for more information.

## Acknowledgements

* https://github.com/eth-brownie/brownie
* https://github.com/hitcxy/blockchain_template
* https://github.com/paradigm-operations/paradigm-ctf-2021
* https://github.com/balsn/proof-of-work
