from django.utils.translation import ugettext_lazy as _

from grappelli.dashboard import modules, Dashboard


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        campaign_models = ('volunteering.models.Campaign',
                           'volunteering.models.Message',
                           'volunteering.models.Assignment',
                           'volunteering.models.Duty',
                           'volunteering.models.Event',
                           'volunteering.models.Activity',
                           'volunteering.models.Location',)

        volunteer_models = ('volunteering.models.Volunteer',
                            'volunteering.models.Family',
                            'volunteering.models.Attribute',)

        self.children.append(modules.LinkList(
            _('Monitor email service'),
            column=1,
            collapsible=False,
            children=[
                ['Events (excluding archived)',
                 'volunteering/event/?is_archived__exact=0', False],
                ['Duties for quick updating',
                 'volunteering/dutyeditable/', False],
                ['Volunteers with temporary changes',
                 'volunteering/volunteer/?temporary_change__exact=1', False],
                ['Recently added volunteers',
                 'volunteering/volunteeradded/', False],
                ['Security supervisors',
                 'volunteering/volunteer/?attributes__id__exact=1', False],
                ['Security-able volunteers',
                 'volunteering/volunteer/?attributes__id__exact=2', False],
                ['Steward-able volunteers',
                 'volunteering/volunteer/?attributes__id__exact=3', False],
            ]
        ))

        self.children.append(modules.ModelList(
            'Manage campaigns',
            collapsible=False,
            column=2,
            models=campaign_models,
            # models=('volunteering.models.Location',),
        ))

        self.children.append(modules.ModelList(
            'Manage volunteers',
            collapsible=False,
            column=2,
            models=volunteer_models,
        ))

        self.children.append(modules.ModelList(
            _('Manage coordinators'),
            column=2,
            collapsible=False,
            models=('django.contrib.*',),
        ))

        self.children.append(modules.LinkList(
            _('Monitor email service'),
            column=2,
            collapsible=False,
            children=[
                ['Email status', 'email/status', False],
                ['Email senders', 'email/senders', False],
                ['Email urls', 'email/urls', False],
                ['Email tags', 'email/tags', False],
                ['Sendables', 'volunteering/sendable/', False],
            ]
        ))

        self.children.append(modules.RecentActions(
            _('Recent actions'),
            limit=20,
            collapsible=False,
            column=3,
        ))
