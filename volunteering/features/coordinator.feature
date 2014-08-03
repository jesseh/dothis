Feature: Administering Campaigns
  the volunteer coordinator
  We've got this campaign
  it has these duties
  when I commit bob to getting the t-shirt for this campaing
  then he is notified of his commitment.

  Scenario: Setting up volunteering opportunities
    Given a admin user is logged in

    When he adds an "event"
    And sets the "name" to be "Sports day"
    And sets the "description" to be "The sports day description"
    And sets the "date" to be "2014-01-01"
    And submits the form
    Then he visits the "event" list page
    And it says "Sports day"
    And it says "The sports day description"
    And it says "Jan. 1, 2014"

    When he adds a "location"
    And sets the "name" to be "Playing fields"
    And sets the "description" to be "Behind the school"
    And submits the form
    Then he visits the "location" list page
    And it says "Playing fields"
    And it says "Behind the school"

    When he adds an "attribute"
    And sets the "name" to be "has whistle"
    And submits the form
    Then he visits the "attribute" list page
    And it says "has whistle"

    When he adds an "activity"
    And sets the "name" to be "Referee"
    And sets the "description" to be "To keep it fun and safe"
    And sets the "attributes" to select "has whistle"
    And submits the form
    Then he visits the "activity" list page
    And it says "Referee"
    And it says "To keep it fun and safe"
    And it says "has whistle"

    When he adds a "duty"
    And sets the "event" to choose "Sports day (2014-01-01)"
    And sets the "location" to choose "Playing fields"
    And sets the "activity" to choose "Referee"
    And sets the "start_time" to be "1:00"
    And sets the "end_time" to be "2:00"
    And sets the "multiple" to be "5"
    And submits the form
    Then he visits the "duty" list page
    And it says "Sports day"
    And it says "Playing fields"
    And it says "Referee"
    #And it says "Jan. 1, 2014"
    And it says "1 a.m."
    And it says "2 a.m."
    And it says "5"


  Scenario: Setting up a volunteer
    Given a admin user is logged in

    When he adds an "attribute"
    And sets the "name" to be "kitchen staff"
    And submits the form
    Then he visits the "attribute" list page
    And it says "kitchen staff"

    When he adds a "volunteer"
    And sets the "name" to be "Ron Ronaldson"
    And sets the "attributes" to select "kitchen staff"
    And submits the form
    Then he visits the "volunteer" list page
    And it says "Ron Ronaldson"
    And it says "kitchen staff"


  Scenario: Planning communications
    # A Recipients defines the set of people to whom the messages will be sent.
    # They can be assigned or assignable
    # They can include 
    # A trigger is a set time that triggers a message for a duty set.
    #
    Given a admin user is logged in

    # a message is sent to the recipients at a given time relative to a base time.
    #
    When he adds a "campaign"
    And sets the "name" to be "Holidays"
    Then he visits the "campaign" list page
    And it says "Holidays"

    When he adds a "message"
    And sets the "campaign" to be "holidays"
    And sets the "assign_state" to be "all"




