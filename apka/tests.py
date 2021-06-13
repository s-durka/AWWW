from django.test import TestCase
from . import models
from . import views
from . import forms
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.test import Client
from django.urls import reverse


def create_file(content):
    temp_dir = models.Directory.objects.create(name="temp")
    f = SimpleUploadedFile("test.txt", content)
    file_object = models.File.objects.create(name="test_file", file_field=f)
    return file_object, f

def create_logged_in_client():
    user = models.User.objects.create(username='test_user')
    user.set_password('password')
    user.save()
    c = Client()
    c.login(username='test_user', password='password')
    return c, user

class DirectoryModelTests(TestCase):
    def test_to_string_directory(self):
        some_folder = models.Directory(name="some_name")
        self.assertEquals(str(some_folder), "/some_name")
        self.assertEquals(some_folder.parent_dir, None)

class FileModelTests(TestCase):
    def test_display_text(self):
        file_object, f = create_file(b'line 1 text.\nline 2 text.\n')
        self.assertEquals(file_object.display_text(), "line 1 text.\nline 2 text.\n")
        os.remove(file_object.file_field.path)

class FileSectionModelTests(TestCase):
    def test_delete_file_cascade_filesection(self):
        file_object, f = create_file(b'/*@ requires valid_range(t,0,n-1); */\n')
        views.add_sections(file_object)
        self.assertEquals(models.FileSection.objects.exists(), True)
        file_object.delete()
        self.assertEquals(models.FileSection.objects.exists(), False)
        os.remove(file_object.file_field.path)
    def test_filesection_cascade_delete(self):
        file_object, f = create_file(b'some text\n')
        status_data_obj = models.StatusData.objects.create(status_data="data") 
        status_obj = models.Status.objects.create(status="status")
        category_obj = models.SectionCategory.objects.create(category="cat")
        section = models.FileSection.objects.create(
            line=1, 
            file_fk=file_object,
            status_data_fk = status_data_obj,
            status_fk = status_obj,
            category = category_obj
            )
        section.delete()
        self.assertFalse(models.StatusData.objects.exists())
        self.assertFalse(models.Status.objects.exists())
        self.assertFalse(models.SectionCategory.objects.exists())
        os.remove(file_object.file_field.path)



class UploadDirectoryModelFormTests(TestCase):
    def test_directory_form_validity(self):
        temp_user = models.User.objects.create(username='username',password='pass')
        form = forms.UploadDirectoryModelForm({
            'name' : 'folder name',
            'desc' : 'ulala'
            }, owner=temp_user)
        self.assertTrue(form.is_valid())

class ProverFormTests(TestCase):
    def test_prover_form_empty(self):
        form = forms.ProverForm({})
        self.assertFalse(form.is_valid())

class UploadFileViewTests(TestCase):
    def test_get_request_to_ajax_upload(self):
        client, user = create_logged_in_client()
        response = client.get(reverse('upload_file'))
        self.assertEquals(response.status_code, 404)
    def test_post_upload_file(self):
        client, user = create_logged_in_client()
        file_obj, f = create_file(b'file text')
        response = client.post(
            reverse('upload_file'),
            data = {
                'name' : 'test_file',
                'file_field' : file_obj.file_field
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.File.objects.all().count(), 2)
        os.remove(file_object.file_field.path)

    

class UploadFolderViewTests(TestCase):
    def test_get_request_to_ajax_upload_folder(self):
        client, user = create_logged_in_client()
        response = client.get(reverse('upload_folder'))
        self.assertEquals(response.status_code, 404) 

class DeleteFileViewTests(TestCase):
    def test_get_request_to_ajax_delete(self):
        client, user = create_logged_in_client()
        response = client.get(reverse('delete_file'))
        self.assertEquals(response.status_code, 404) 

class DeleteFolderViewTests(TestCase):
    def test_get_request_to_ajax_delete(self):
        client, user = create_logged_in_client()
        response = client.get(reverse('delete_folder'))
        self.assertEquals(response.status_code, 404) 
    
class IndexTests(TestCase):
    def test_redirect_not_logged(self):
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/accounts/login/?next=/')