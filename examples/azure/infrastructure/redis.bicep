@description('The Azure region for the cache')
param location string

@description('Unique name for the Redis instance')
param redisName string

@description('Redis SKU name')
param skuName string = 'Premium'

@description('Redis SKU family')
param skuFamily string = 'P'

@description('Redis SKU capacity')
param skuCapacity int = 1

@description('The subnet ID for private endpoint')
param subnetId string

resource redis 'Microsoft.Cache/Redis@2023-08-01' = {
  name: redisName
  location: location
  properties: {
    sku: {
      name: skuName
      family: skuFamily
      capacity: skuCapacity
    }
    enableNonSslPort: false
    minimumTlsVersion: '1.2'
    publicNetworkAccess: 'Disabled'
    redisConfiguration: {
       'maxmemory-policy': 'volatile-lru'
    }
  }
}

// Private Endpoint for Redis
resource privateEndpoint 'Microsoft.Network/privateEndpoints@2023-09-01' = {
  name: '${redisName}-pe'
  location: location
  properties: {
    subnet: {
      id: subnetId
    }
    privateLinkServiceConnections: [
      {
        name: '${redisName}-plsc'
        properties: {
          privateLinkServiceId: redis.id
          groupIds: [
            'redisCache'
          ]
        }
      }
    ]
  }
}

output redisHost string = redis.properties.hostName
output redisId string = redis.id
