from api.models import Dictionary
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Update word_roots of the Dictionary model'

    def add_arguments(self, parser):
        parser.add_argument('language_id', nargs='+', type=int)

    def handle(self, *args, **options):
        try:
            import os
            import datetime
            from django.utils.timezone import utc

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

            polarities_dict = {"polarities": ["P","N"],"files": ["positive_dictionary","negative_dictionary"]}
            for i,polarity in enumerate(polarities_dict['polarities']):

                # Updating positive and negative dictionary fixtures
                query = Dictionary.objects.filter(polarity=polarities_dict['polarities'][i])
                file=open(os.getcwd()+"/fixtures/"+polarities_dict['files'][i]+".json",'w+')
                file.write("[")
                for j,instance in enumerate(query):
                    item=""
                    item='\n\t{\
                        \n\t\t"model": "api.dictionary",\
                        \n\t\t"fields": {\
                        \n\t\t\t"word": "'+instance.word+'",\
                        \n\t\t\t"word_root": "'+instance.word_root+'",\
                        \n\t\t\t"polarity": "'+polarities_dict['polarities'][i]+'",\
                        \n\t\t\t"language_id": 1,\
                        \n\t\t\t"is_active": true,\
                        \n\t\t\t"is_deleted": false,\
                        \n\t\t\t"created_date": "'+str(datetime.datetime.utcnow().replace(tzinfo=utc))+'",\
                        \n\t\t\t"updated_date": "'+str(datetime.datetime.utcnow().replace(tzinfo=utc))+'"\
                        \n\t\t}\
                        \n\t}'
                    if j != len(query)-1:
                        file.write(item+",")
                    else:
                        file.write(item+"\n]")
                file.close()

            self.stdout.write(self.style.SUCCESS('Successfully updated dictionary word roots for language_id: "%s"' % options['language_id'][0]))

        except Exception as e:
            self.stdout.write(self.style.ERROR('An error happened: "%s"' % str(e)))
