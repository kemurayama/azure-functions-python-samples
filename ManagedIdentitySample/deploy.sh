SUBSCRIPTION=
LOCATION=
RESOURCEGROUP=
APPNAME=
ASPNAME=
FUNCTION=
STORAGE=

az login 
az account set --subscription $SUBSCRIPTION

# Create Resource Group
az group create -l $LOCATION -n $RESOURCEGROUP

# Create App Service Plan
az appservice plan create --name $ASPNAME \
    --resource-group $RESOURCEGROUP \
    --is-linux --location $LOCATION \
    --number-of-workers 1 \
    --sku S1

# Create Web App
az webapp create --name $APPNAME \
    --plan $ASPNAME \
    --resource-group $RESOURCEGROUP \
    --runtime "PYTHON|3.7" \
    --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 --chdir app app:app"  \
    --assign-identity '[system]'

# Create Storage Account
az storage account create --name $STORAGE \
    --resource-group $RESOURCEGROUP \
    --location $LOCATION

# Create App Insights
az config set extension.use_dynamic_install=yes_without_prompt
az monitor app-insights component create --app $FUNCTION \
    --location $LOCATION \
    -g $RESOURCEGROUP \
    --kind web \
    --application-type web 

# Create Function App
az functionapp create --name $FUNCTION \
    --resource-group $RESOURCEGROUP \
    --app-insights $FUNCTION \
    --os-type Linux \
    --plan $ASPNAME \
    --storage-account $STORAGE \
    --functions-version 3 \
    --runtime python \
    --runtime-version 3.7 

PASS=$(openssl rand -base64 32)
APP=$(az ad app create --display-name $FUNCTION --homepage https://$FUNCTION.azurewebsites.net --oauth2-allow-implicit-flow true --reply-urls https://$FUNCTION.azurewebsites.net/.auth/login/aad/callback --password $PASS --required-resource-accesses @manifest.json)
ID=$(echo $APP | jq -r .appId)
TENANTID=$(az account show --query tenantId -o tsv)

az webapp auth update  -g $RESOURCEGROUP -n $FUNCTION --enabled true \
  --action LoginWithAzureActiveDirectory \
  --aad-allowed-token-audiences https://$FUNCTION.azurewebsites.net/.auth/login/aad/callback \
  --aad-client-id $ID --aad-client-secret $PASS \
  --aad-token-issuer-url https://sts.windows.net/$TENANTID/

az webapp config appsettings set -g $RESOURCEGROUP -n $APPNAME --settings FUNCTION_URL=https://$FUNCTION.azurewebsites.net/api/HTTPTrigger?name=Azure
az webapp config appsettings set -g $RESOURCEGROUP -n $APPNAME --settings FUNCTIONAPP_ID=$ID

cd frontend
zip -r frontend.zip ./
az webapp deployment source config-zip --resource-group $RESOURCEGROUP --name $APPNAME --src frontend.zip
cd ..


cd backend
func azure functionapp publish $FUNCTION
cd ..
