pb.GetChallengeInfo().then(res => {
    $('#challenge-description').text(res.description);
    if (res.showSource == true) {
        pb.GetSourceCode().then(res => {
            for (const filename in res.source) {
                var content = res.source[filename];
                var card = $('<div>');
                card.addClass('card');
                var pre = $('<pre>');
                var code = $('<code>');
                code.addClass('language-solidity');
                code.css('font-weight', 'bold');
                code.css('font-family', 'Cascadia Mono, monospace');
                code.text(content);
                pre.append(code);
                card.append(pre);
                $('#target-element').append(card);
            }
            hljs.highlightAll();
        });
    }
    if (res.solvedEvent.length === 0) {
        $('#input-text').hide();
    }
});

if (localStorage.getItem('token') === null) {
    pb.NewPlayground().then(res => {
        localStorage.setItem('token', res.token);
        var msg = `please transfer more than ${res.value.toFixed(3)} test ether to the deployer account ${res.address} for next step`
        $('#challenge-status').text(msg);
    }).catch(err => { $('#challenge-status').text(`NewPlayground failed, contact admin: ${err.msg}`); })
} else {
    var token = localStorage.getItem('token');
    if (localStorage.getItem('target') === null) {
        pb.DeployContract({}, { headers: { authorization: token } })
        .then(res => {
            var target = res.address;
            localStorage.setItem('target', target);
            $('#challenge-status').text('please solve the contrat @' + target);
        })
        .catch(err => {
            console.log(err);
            $('#challenge-status').text(err.msg);
        })
    } else {
        var target = localStorage.getItem('target');
        $('#challenge-status').text('please solve the contrat @' + target);
    }
}

function submit_tx() {
    var solve_tx_hash = document.getElementById('input-text').value;
    pb.GetFlag({ txHash: solve_tx_hash }, { headers: { authorization: token } })
    .then(res => {
        console.log(res);
        if ('flag' in res) {
            $('#flag-placeholder').text(`🥰🥰🥰 ${res.flag}`);
        }
    })
    .catch(err => { $('#flag-placeholder').text(err.msg); });
};

function clean_local() {
    localStorage.clear();
    window.location.reload();
}