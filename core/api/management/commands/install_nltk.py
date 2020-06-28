from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Install nltk for word tokenize and stop words'

    def handle(self, *args, **options):
        try:
            import nltk
            nltk.download() # Needed for: stopwords.words()
            nltk.download('punkt')  # Needed for: word_tokenize()

            self.stdout.write(self.style.SUCCESS('Successfully installed nltk'))

        except Exception as e:
            self.stdout.write(self.style.ERROR('An error happened: "%s"' % str(e)))
