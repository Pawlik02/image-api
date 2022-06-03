from rest_framework.test import APITestCase
from image_api.models import User, Plan, Height, Image
from django.core.files.uploadedfile import SimpleUploadedFile


def get_user_basic():
    height = Height(height=200)
    height.save()
    plan = Plan(name='test1', original_image=False, expiring_link=False)
    plan.save()
    plan.height.add(height)
    user = User(username='test1', plan=plan)
    user.set_password('1@qwerty')
    user.save()
    return user


def get_user_premium():
    height1 = Height(height=200)
    height1.save()
    height2 = Height(height=400)
    height2.save()
    plan = Plan(name='test2', original_image=True, expiring_link=False)
    plan.save()
    plan.height.add(height1)
    plan.height.add(height2)
    user = User(username='test2', plan=plan)
    user.set_password('1@qwerty')
    user.save()
    return user


def get_user_enterprise():
    height1 = Height(height=200)
    height1.save()
    height2 = Height(height=400)
    height2.save()
    plan = Plan(name='test3', original_image=True, expiring_link=True)
    plan.save()
    plan.height.add(height1)
    plan.height.add(height2)
    user = User(username='test3', plan=plan)
    user.set_password('1@qwerty')
    user.save()
    return user


class TestImageList(APITestCase):
    def test_get(self):
        response = self.client.get('')
        assert response.status_code == 403
        
        user1 = get_user_basic()
        self.client.login(username='test1', password='1@qwerty')
        response = self.client.get('')
        assert response.status_code == 200


class TestImageDetail(APITestCase):
    def test_get(self):
        response = self.client.get('/1/')
        assert response.status_code == 403

        user1 = get_user_basic()
        self.client.login(username='test1', password='1@qwerty')
        mock_image = SimpleUploadedFile(name='test_image.jpg', content=open('image_api/test_image.jpg', 'rb').read(),
                                        content_type='image/jpeg')
        Image.objects.create(image=mock_image, owner=user1)
        response = self.client.get('/1/')
        assert response.status_code == 200

        response = self.client.get('/2/')
        assert response.status_code == 404

        self.client.logout()
        user2 = get_user_premium()
        self.client.login(username='test2', password='1@qwerty')
        response = self.client.get('/1/')
        assert response.status_code == 403


class TestImageOriginal(APITestCase):
    def test_get(self):
        user2 = get_user_premium()
        mock_image = SimpleUploadedFile(name='test_image.jpg', content=open('image_api/test_image.jpg', 'rb').read(),
                                        content_type='image/jpeg')
        Image.objects.create(image=mock_image, owner=user2)
        response = self.client.get('/1/original/')
        assert response.status_code == 403

        self.client.login(username='test2', password='1@qwerty')
        response = self.client.get('/1/original/')
        assert response.status_code == 200

        response = self.client.get('/2/original/')
        assert response.status_code == 404

        self.client.logout()
        user3 = get_user_enterprise()
        self.client.login(username='test3', password='1@qwerty')
        response = self.client.get('/1/original/')
        assert response.status_code == 403


class TestImageDetailExpiring(APITestCase):
    def test_get(self):
        user3 = get_user_enterprise()
        self.client.login(username='test3', password='1@qwerty')
        mock_image = SimpleUploadedFile(name='test_image.jpg', content=open('image_api/test_image.jpg', 'rb').read(),
                                        content_type='image/jpeg')
        image = Image.objects.create(image=mock_image, owner=user3, time=300)
        self.client.logout()

        response = self.client.get(f'/1/{image.expiring_link}')
        assert response.status_code == 200

        response = self.client.get(f'/1/randomtextlongerthan10characters')
        assert response.status_code == 404


class TestImageThumbnail(APITestCase):
    def test_get(self):
        user3 = get_user_enterprise()
        self.client.login(username='test3', password='1@qwerty')
        mock_image = SimpleUploadedFile(name='test_image.jpg', content=open('image_api/test_image.jpg', 'rb').read(),
                                        content_type='image/jpeg')
        image = Image.objects.create(image=mock_image, owner=user3, time=300)
        response = self.client.get('/1/thumbnail/200')
        assert response.status_code == 200

        response = self.client.get('/1/thumbnail/400')
        assert response.status_code == 200
