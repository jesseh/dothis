Feature: Administering Campaigns
  the volunteer coordinator
  We've got this campaign
  it has these duties
  when I commit bob to getting the t-shirt for this campaing
  then he is notified of his commitment.


  campaign -> (duties with implied potential volunteers)
  duties -> ( description, required capabilities)
  volunteer -> ( contact info, capabilities)


  x coordinator can create a campaign 
  x a campaing has duties 
  x admin can setup up volunteers
  o coordinator can see the assigned and unassigned duties for a given campaign.
  o volunteer can go to system see potential duties
  o volunteer can assign themself to many duties

  o a duty has required capabilities

  o admin can manage volunteer capabilities


  Scenario: Creating a capaign with duties
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
    When he creates a duty called "Security"
    Then he sees that the duty "Security" was created
