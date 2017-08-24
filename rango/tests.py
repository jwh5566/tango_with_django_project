from django.test import TestCase


class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """
        确保views是正数或0
        :return:
        """
        from rango.models import Category
        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_createion(self):
        """
        测试slug
        :return:
        """
        from rango.models import Category
        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')


class IndexViewTest(TestCase):
    def test_index_view_with_no_categories(self):
        """
         测试没有分类的时候，是否有响应
        :return:
        """
        from django.core.urlresolvers import reverse
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context['categories'], [])

    def add_cat(self, name, views, likes):
        """
        添加分类
        :param name:
        :param views:
        :param likes:
        :return:
        """
        from rango.models import Category
        c = Category.objects.get_or_create(name=name)[0]
        c.views = views
        c.likes = likes
        c.save()
        return c

    def test_index_view_with_categories(self):
        """
        检查首页有分类显示
        :return:
        """
        from django.core.urlresolvers import reverse
        self.add_cat('test', 1, 1)
        self.add_cat('temp', 1, 1)
        self.add_cat('tmp', 1, 1)
        self.add_cat('tmp test temp', 1, 1)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tmp test temp')
        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats, 4)
