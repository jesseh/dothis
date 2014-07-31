Feature: Volunteering
  o volunteer can go to system see potential duties
  o volunteer can assign themself to many duties
  o coordinator can see the assigned and unassigned duties

  Scenario: Adding a Volunteer
    Given a admin user is logged in
    When he creates a volunteer called "Steve Stevenson"
    Then he sees that the volunteer "Steve Stevenson" was created

  Scenario: Viewing the plan for a volunteer
    Given a admin user is logged in
    Given the duties:
      | Activity  | Location      | Event     |
      | counselor | fright street | halloween |
      | cook      | kitchen       | halloween |
      | security  | scream lane   | halloween |
      | greeter   | angry ave     | halloween |
      | usher     | candy cove    | halloween |
    Given some duties are assigned to the volunteer:
      | Activity  | Location      | Event     |
      | counselor | fright street | halloween |
      | cook      | kitchen       | halloween |
    Given some duties are assigned to another volunteer:
      | Activity  | Location      | Event     |
      | security  | scream lane   | halloween |
    When the volunteer views her plan
    Then she sees the available duties for which she could volunteer to be assigned:
      | Activity  | Location      | Event     |
      | greeter   | angry ave     | halloween |
      | usher     | candy cove    | halloween |
    And she sees the duties assigned to her:
      | Activity  | Location      | Event     |
      | counselor | fright street | halloween |
      | cook      | kitchen       | halloween |
    And she does not sees the duties assigned to others:
      | Activity  | Location      | Event     |
      | security  | scream lane   | halloween |


  Scenario: A volunteer can volunteer for a duty
    Given a First Aid duty
    And a doctor who is qualified for the First Aid duty
    When the doctor volunteers for the previously unassigned First Aid duty
    Then the doctor is assigned the First Aid duty

  Scenario: A volunteer cannot volunteer for a duty she cannot perform
    Given a First Aid duty
    # And a cook who is not qualified for the First Aid duty
    # Then the cook cannot volunteer for the First Aid duty

  Scenario: A volunteer cannot volunteer for a duty that has already been taken
    # Given a duty
    # And two volunteers who are qualified for the duty
    # When the first volunteer has volunteered for the duty
    # Then the second volunteer cannot volunteer for the duty
