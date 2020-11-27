# Azure Web App (Python) with Managed Identity

This repository is to show how **Managed Identity** works on Azure Web App and connects Function App.

## Prerequisites

Install `zip` and `jq` command for deploy.sh

## How to Deploy

1. Create Azure Web App and enable AAD Authentication.
2. Go to AAD portal and find the AAD App you created.
3. Copy manifest and create `manifest.json` like below

```json
[
    {
        "resourceAppId": "xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "resourceAccess": [
            {
                "id": "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy",
                "type": "Scope"
            }
        ]
    }
]
```

4. Use `deploy.sh` to deploy both Web App and Function App. You need to set these Environment Variables to run the script.

```bash
SUBSCRIPTION
RESOURCEGROUP
LOCATION
ASPNAME
APPNAME
STORAGE
FUNCTION
```

## How to Use

`/` returns `json` response which contains `access_token`.

```json
{
    "access_token": "", 
    "expires_on": "1604063773", 
    "resource": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx", 
    "token_type": "Bearer", 
    "client_id": "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
}
```

`/request_function` returns a response from Azure Functions.

## LICENSE

This repository is [MIT LICENSE](./LICENSE).
