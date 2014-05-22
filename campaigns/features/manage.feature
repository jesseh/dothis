Feature: Administering Campaigns
  the volunteer coordinator
  We've got this campaign
  it has these duties
  when I commit bob to getting the t-shirt for this campaing
  then he is notified of his commitment.


  campaign -> (duties with implied potential volunteers)
  duties -> ( description, required capabilities)
  volunteer -> ( contact info, capabilities)


  coordinator can create a campaign with duties and required capabilities

  coordinator can see the assigned and unassigned duties for a given campaign.

  admin can setup up volunteers

  admin can manage volunteer capabilities


  volunteer can go to system
  see potential duties
  and assign themself to many duties

  Scenario: Adding a Campaign
    Given a admin user is logged in
    When he creates a campaign called "Gate Security"
    Then he sees that the campaign "Gate Security" was created

  Scenario: Assigning Duties to a campaign
    Given a coordinator is logged in
    When he creates a campaign called "Summer camp" with duties:
      | Name      |
      | counselor |
      | cook      |
    Then he sees the "Summer camp" campaign with the duties:
      | Name      |
      | counselor |
      | cook      |

  Scenario: Adding a Volunteer
    Given a admin user is logged in
    When he creates a volunteer called "Steve Stevenson"
    Then he sees that the volunteer "Steve Stevenson" was created
