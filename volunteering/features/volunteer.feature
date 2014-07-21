Feature: Volunteering
  o volunteer can go to system see potential duties
  o volunteer can assign themself to many duties
  o coordinator can see the assigned and unassigned duties for a given campaign.

  Scenario: Adding a Volunteer
    Given a admin user is logged in
    When he creates a volunteer called "Steve Stevenson"
    Then he sees that the volunteer "Steve Stevenson" was created

  Scenario: Viewing the plan for a volunteer
    Given a admin user is logged in
    Given a campaign called "Summer camp" with duties:
      | Name      | Attributes |
      | counselor |      |
      | cook      |      |
      | security  |      |
      | greeter   |      |
      | usher     |      |
    Given some duties are assigned to the volunteer:
      | Name      | Attributes |
      | counselor |      |
      | cook      |      |
    Given some duties are assigned to another volunteer:
      | Name     | Attributes |
      | security |      |
    When the volunteer views her plan
    Then she sees the available duties for which she could volunteer to be assigned:
      | Name    | Attributes |
      | greeter |      |
      | usher   |      |
    And she sees the duties assigned to her:
      | Name      | Attributes |
      | counselor |      |
      | cook      |      |
    And she does not sees the duties assigned to others:
      | Name     | Attributes |
      | security |      |

  Scenario: A volunteer can volunteer for a duty
    Given a campaign with a First Aid duty
    And a doctor who is qualified for the First Aid duty
    When the doctor volunteers for the First Aid duty
    Then the doctor is assigned the First Aid duty

  Scenario: A volunteer cannot volunteer for a duty she cannot perform
    Given a campaign with a First Aid duty
    And a cook who is not qualified for the First Aid duty
    Then the cook cannot volunteer for the First Aid duty

  Scenario: A volunteer cannot volunteer for a duty that has already been taken
    Given a campaign with a duty
    And two volunteers who are qualified for the duty
    When the first volunteer has volunteered for the duty
    Then the second volunteer cannot volunteer for the duty
