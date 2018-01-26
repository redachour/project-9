from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from datetime import timedelta

from .models import *
from .forms import *


class MenuViewsTests(TestCase):
    def setUp(self):

        self.user = User.objects.create(
            username='username',
            email='email@hotmail.com',
            password='password')

        ingredient = Ingredient(name='Chocolate')
        ingredient.save()

        self.item = Item(name='Ice cream',
                         description='chocolate ice cream',
                         chef=self.user)

        self.item.save()
        self.item.ingredients.add(ingredient)
        self.menu = Menu.objects.create(
                season='Summer',
                expiration_date=timezone.now() + timedelta(days=400)
        )
        self.menu.items.add(self.item)

    def test_menu_list_view(self):
        resp = self.client.get(reverse('menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.menu, resp.context['menus'])
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')
        self.assertContains(resp, self.menu.season)

    def test_menu_detail_view(self):
        resp = self.client.get(reverse('menu_detail',
                                       kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.menu, resp.context['menu'])
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')

    def test_item_detail_view(self):
        resp = self.client.get(reverse('item_detail',
                                       kwargs={'pk': self.item.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.item, resp.context['item'])
        self.assertTemplateUsed(resp, 'menu/detail_item.html')

    def test_create_new_menu_view(self):
        resp = self.client.get(reverse('menu_new'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')

    def test_edit_menu_view(self):
        resp = self.client.post(reverse('menu_edit',
                                        kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')

    def test_menu_form(self):
        form = MenuForm({
            'season': 'Winter',
            'items': (1,),
            'expiration_date': timezone.now() + timedelta(days=400)})
        self.assertTrue(form.is_valid())
        menu = form.save()
        self.assertEqual(menu.season, 'Winter')
        self.assertEqual(menu.expiration_date.year, 2019)

    def test_date_validator(self):
        form = MenuForm({
            'season': 'Winter',
            'items': (1,),
            'expiration_date': '10/10/2017'
        })
        self.assertFalse(form.is_valid())
