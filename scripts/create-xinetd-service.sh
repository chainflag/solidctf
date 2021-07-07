#!/bin/bash

cat <<EOF > /etc/xinetd.d/ctf
service ctf
{
    type            = UNLISTED
    flags           = NODELAY
    disable         = no
    socket_type     = stream
    protocol        = tcp
    wait            = no
    user            = root
    log_type        = FILE /var/log/ctf/xinetd.log
    log_on_success  = PID HOST EXIT DURATION
    log_on_failure  = HOST ATTEMPT
    port            = ${PORT}
    bind            = 0.0.0.0
    server          = /usr/local/bin/python3
    server_args     = /opt/main.py
    per_source      = ${PER_SOURCE:-4}
    cps             = ${CPS_RATE:-200} ${CPS_DELAY:-5}
    rlimit_cpu      = ${RLIMIT_CPU:-5}
}
EOF
