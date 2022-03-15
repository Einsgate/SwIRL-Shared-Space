Feature: Delete a reservation

  Scenario: Delete a zone reservation

	Given Open reservation history
	When I click on the delete on specific reservation
	Then The reservation list changed