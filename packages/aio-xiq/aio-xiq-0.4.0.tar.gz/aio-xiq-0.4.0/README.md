# Extreme Cloud IQ - Python3 AsyncIO Client

This repository contains a Python3 asyncio based client library for interacting
with the Extreme Cloud IQ system (XIQ).

Note that Extreme does provide their own Python SDK client, which can be found
in the reference section below.

# Installation

```shell
pip install aio-xiq
```

This XIQ asyncio python client is a subclass from httpx.AsyncClient.

# QuickStart

Before using the API you must either have an existing token or login with your user-name + password
credentials.  You can either pass these values into the client constructor, or use these environment variables:

* XIQ_USER - the login user-name
* XIQ_PASSWORD = the login password
<br/>
-- or --
* XIQ_TOKEN - an existing API token

**Username + Password**

If you are using your login credentials you must execute the `login()` method to obtain an access
token.

```python
from aioxiq import XiqClient

async with XiqClient(xiq_user='bob@corp.com', xiq_password='notarealpassword') as api:
    await api.login()
    devices = await api.fetch_devices()
```

**API Token**

You can create an API token via the XIQ portal by nagivating to the Global
Settings page (found under your User profile near the top-right), and then
selecting the "API Token Management" option on the left sidebar.

When using the API Token approach, you can use the client diretly without having
to perform the login function.

```python
from aioxiq import XiqClient

# presume that XIQ_TOKEN environment variable is set with an existing token.
# you can immediately use the API without login.

async with XiqClient() as api:
    devices = api.fetch_devices()
```

### References
 * [Extreme Developer Portal](https://developer.extremecloudiq.com/)
 * [Extreme XIQ API Online Docts, Swagger](https://api.extremecloudiq.com/swagger-ui/index.html?configUrl=/openapi/swagger-config)
 * [Extreme XIQ APIs Github repo](https://github.com/extremenetworks/ExtremeCloudIQ-APIs)
 * [Extreme XIQ Python SDK Github repo](https://github.com/extremenetworks/ExtremeCloudIQ-SDK-Python)
