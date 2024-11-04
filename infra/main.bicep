
param location string = resourceGroup().location
@allowed([
  'dev'
  'prod'
])
param environmentName string
param productName string
param supportEmail string
param deploymentDate string = utcNow()
param image string = 'sohalal/backend'
param imageTag string = 'latest' 

var appServicePlanName = '${productName}-${environmentName}-asp'
var appServiceName = '${productName}-${environmentName}-app'
var acrName = '${productName}${environmentName}acr'
var keyVaultName = '${productName}-${environmentName}-kv'
var redisName = '${productName}${environmentName}redis'
var postgresName = '${productName}${environmentName}postgres'
var appInsightsName = '${productName}-${environmentName}-ai'
var budgetName = '${productName}-${environmentName}-budget'

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-11-01-preview' = {
  name: acrName
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
  }
}


resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: 'F1'
  }
  properties: {
    reserved: true
  }
}

resource webapp 'Microsoft.Web/sites@2023-12-01' = {
  name: appServiceName
  location: location
  tags: {
    'hidden-related:${resourceGroup().id}/providers/Microsoft.Web/serverfarms/appServicePlan': 'Resource'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      healthCheckPath: '/health'
      // acrUseManagedIdentityCreds: true
      linuxFxVersion: null
      appSettings: [
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsightsComponents.properties.InstrumentationKey
        }
        {
          name: 'REDIS_HOST'
          value: redisCache.properties.hostName
        }
        {
          name: 'WEBSITES_PORT'
          value: '8000'
        }
        {
          name: 'DOCKER_CUSTOM_IMAGE_NAME'
          value: 'DOCKER|${containerRegistry.name}.azurecr.io/${image}:${imageTag}'
        }
      ]
    }
  }
}

resource acrPullRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(webapp.id, 'acrpull')
  scope: containerRegistry
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')  // AcrPull role
    principalId: webapp.identity.principalId
  }
}

// resource budget 'Microsoft.Consumption/budgets@2021-10-01' = {
//   name: budgetName
//   scope: resourceGroup()
//   properties: {
//     category: 'Cost'
//     amount: 1
//     timeGrain: 'Monthly'
//     timePeriod: {
//       startDate: deploymentDate
//     }
//     notifications: {
//       actual: {
//         enabled: true
//         operator: 'GreaterThan'
//         threshold: 100
//         contactEmails: [
//           supportEmail
//         ]
//       }
//     }
//   }
// }

resource appInsightsComponents 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
  }
}

resource redisCache 'Microsoft.Cache/Redis@2019-07-01' = {
  name: redisName
  location: location
  properties: {
    sku: {
      name: 'Basic'
      family: 'C'
      capacity: 0
    }
  }
}

resource keyVault 'Microsoft.KeyVault/vaults@2019-09-01' = {
  name: keyVaultName
  location: location
  properties: {
    enabledForDeployment: true
    enabledForTemplateDeployment: true
    enabledForDiskEncryption: true
    tenantId: tenant().tenantId
    accessPolicies: [
      // {
      //   tenantId: tenant().tenantId
      //   objectId: webApplication.identity.principalId
      //   permissions: {
      //     keys: [
      //       'get'
      //       'list'
      //     ]
      //     secrets: [
      //       'get'
      //       'list'
      //     ]
      //   }
      // }
    ]
    sku: {
      name: 'standard'
      family: 'A'
    }
  }
}

resource appInsightsSecret 'Microsoft.KeyVault/vaults/secrets@2019-09-01' = {
  parent: keyVault
  name: 'appInsightsSecret'
  properties: {
    value: appInsightsComponents.properties.ConnectionString
  }
}

resource redisSecret 'Microsoft.KeyVault/vaults/secrets@2019-09-01' = {
  parent: keyVault
  name: 'redisSecret'
  properties: {
    value: redisCache.listKeys().primaryKey
  }
}





