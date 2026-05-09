targetScope = 'resourceGroup'

@description('The Azure region for the AKS cluster')
param location string = resourceGroup().location

@description('Unique name for the AKS cluster')
param clusterName string

@description('Kubernetes version')
param kubernetesVersion string = '1.35'

@description('The ID of the subnet where AKS nodes will be located')
param aksSubnetId string

resource aks 'Microsoft.ContainerService/managedClusters@2024-02-01' = {
  name: clusterName
  location: location
  sku: {
    name: 'Base'
    tier: 'Standard'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    kubernetesVersion: kubernetesVersion
    dnsPrefix: clusterName
    agentPoolProfiles: [
      {
        name: 'systempool'
        count: 2
        vmSize: 'Standard_DS2_v2'
        osType: 'Linux'
        mode: 'System'
        vnetSubnetID: aksSubnetId
      }
    ]
    networkProfile: {
      networkPlugin: 'azure'
      networkPluginMode: 'overlay'
      networkPolicy: 'azure'
    }
    securityProfile: {
      workloadIdentity: {
        enabled: true
      }
    }
    oidcIssuerProfile: {
      enabled: true
    }
  }
}

output clusterName string = aks.name
output oidcIssuerUrl string = aks.properties.oidcIssuerProfile.issuerURL
output aksIdentityPrincipalId string = aks.identity.principalId
