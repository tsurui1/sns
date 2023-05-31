from accounts.models import CustomUser
from insta.models import Post
from django.test import TestCase
from django.shortcuts import resolve_url


class ほげほげViewTests(TestCase):

    # 1度だけ呼ばれる。テストデータの準備などをここで行う
    def setUp(self):
        self.user = CustomUser.objects.create(
            username='test_user'
        )
        self.user2 = CustomUser.objects.create(
            username='test_user2'
        )
        self.user.follow.add(self.user2)

        Post.objects.create(
            caption='test1', user=self.user2
        )


    def test_get(self):
        self.client.force_login(self.user)
        response = self.client.get(resolve_url("insta:top"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test1")