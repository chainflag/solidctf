# eth-challenge-base

xinetd docker for building ethereum contract challenge in CTF.

## Getting Started

* Quick demo with [example](https://github.com/chainflag/eth-challenge-base/tree/main/_example) challenge
```bash
$ docker run -d -p pub_port:20000 -e WEB3_PROVIDER_URI=uri chainflag/eth-challenge-base
$ nc [hostname] [port]
```

* Serving your own contract challenge
```bash
$ docker run -d -p pub_port:20000 -e WEB3_PROVIDER_URI=uri -v `pwd`/contracts:/home/ctf/contracts -v `pwd`/challenge.yml:/home/ctf/challenge.yml chainflag/eth-challenge-base
```

## Documentation

See details in https://github.com/chainflag/eth-challenge-base/wiki

## License

This project is licensed under the MIT License
