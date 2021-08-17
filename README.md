# eth-challenge-base

xinetd docker for building ethereum contract challenge in CTF.

## Usage
* Implement the isSolved() function for your challenge contract by referring to the [example](https://github.com/chainflag/eth-challenge-base/blob/main/challenge/contracts/Greeter.sol#L20)
, and put it in [contracts directory](https://github.com/chainflag/eth-challenge-base/tree/main/challenge/contracts) to replace the `Greeter.sol`.

* Set up the [challenge.yml](https://github.com/chainflag/eth-challenge-base/blob/main/challenge/challenge.yml) value, including flag, banner, contract constructor args, etc.

* Build Docker Image and run Docker Container, then you can `nc` to the challenge.
```bash
$ docker build -t my-eth-challenge .
$ docker run -it -d -p pub_port:20000 \
-e TOKEN_SECRET=secret \
-e TOKEN_EXP_SECONDS=7200 \
-e WEB3_PROVIDER_URI=uri \
my-eth-challenge
$ nc [hostname] [port]
```

>Tips:
you can run `python3 -c "import secrets; print(secrets.token_hex(32))"` to generate TOKEN_SECRET
