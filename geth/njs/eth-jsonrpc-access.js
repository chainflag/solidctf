function access(r) {
  r.headersOut["Content-Type"] = "application/json";
  try {
    var payload = JSON.parse(r.requestBody);
  } catch (error) {
    r.return(415, createErrorResponse(-32700, "Parse error", null));
  }

  var errorResponse = validateMethod(payload);
  if (errorResponse) {
    r.return(401, errorResponse);
  }

  r.internalRedirect("@jsonrpc", function (response) {
    r.return(200, clearBlockTransactions(payload.method, response));
  });
}

function createErrorResponse(code, message, id) {
  return JSON.stringify({
    jsonrpc: "2.0",
    error: {
      code,
      message,
    },
    id,
  });
}

function validateMethod(payload) {
  var whitelist = [
    "eth_blockNumber",
    "eth_call",
    "eth_chainId",
    "eth_estimateGas",
    "eth_gasPrice",
    "eth_getBalance",
    "eth_getBlockByNumber",
    "eth_getCode",
    "eth_getStorageAt",
    "eth_getTransactionByHash",
    "eth_getTransactionCount",
    "eth_getTransactionReceipt",
    "eth_sendRawTransaction",
    "net_version",
    "rpc_modules",
    "web3_clientVersion",
  ];

  if (
    Object.keys(payload).filter((key) => key.toLowerCase() === "method")
      .length !== 1
  ) {
    return createErrorResponse(-32600, "Invalid request", payload.id);
  }

  if (!whitelist.includes(payload.method)) {
    return createErrorResponse(-32004, "Method not supported", payload.id);
  }
}

function clearBlockTransactions(method, response) {
  if (method !== "eth_getBlockByNumber") {
    return response;
  }

  var data = JSON.parse(response);
  if (data.result) {
    data.result.transactions = [];
  }
  return JSON.stringify(data);
}

export default { access };
