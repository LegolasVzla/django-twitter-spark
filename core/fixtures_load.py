import os
import subprocess
from core.settings import BASE_DIR

def loaddata():
	subprocess.call("python manage.py loaddata fixtures/"+'languages.json',shell=True)
	subprocess.call("python manage.py loaddata fixtures/"+'social_networks.json',shell=True)
	subprocess.call("python manage.py loaddata fixtures/"+'users.json',shell=True)
	subprocess.call("python manage.py loaddata fixtures/"+'topics.json',shell=True)
	subprocess.call("python manage.py loaddata fixtures/"+'word_root.json',shell=True)
	subprocess.call("python manage.py loaddata fixtures/"+'positive_spanish_dictionary.json',shell=True)
	subprocess.call("python manage.py loaddata fixtures/"+'negative_spanish_dictionary.json',shell=True)
	subprocess.call("python manage.py loaddata fixtures/"+'social_network_accounts.json',shell=True)
	
loaddata()
