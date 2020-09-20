from django.contrib import admin

# Register your models here.
from api.models import (User,Dictionary,CustomDictionary,Topic,Search,
	WordRoot,SocialNetworkAccounts)

admin.site.register(User)
admin.site.register(Dictionary)
admin.site.register(CustomDictionary)
admin.site.register(Topic)
admin.site.register(Search)
admin.site.register(WordRoot)
admin.site.register(SocialNetworkAccounts)

