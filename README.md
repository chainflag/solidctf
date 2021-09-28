# eth-challenge-base

xinetd docker for building ethereum contract challenge in capture the flag (CTF).

## Getting Started

### Quick Demo

```bash
docker run -it -p 20000:20000 -e WEB3_PROVIDER_URI=uri chainflag/eth-challenge-base
nc 127.0.0.1 20000
```

### Build Challenge

Create challenge project based on [example](https://github.com/chainflag/eth-challenge-base/tree/main/example)
* `contracts` is a directory used to store challenge contract, you should code isSolved() function for the contract to check if it is solved
* `chall.env` is for setting environment variables of docker container, including web3 provider, token secret and token expiration seconds
* `info.yaml` is config info regarding the contract challenge, you can specify challenge description, flag, contract name, etc. in this file

**Environment variable defaults**

| Name              | Default Value
| ----------------- | ----------------------------------
| TOKEN_SECRET      | random by `secrets.token_hex(32)`      
| TOKEN_EXP_SECONDS | None(non-expiring)
| WEB3_PROVIDER_URI | http://localhost:8545

Start serving your contract challenge
```bash
bash start.sh
```

## License

Distributed under the MIT License. See LICENSE for more information.

## Acknowledgements

* https://github.com/eth-brownie/brownie
* https://github.com/hitcxy/blockchain_template
* https://github.com/paradigm-operations/paradigm-ctf-2021
