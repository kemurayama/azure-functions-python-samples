# Azure Functions Python Samples

## EventGrid Trigger by Storage Blob Upload event.

[This Function](EventGridTrigger) works with Blob Upload event with EventGrid subscription.

You need below resources.

- Block Blob Storage Account or General-purpose v2 accounts
- Event Grid Subscription
- Azure Blob Storage SDK

## HTTPTrigger with Managed ID for Storage Authentication

[This Function](HttpTriggerManagedID) uses [Managed ID](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview) to authenticate Azure Storage Account.

It also requires `WEBSITE_RUN_FROM_PACKAGE=1` in AppSettings. It makse **wwwroot read only**

## LICENSE

This repository is [MIT LICENSE](./LICENSE). 