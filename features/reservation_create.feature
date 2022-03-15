## examples
Feature: Create a reservation

  Scenario: Create a zone reservation

	Given Create zone one open reservation
	When I submit a zone one reservation
	Then I am received error message 
	
	Given Create zone one quiet reservation
	When I submit zone two open reservation
	Then I am received error messsage
	
	Given Create zone one cloased reservation
	When I submit a zone two open reservation
	Then I am received error message