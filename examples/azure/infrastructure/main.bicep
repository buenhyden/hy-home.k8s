targetScope = 'resourceGroup'

@description('The Azure region for the migration')
param location string = resourceGroup().location

@description('Unique name prefix for all resources')
param prefix string = 'hy-home'

@description('Address space for the VNet')
param vnetPrefix string = '10.0.0.0/16'

@description('Subnet for AKS (CNI Overlay)')
param aksSubnetPrefix string = '10.0.1.0/24'

@description('Subnet for Application Gateway for Containers (AGC)')
param agcSubnetPrefix string = '10.0.2.0/24'

@description('Kubernetes version')
param k8sVersion string = '1.30'

// 1. VNet & Subnets
resource vnet 'Microsoft.Network/virtualNetworks@2023-09-01' = {
  name: '${prefix}-vnet'
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [vnetPrefix]
    }
    subnets: [
      {
        name: 'aks-subnet'
        properties: {
          addressPrefix: aksSubnetPrefix
          networkSecurityGroup: {
            id: nsg.id
          }
        }
      }
      {
        name: 'agc-subnet'
        properties: {
          addressPrefix: agcSubnetPrefix
          // AGC requires a dedicated subnet with delegation
          delegations: [
            {
              name: 'delegation'
              properties: {
                serviceName: 'Microsoft.ServiceNetworking/trafficControllers'
              }
            }
          ]
        }
      }
    ]
  }
}

resource nsg 'Microsoft.Network/networkSecurityGroups@2023-09-01' = {
  name: '${prefix}-aks-nsg'
  location: location
  properties: {
    securityRules: [
      {
        name: 'AllowHTTPS'
        properties: {
          priority: 100
          protocol: 'Tcp'
          access: 'Allow'
          direction: 'Inbound'
          sourceAddressPrefix: '*'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '443'
        }
      }
    ]
  }
}

// 2. AKS Cluster (OIDC & Workload Identity enabled)
resource aks 'Microsoft.ContainerService/managedClusters@2024-02-01' = {
  name: '${prefix}-aks'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    kubernetesVersion: k8sVersion
    dnsPrefix: '${prefix}-aks'
    agentPoolProfiles: [
      {
        name: 'systempool'
        count: 2
        vmSize: 'Standard_D2s_v3'
        osType: 'Linux'
        mode: 'System'
        vnetSubnetID: vnet.properties.subnets[0].id
      }
    ]
    networkProfile: {
      networkPlugin: 'azure'
      networkPluginMode: 'overlay' // Azure CNI Overlay
      podCidr: '192.168.0.0/16'
      serviceCidr: '172.16.0.0/16'
      dnsServiceIP: '172.16.0.10'
    }
    oidcIssuerProfile: {
      enabled: true
    }
    securityProfile: {
      workloadIdentity: {
        enabled: true
      }
    }
  }
}

// 3. User Assigned Identity for App Workload
resource appIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${prefix}-app-id'
  location: location
}

// 4. Federated Identity Credential for App
resource federatedCredential 'Microsoft.ManagedIdentity/userAssignedIdentities/federatedIdentityCredentials@2023-01-31' = {
  parent: appIdentity
  name: '${prefix}-app-fedid'
  properties: {
    issuer: aks.properties.oidcIssuerProfile.issuerURL
    subject: 'system:serviceaccount:default:hy-home-sa'
    audiences: ['api://AzureADTokenExchange']
  }
}

output aksName string = aks.name
output oidcIssuer string = aks.properties.oidcIssuerProfile.issuerURL
output vnetId string = vnet.id
output agcSubnetId string = vnet.properties.subnets[1].id
