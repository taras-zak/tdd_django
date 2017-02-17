from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from todo_lists.views import home_page
from todo_lists.models import Item

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_sove_a_POST_request(self):
        response = self.client.post('/', data={'item_text': "A new list item"})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'Firsts list item'
        first_item.save()

        first_item = Item()
        first_item.text = 'Second list item'
        first_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'Firsts list item')
        self.assertEqual(second_saved_item.text, 'Second list item')
