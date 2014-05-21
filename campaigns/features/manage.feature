Feature: Administering Campaigns

  Scenario: Adding a Campaign
    Given a admin user is logged in
    When he creates a campaign called "Gate Security"
    Then he sees that the campaign "Gate Security" was created
