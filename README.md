# saarctf-client

This library allows accessing the status endpoint as described on https://ctf.saarland/setup

For usage information check out the `saarctf_client/client.py`, the code should not be too hard to understand.

## Request caching

You can optionally cache requests using a redis backend. This makes sense if you have limited bandwidth and start a large amount of processes in parallel or frequently call the functions, since each function equates an HTTP request to the endpoint.

To enable redis caching setup a redis listening on `localhost:6379` and set the environment variable `export SAARCTF_CLIENT_CACHE=1`. You can adjust the default TTL of 5 seconds by setting e.g. `SAARCTF_CLIENT_CACHE_EXPIRY=15`.
