describe('Map Tests', () => {
  beforeEach(() => {
    cy.visit('http://localhost:5173');
  });

  it('renders map container', () => {
    cy.get('.dashboard').find('canvas').should('exist');
  });

  it('displays device markers on map', () => {
    cy.get('.dashboard').find('.device-marker').should('have.length.gte', 1);
  });
});
