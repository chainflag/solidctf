import $ from 'jquery';
import { client } from 'twirpscript';
import hljs from 'highlight.js';
import hljsDefineSolidity from 'highlightjs-solidity';

import {
  GetChallengeInfo,
  GetSourceCode,
  GetFlag,
  NewPlayground,
  DeployContract,
} from '../challenge.pb.js';

import '../assets/style.css';

const API_PREFIX = '/api/twirp';
client.prefix = API_PREFIX;

hljsDefineSolidity(hljs);
hljs.initHighlightingOnLoad();

$(document).ready(async function () {
  try {
    const infoRes = await GetChallengeInfo({});
    $('#challenge-description').text(res.description);

    if (infoRes.solvedEvent.length === 0) {
      $('#input-text').hide();
    }

    if (infoRes.showSource) {
      const sourceRes = await GetSourceCode({});
      displaySource(sourceRes.source);
    }
  } catch (err) {
    $('#challenge-status').text(`API error: ${err.msg}`);
  }

  let token = localStorage.getItem('token');
  if (!token) {
    try {
      const startRes = NewPlayground({});
      localStorage.setItem('token', startRes.token);
      const msg = `please transfer more than ${startRes.value.toFixed(
        3
      )} test ether to the deployer account ${startRes.address} for next step`;
      $('#challenge-status').text(msg);
    } catch (err) {
      $('#challenge-status').text(
        `NewPlayground failed, contact admin: ${err.msg}`
      );
    }
    return;
  }

  if (!localStorage.getItem('target')) {
    try {
      const deployRes = await DeployContract(
        {},
        { headers: { authorization: token } }
      );
      const target = deployRes.address;
      localStorage.setItem('target', target);
      $('#challenge-status').text('please solve the contrat @' + target);
    } catch (err) {
      console.log(err);
      $('#challenge-status').text(err.msg);
    }
  } else {
    const target = localStorage.getItem('target');
    $('#challenge-status').text('please solve the contrat @' + target);
  }

  $('#get-flag').click(getFlag);
});

function displaySource(source) {
  for (const filename in source) {
    const content = source[filename];
    const card = $('<div>').addClass('card');
    const pre = $('<pre>');
    const code = $('<code>')
      .addClass('language-solidity')
      .css({
        'font-weight': 'bold',
        'font-family': 'Cascadia Mono, monospace',
      })
      .text(content);
    pre.append(code);
    card.append(pre);
    $('#target-element').append(card);
  }
  hljs.highlightAll();
}

function getFlag() {
  try {
    const solve_tx_hash = document.getElementById('input-text').value;
    const token = localStorage.getItem('token');
    const res = GetFlag(
      { txHash: solve_tx_hash },
      { headers: { authorization: token } }
    );
    console.log(res);
    if ('flag' in res) {
      $('#flag-placeholder').text(`🥰🥰🥰 ${res.flag}`);
    }
  } catch (err) {
    $('#flag-placeholder').text(err.msg);
  }
}
