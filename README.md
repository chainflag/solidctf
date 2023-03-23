# SolidCTF

![Docker CI](https://img.shields.io/github/actions/workflow/status/chainflag/solidctf/docker-image.yml?branch=main)
![Docker size](https://badgen.net/docker/size/chainflag/solidctf/latest?color=cyan)
![Latest tag](https://badgen.net/github/tag/chainflag/solidctf)
![License: MIT](https://badgen.net/github/license/chainflag/solidctf?color=yellow)

SolidCTF is an infrastructure solution that simplifies the build of Solidity Capture the Flag (CTF) challenges. It provides the ability to CTF organizers to rapidly set up a playable Solidity CTF environment, freeing them up to concentrate on designing smart contracts for puzzles.

## Getting Started

### Quick Demo

Use the following command to run a quick demo:

```bash
docker run -it -p 20000:20000 -e WEB3_PROVIDER_URI=https://rpc.sepolia.org chainflag/eth-challenge-base
nc 127.0.0.1 20000
```

## Usage

### Create challenge project based on [example](https://github.com/chainflag/solidctf/tree/main/example)
* The `contracts` directory is where you should code the challenge contract, specifically, you need to implement [isSolved()](https://github.com/chainflag/solidctf/blob/main/example/contracts/Example.sol#L18) function to check if it is solved.
* The `challenge.yml` file is the config for specifying challenge description, flag, contract name, constructor, gas limit etc. Refer to the comments in this file for more details.
* The `.env` file is used to set environment variables of docker container, including web3 provider, token secret and proof of work difficulty.

>You can build multi-contract challenges by deploying contracts in a setup contract's constructor

### Start serving your contract challenge

Use the following command to start serving the contract challenge:
```bash
docker run -d -p 20000:20000 --env-file .env -v `pwd`/contracts:/home/ctf/contracts -v `pwd`/challenge.yml:/home/ctf/challenge.yml chainflag/eth-challenge-base:0.9.3
```

Alternatively, you can use docker-compose:

```bash
docker-compose up -d
```

## Advance

### Use private PoA Ethereum network as challenge environment
1. Launch an anti-plagiarism PoA network by following the instructions [here](https://github.com/chainflag/solidctf/tree/main/fogeth).
2. Keep the web3 provider defaults in the `.env` file.
3. Run the docker container using the following command:
```bash
docker run -d -p 20000:20000 --network fogeth_default --env-file .env -v `pwd`/contracts:/home/ctf/contracts -v `pwd`/challenge.yml:/home/ctf/challenge.yml chainflag/eth-challenge-base:0.9.3
```

## Development

### Prerequisites

Before you start, make sure you have the following installed:

* Docker
* Python3
* Required packages (`pip install -r requirements.txt`)

### Run in development mode
1. Generate protobuf code and run server

```bash
make protoc
export WEB3_PROVIDER_URI="your web3 provider"
make dev
```

2. Open another terminal to run client

```bash
python client.py
```

### Format python source

To format the Python source code, you will need to install additional packages (`pip install -r requirements-dev.txt`) and run the following command:

```bash
make format
```

## Acknowledgements
Many thanks to [JetBrains](https://jb.gg/OpenSourceSupport) for providing their excellent tools and an open source license to support the development of this project.

## License

Distributed under the MIT License. See LICENSE for more information.
