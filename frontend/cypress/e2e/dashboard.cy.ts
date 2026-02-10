describe('Dashboard E2E Tests', () => {
  beforeEach(() => {
    cy.visit('http://localhost:5173');
  });

  it('loads the dashboard successfully', () => {
    cy.get('h1').contains('Command & Control Dashboard');
  });

  it('displays device stats cards', () => {
    cy.get('.dashboard').contains('Total Devices');
  });

  it('shows device list panel', () => {
    cy.get('.dashboard').contains('Devices');
  });
});
