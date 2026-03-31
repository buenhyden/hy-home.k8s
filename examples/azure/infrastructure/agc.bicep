targetScope = 'resourceGroup'

@description('The Azure region for the migration')
param location string = resourceGroup().location

@description('Unique name prefix for all resources')
param prefix string = 'hy-home'

@description('The ID of the subnet where AGC associations will be created')
param agcSubnetId string

// 1. Application Gateway for Containers (Traffic Controller - v2)
resource trafficController 'Microsoft.ServiceNetworking/trafficControllers@2023-11-01' = {
  name: '${prefix}-agc'
  location: location
}

// 2. Association (Linking Traffic Controller to Subnet)
resource association 'Microsoft.ServiceNetworking/trafficControllers/associations@2023-11-01' = {
  parent: trafficController
  name: '${prefix}-agc-association'
  location: location
  properties: {
    subnet: {
      id: agcSubnetId
    }
  }
}

// 3. Frontend (Global Endpoint provided by AGC)
resource frontend 'Microsoft.ServiceNetworking/trafficControllers/frontends@2023-11-01' = {
  parent: trafficController
  name: '${prefix}-agc-frontend'
  location: location
}

output agcFqdn string = frontend.properties.fqdn
output trafficControllerId string = trafficController.id
