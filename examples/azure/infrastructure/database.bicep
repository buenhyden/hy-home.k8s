@description('The Azure region for the database')
param location string

@description('Unique name for the PostgreSQL server')
param serverName string

@description('Admin login for the server')
param adminLogin string = 'pgadmin'

@description('Entra ID Admin name')
param entraAdminName string

@description('Entra ID Admin Object ID')
param entraAdminObjectId string

@description('PostgreSQL version')
param version string = '16'

@description('Database SKU')
param skuName string = 'Standard_B1ms' // Burstable for Dev/Scaling example

resource postgres 'Microsoft.DBforPostgreSQL/flexibleServers@2023-12-01-preview' = {
  name: serverName
  location: location
  sku: {
    name: skuName
    tier: 'Burstable'
  }
  properties: {
    version: version
    administratorLogin: adminLogin
    authConfig: {
      activeDirectoryAuth: 'Enabled'
      passwordAuth: 'Disabled'
      tenantId: subscription().tenantId
    }
    highAvailability: {
      mode: 'ZoneRedundant'
    }
    storage: {
      storageSizeGB: 32
    }
  }
}

resource database 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2023-12-01-preview' = {
  parent: postgres
  name: 'hy-home-db'
  properties: {
    charset: 'UTF8'
    collation: 'en_US.utf8'
  }
}

resource entraAdmin 'Microsoft.DBforPostgreSQL/flexibleServers/administrators@2023-12-01-preview' = {
  parent: postgres
  name: entraAdminObjectId
  properties: {
    principalName: entraAdminName
    principalType: 'User'
    tenantId: subscription().tenantId
  }
}

output serverHost string = postgres.properties.fullyQualifiedDomainName
output serverId string = postgres.id
