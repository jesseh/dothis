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
    When a volunteer views her plan
    Then she sees the available duties for which she could volunteer
    # And she sees the duties for which she has volunteered
