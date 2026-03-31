targetScope = 'resourceGroup'

@description('The Azure region for the migration')
param location string = resourceGroup().location

@description('Unique name prefix for all resources')
param prefix string = 'hyhome'

@description('Entra ID Admin name (for DB/KeyVault)')
param adminName string

@description('Entra ID Admin Object ID')
param adminObjectId string

// 1. Networking Infrastructure
module network './network.bicep' = {
  name: 'network-deployment'
  params: {
    location: location
    prefix: prefix
  }
}

// 2. AKS Cluster (OIDC & Workload Identity)
module aks './aks.bicep' = {
  name: 'aks-deployment'
  params: {
    location: location
    clusterName: '${prefix}-aks'
    aksSubnetId: network.outputs.aksSubnetId
  }
}

// 3. Application Gateway for Containers (AGC)
module agc './agc.bicep' = {
  name: 'agc-deployment'
  params: {
    location: location
    prefix: prefix
    agcSubnetId: network.outputs.agcSubnetId
  }
}

// 4. Database Module
module database './database.bicep' = {
  name: 'db-deployment'
  params: {
    location: location
    serverName: '${prefix}-pg-server'
    entraAdminName: adminName
    entraAdminObjectId: adminObjectId
  }
}

// 5. Redis Cache Module
module redis './redis.bicep' = {
  name: 'redis-deployment'
  params: {
    location: location
    redisName: '${prefix}-redis-cache'
    subnetId: network.outputs.aksSubnetId
  }
}

// 6. Azure Key Vault (RBAC Mode)
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: '${prefix}-kv'
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enabledForDeployment: true
    enabledForTemplateDeployment: true
    publicNetworkAccess: 'Disabled'
  }
}

// 7. Managed Identity for Application
resource appIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${prefix}-app-id'
  location: location
}

// Federated Identity Credential for AKS Workload Identity
resource federatedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities/federatedIdentityCredentials@2023-01-31' = {
  parent: appIdentity
  name: '${prefix}-federated-id'
  properties: {
    issuer: aks.outputs.oidcIssuerUrl
    subject: 'system:serviceaccount:default:${prefix}-sa'
    audiences: [
      'api://AzureADTokenExchange'
    ]
  }
}

// Role Assignment: Key Vault Secrets User
resource kvRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, appIdentity.id, 'Key Vault Secrets User')
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')
    principalId: appIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

output aksName string = aks.outputs.clusterName
output pgHost string = database.outputs.serverHost
output redisHost string = redis.outputs.redisHost
output kvName string = keyVault.name
output oidcIssuer string = aks.outputs.oidcIssuerUrl
output clientId string = appIdentity.properties.clientId
