{
  "projectRoot": "",
  "folder": "cypress",
  "files": [
    {
      "filePath": "cypress/e2e/dashboard.cy.ts",
      "content": "describe('Dashboard E2E Tests', () => {\n  beforeEach(() => {\n    cy.visit('http://localhost:5173');\n  });\n\n  it('loads the dashboard successfully', () => {\n    cy.get('h1').contains('Command & Control Dashboard');\n  });\n\n  it('displays device stats cards', () => {\n    cy.get('.dashboard').contains('Total Devices');\n  });\n\n  it('shows device list panel', () => {\n    cy.get('.dashboard').contains('Device List');\n  });\n});\n"
    },
    {
      "filePath": "cypress/e2e/map.cy.ts",
      "content": "describe('Map Tests', () => {\n  beforeEach(() => {\n    cy.visit('http://localhost:5173');\n  });\n\n  it('renders map container', () => {\n    cy.get('.dashboard').find('canvas').should('exist');\n  });\n\n  it('displays device markers on map', () => {\n    cy.get('.dashboard').find('.device-marker').should('have.length.gte', 1);\n  });\n});\n"
    },
    {
      "filePath": "cypress/e2e/devices.cy.ts",
      "content": "describe('Device Tests', () => {\n  beforeEach(() => {\n    cy.visit('http://localhost:5173');\n  });\n\n  it('loads devices from API', () => {\n    cy.intercept('GET', 'http://localhost:45847/api/v1/devices').as('getDevices');\n    cy.wait('@getDevices').its('response.statusCode').should('eq', 200);\n  });\n\n  it('displays device status badges', () => {\n    cy.get('.device-status').should('exist');\n  });\n});\n"
    }
  ]
}
