import os
from dataclasses import dataclass
from typing import Optional

import aiohttp
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


@dataclass
class RPCError:
    code: int
    message: str


PARSE_ERROR = RPCError(code=-32700, message="Parse error")
INVALID_REQUEST = RPCError(code=-32600, message="Invalid request")
METHOD_NOT_SUPPORTED = RPCError(code=-32004, message="Method not supported")
RESULT_UNAVAILABLE = RPCError(code=-32002, message="Resource unavailable")

ALLOWED_METHODS = frozenset(
    [
        "eth_blockNumber",
        "eth_call",
        "eth_chainId",
        "eth_estimateGas",
        "eth_feeHistory",
        "eth_gasPrice",
        "eth_getBalance",
        "eth_getBlockByHash",
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
    ]
)


def error_response(error: RPCError, status_code: int, request_id: Optional[int] = None):
    return JSONResponse(
        content={
            "jsonrpc": "2.0",
            "error": {
                "code": error.code,
                "message": error.message,
            },
            "id": request_id,
        },
        status_code=status_code,
    )


async def dispatch_request(provider: str, body: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(provider, json=body) as response:
            return await response.json()


async def rpc_proxy_handler(request: Request) -> Response:
    try:
        body = await request.json()
    except ValueError:
        return error_response(PARSE_ERROR, 415)

    request_id = body.get("id")
    body_keys = [key.lower() for key in body.keys()]
    if body_keys.count("method") != 1 or not isinstance(body["method"], str):
        return error_response(INVALID_REQUEST, 401, request_id)

    if body["method"] not in ALLOWED_METHODS:
        return error_response(METHOD_NOT_SUPPORTED, 401, request_id)

    try:
        response = await dispatch_request(
            os.getenv("WEB3_PROVIDER_URI", "http://127.0.0.1:8545"), body
        )
        if (
            body["method"] in ("eth_getBlockByHash", "eth_getBlockByNumber")
            and "result" in response
        ):
            response["result"]["transactions"] = []
        return JSONResponse(content=response)
    except Exception:
        return error_response(RESULT_UNAVAILABLE, 500, request_id)
