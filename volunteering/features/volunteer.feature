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
      | Name      | Tags |
      | counselor |      |
      | cook      |      |
      | security  |      |
      | greeter   |      |
      | usher     |      |
    Given some duties are assigned to the volunteer:
      | Name      | Tags |
      | counselor |      |
      | cook      |      |
    Given some duties are assigned to another volunteer:
      | Name     | Tags |
      | security |      |
    When the volunteer views her plan
    Then she sees the available duties for which she could volunteer to be assigned:
      | Name    | Tags |
      | greeter |      |
      | usher   |      |
    And she sees the duties assigned to her:
      | Name      | Tags |
      | counselor |      |
      | cook      |      |
    And she does not sees the duties assigned to others:
      | Name     | Tags |
      | security |      |
