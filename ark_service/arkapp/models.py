from django.db import models
from django.conf import settings

import arkpy

class Minter(models.Model): 

    name = models.CharField(max_length=65)
    prefix = models.CharField(max_length=7, null=True)
    template = models.CharField(max_length=25)
    active = models.BooleanField(default=True)
    date_created = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    def __repr__(self): 
        return '<Minter: {}>'.format(self.name)

    def _ark_exists(self, key): 
        if len(Ark.objects.filter(key=key)) > 0: 
            return True
        else: 
            return False

    def mint(self, quantity): 
        authority = settings.NAAN
        template = self.template
        prefix = self.prefix
        for item in range(quantity): 
            ark = Ark()
            while True: 
                if prefix == None: 
                    offset = 6
                    tryark = arkpy.mint(authority, template, prefix)[offset:]
                else: 
                    offset = 6 + len(prefix)
                    tryark = arkpy.mint(authority, template, prefix)[offset:]
                if self._ark_exists(tryark):
                    pass
                else: 
                    ark.url = tryark
                    ark.key = tryark
                    ark.minter = self
                    break
            ark.save()

class Ark(models.Model): 
    key = models.CharField(max_length=25, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    minter = models.ForeignKey(Minter)
    url = models.URLField(null=True, blank=True)

    def __repr__(self): 
        return '<Ark: {}>'.format(self.key)

    def bind(self, url): 
        nma = url
        ark_label = 'ark:'
        naan = settings.NAAN
        prefix = self.minter.prefix
        key = self.key
        bound = nma + '/' + ark_label + '/' + naan + '/' + prefix + '/' + key
        self.url = bound