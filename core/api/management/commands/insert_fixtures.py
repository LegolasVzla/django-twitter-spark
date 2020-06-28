from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Install nltk for word tokenize and stop words'

    def handle(self, *args, **options):
        try:
            import os
            import subprocess

            subprocess.call("python manage.py loaddata fixtures/"+'languages.json',shell=True)
            subprocess.call("python manage.py loaddata fixtures/"+'social_networks.json',shell=True)
            subprocess.call("python manage.py loaddata fixtures/"+'users.json',shell=True)
            subprocess.call("python manage.py loaddata fixtures/"+'topics.json',shell=True)
            subprocess.call("python manage.py loaddata fixtures/"+'word_root.json',shell=True)
            subprocess.call("python manage.py loaddata fixtures/"+'positive_dictionary.json',shell=True)
            subprocess.call("python manage.py loaddata fixtures/"+'negative_dictionary.json',shell=True)
            subprocess.call("python manage.py loaddata fixtures/"+'social_network_accounts.json',shell=True)

            self.stdout.write(self.style.SUCCESS('Successfully load fixtures'))

        except Exception as e:
            self.stdout.write(self.style.ERROR('An error happened: "%s"' % str(e)))
