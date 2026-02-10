describe('Device Tests', () => {
  beforeEach(() => {
    cy.visit('http://localhost:5173');
  });

  it('loads devices from API', () => {
    cy.intercept('GET', 'http://localhost:45847/api/v1/devices').as('getDevices');
    cy.wait('@getDevices').its('response.statusCode').should('eq', 200);
  });

  it('displays device status badges', () => {
    cy.get('.device-status').should('exist');
  });
});
