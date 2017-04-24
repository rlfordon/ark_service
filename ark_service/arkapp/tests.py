from django.test import TestCase

from arkapp.models import Ark, Minter

class MinterTestCase(TestCase): 
    def test_ark_exists(self): 
        minter = Minter(name='test_ark_exists', prefix='123', template='eeddeeddk')
        minter.save()
        ark = Ark(key='111111111', minter=minter)
        ark.save()
        self.assertTrue(minter._ark_exists('111111111'))

    def test_mint(self): 
        minter = Minter(name='test_mint', prefix='123', template='eeddeeddk')
        minter.save()
        minter.mint(1)
        ark = Ark.objects.all()[0]
        self.assertTrue(len(ark.key)==9)

class ArkTestCase(TestCase): 
    def test_bind(self):
        url = 'www.example.com'
        minter = Minter(name='test_ark_exists', prefix='123', template='eeddeeddk')
        minter.save()
        ark = Ark(key='111111111', minter=minter)
        ark.bind(url)
        ark.save()
        self.assertTrue(ark.url == 'www.example.com/ark:/12345/123/111111111')