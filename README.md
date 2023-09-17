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
docker run -it -p 20000:20000 -e WEB3_PROVIDER_URI=https://rpc.sepolia.org chainflag/solidctf:1.0
nc 127.0.0.1 20000
```

### Usage

1. Clone the [solidity-ctf-template](https://github.com/chainflag/solidity-ctf-template) using `git clone git@github.com:chainflag/solidity-ctf-template.git` command to create a new challenge project.
2. Open the contract directory and code your challenge contract that contains the [isSolved()](https://github.com/chainflag/solidity-ctf-template/blob/main/contracts/Example.sol#L19) to replace the example contract. For the multi-contract challenges, you can deploy them in a setup contract's constructor.
3. Edit the [challenge.yml](https://github.com/chainflag/solidity-ctf-template/blob/main/challenge.yml) to configure your challenge. See to the comments in this file for more details on how to configure it.
4. Place your flag in the file [flag.txt](https://github.com/chainflag/solidity-ctf-template/blob/main/flag.txt) file and change the alloc address private key in the [.env](https://github.com/chainflag/solidity-ctf-template/blob/main/.env) to your own.
5. Run the `docker-compose pull && docker-compose up -d` command to start serving your challenge.

## Development

### Prerequisites

Before you start, make sure you have the following installed:

* Docker
* Python3
* Required packages (`pip install -r requirements.txt`)

### Run in development mode
1. Clone the repository

```bash
git clone git@github.com:chainflag/solidctf.git
git submodule update --init --recursive
```

2. Generate protobuf code and run server

```bash
make protoc
export WEB3_PROVIDER_URI="your web3 provider"
make dev
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
