## examples
Feature: Create a reservation

  Scenario: Create a zone reservation

	Given Create zone one open reservation
	When I submit a zone one reservation
	Then I am received error message 