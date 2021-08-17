# eth-challenge-base

xinetd docker for building ethereum contract challenge in CTF.

## Usage
* Implement the isSolved() function for your challenge contract by referring to the [example](https://github.com/chainflag/eth-challenge-base/blob/main/challenge/contracts/Greeter.sol#L20)
, and put it in [contracts directory](https://github.com/chainflag/eth-challenge-base/tree/main/challenge/contracts) to replace the `Greeter.sol`.

* Setup the [challenge.yml](https://github.com/chainflag/eth-challenge-base/blob/main/challenge/challenge.yml) value, including flag, banner, contract constructor args, etc.

>Tips:
you can run `python3 -c "import secrets; print(secrets.token_hex(32))"` to generate auth_token.secret

* Build Docker Image and run Docker Container, then you can `nc` to the challenge.
```bash
$ docker build -t eth-challenge .
$ docker run --env-file challenge/.env -d -p pub_port:20000 eth-challenge
$ nc [hostname] [port]
```
