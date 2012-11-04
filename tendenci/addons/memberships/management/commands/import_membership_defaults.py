from datetime import datetime

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class Command(BaseCommand):
    """
    Import MembershipDefault.

    Usage:
        python manage.py import_membership_defaults [mimport_id] [request.user.id]

        example:
        python manage.py import_membership_defaults 10 1
    """

    def handle(self, *args, **options):
        from tendenci.addons.memberships.models import MembershipImport
        from tendenci.addons.memberships.utils import memb_import_parse_csv
        from tendenci.addons.memberships.utils import process_default_membership

        mimport = get_object_or_404(MembershipImport,
                                        pk=args[0])
        request_user = User.objects.get(pk=args[1])

        fieldnames, data_list = memb_import_parse_csv(mimport)
        summary_d = {
                     'insert': 0,
                     'update': 0,
                     'update_insert': 0,
                     'invalid': 0
                     }

        for memb_data in data_list:
            process_default_membership(
                                      request_user,
                                      memb_data,
                                      mimport,
                                      dry_run=False,
                                      summary_d=summary_d)
            mimport.num_processed += 1
            mimport.save()

        # we are done. save the status
        summary = 'insert:%d,update:%d,update_insert:%d,invalid:%d' % (
                                    summary_d['insert'],
                                    summary_d['update'],
                                    summary_d['update_insert'],
                                    summary_d['invalid']
                                    )
        mimport.summary = summary
        mimport.status = 'completed'
        mimport.complete_dt = datetime.now()
        mimport.save()
