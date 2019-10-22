# Azure Functions Python Samples

## EventGrid Trigger by Storage Blob Upload event.

[This Function](EventGridTrigger) works with Blob Upload event.

You need below resources.

- Block Blob Storage Account or General-purpose v2 accounts
- Event Grid Subscription
- Azure Blob Storage SDK

In the Function, used [this SDK version](https://pypi.org/project/azure-storage-blob/12.0.0b4/) in order to use `aio`. 
`pip install azure-storage-blob==12.0.0b4` 

## HTTPTrigger with Managed ID for Storage Authentication

[This Function](HttpTriggerManagedID) uses [Managed ID](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview) to authenticate Azure Storage Account.

`azure-identity` is required module. 

`pip install azure-identity==1.0.0b4`

It also requires `WEBSITE_RUN_FROM_PACKAGE=1` in AppSettings. It makse **wwwroot read only**