import argparse
from functools import partial
from typing import Union

import uvicorn
from fastapi import FastAPI

from link_apis import LinkApi
from builder.auth import LinkAuth
linkApi = LinkApi()
app = FastAPI()


@app.post('/{method}')
def invoke_api(method: str, data: Union[dict, str]):
    cookie_str = data["cookies_str"]
    del data["cookies_str"]
    auth = LinkAuth()
    auth.perepare_auth(cookie_str)
    func = getattr(linkApi, method)
    if callable(func):
        func = partial(func, auth=auth)
        return func(**data)
    else:
        raise Exception(f"{method} is not callable")


def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=5011, type=int, help='fastapi server port')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_config()
    uvicorn.run(app, host="0.0.0.0", port=args.port)
