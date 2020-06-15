from django.core.management.base import BaseCommand, CommandError
from api.models import Dictionary

class Command(BaseCommand):
    help = 'Update word_roots of the Dictionary model'

    def add_arguments(self, parser):
        parser.add_argument('language_id', nargs='+', type=int)

    def handle(self, *args, **options):
        try:
            import Stemmer
            
            if options['language_id'][0] == 1:
                stemmer = Stemmer.Stemmer('spanish')
            else:
                raise CommandError('Language id "%s" does not exist' % options['language_id'][0])
            
            query = Dictionary.objects.filter(
                is_active=True,
                is_deleted=False,
                language_id=options['language_id'][0]
            )
            # Apply stemmer to every word of the dictionary
            for instance in query:
                instance.word_root = stemmer.stemWord(instance.word)
                instance.save()                

            self.stdout.write(self.style.SUCCESS('Successfully updated dictionary word roots for language_id: "%s"' % options['language_id'][0]))

        except Exception as e:
            self.stdout.write(self.style.ERROR('An error happened: "%s"' % str(e)))
