dothis
======

A simple app to help get volunteers to commit to duties.

## Todo

* Add a null robots.txt
* Check if still assignable in assignment.
* Limit the signups per roll and add error handling in the form.
* Finish the email sending (send today, send when scheduled)
* Set up the cron job
* Put the real Mandrill api key in to Heroku.
* Output reports.
* Fix the page title




## Intro

* Go to a specific volunteer (http://nnls-coordinator.herokuapp.com/admin/volunteering/volunteer/ and click the left column of any row) and you'll see a link on the upper right of the page called "view on site". This links to the page that each person will see when they click through the email we are about to send. As you can see the list of volunteering opportunities is specific to the qualifications of each person as defined by their "attributes".

* Go to the duties list (http://nnls-coordinator.herokuapp.com/admin/volunteering/duty/) for the list of all the positions that we are trying to fill. As you can see, each duty is composed of of an 'event', a 'location', an 'activity'. It is set up this way so that we don't have to repeat ourselves when defining duties. In other words, there are only a handful of locations that are shared across many duties. And when you change the description of a location it will show up for all relevant duties.

* Duties also have an optional start time, end time, multiple, details, and coordinator notes. The hourly time is part of the duty while the date is part of the event so that we can easily copy duties for next year, and to prevent a mistyped date creating confusion.

  * The multiple is how many volunteers are needed for this specific duty.
  * The assignments lists shows how has volunteered for what. Members can generate their own assignments by claiming a volunteering opportunity through their personal link (as described in the first bullet). You can also create, change and delete assignments directly through this part of the site.

* Go to the admin overview page (http://nnls-coordinator.herokuapp.com/admin/) and you can see the entry for setting info about events, locations and activities, as discussed in the previous bullet.

* On the admin overview page there is a link to Users as well as to Volunteers. Users are you and me - people who have access to the admin pages. All of the shul members are included as Volunteers, but not Users.

* The link to attributes lets you define more attributes, which are used to limit which volunteers are suitable for which activities. This, in turn, limits the duties that a given volunteer is presented because each duty is comprised of an activity.

* The links called Campaigns, Triggers and Messages are related to the email system. In short, a campaign defines a set of duties for which emails will be sent (e.g. all duties related to a specific event, or all duties related to stewarding). The trigger defines when to send what message. Messages can be triggered at a fixed date, or some number of days before the relevant event, or some number of days after the duty was assigned. This means we can send "Thanks for volunteering" the day that someone assigns a duty to themselves. We can also send "Remember to.." three days before each event. And we can send "Please sign up" on a specific day in the future. The Message is then the content. It is seperate so that the same message can be used for various campaigns and triggers. This means we only have to write one "Thanks for volunteering" message.

* Note: I am still putting the finishing touches on this part of the system

* The third section of the admin overview page, called Djrill, shows information related to the emails we send. The system is hooked into Mailchimp's sibling company called Mandrill and it all should work at no cost for the first 12,000 emails per month.


