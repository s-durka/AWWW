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
        # os.remove(file_object.file_field.path)

class FileSectionModelTests(TestCase):
    def test_delete_file_cascade_filesection(self):
        file_object, f = create_file(b'/*@ requires valid_range(t,0,n-1); */\n')
        views.add_sections(file_object)
        self.assertEquals(models.FileSection.objects.exists(), True)
        file_object.delete()
        self.assertEquals(models.FileSection.objects.exists(), False)
        # os.remove(file_object.file_field.path)
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
        # os.remove(file_object.file_field.path)



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
        # os.remove(file_obj.file_field.path)

class UploadFolderViewTests(TestCase):
    def test_get_request_to_ajax_upload_folder(self):
        client, user = create_logged_in_client()
        response = client.get(reverse('upload_folder'))
        self.assertEquals(response.status_code, 404) 
    def test_post_upload_folder(self):
        client, user = create_logged_in_client()
        response = client.post(
            reverse('upload_folder'),
            data = {
                'name' : 'new_dir',
                'desc' : 'test directory....'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Directory.objects.all().count(), 1)
        self.assertEqual(user, models.Directory.objects.first().owner)


class DeleteFileViewTests(TestCase):
    def test_get_request_to_ajax_delete(self):
        client, user = create_logged_in_client()
        response = client.get(reverse('delete_file'))
        self.assertEquals(response.status_code, 404) 
    def test_post_delete_file(self):
        client, user = create_logged_in_client()
        file_obj, f = create_file(b'file text')
        response = client.post(
            reverse('delete_file'),
            data = {
                'file_to_delete' : file_obj.id
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.File.objects.all().count(), 1) #dalej 1
        self.assertEqual(models.File.objects.first().is_available, False)


class DeleteFolderViewTests(TestCase):
    def test_get_request_to_ajax_delete(self): # metoda get nie powininna być możliwa
        client, user = create_logged_in_client()
        response = client.get(reverse('delete_folder'))
        self.assertEquals(response.status_code, 404) 
    def test_post_delete_folder(self):
        client, user = create_logged_in_client()
        dir_obj = models.Directory.objects.create(name="test_dir")
        response = client.post(
            reverse('delete_folder'),
            data = {
                'directory_to_delete' : dir_obj.id
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Directory.objects.all().count(), 1) #dalej 1
        self.assertEqual(models.Directory.objects.first().is_available, False)

class IndexTests(TestCase):
    def test_redirect_not_logged(self):
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/accounts/login/?next=/')
    def test_basic_home_view_test(self):
        client, user = create_logged_in_client()
        response = client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
    def test_homepage_reload_page(self):
        client, user = create_logged_in_client()
        response = client.get(reverse('index'))
        self.assertIn('vc_form', response.context)
        self.assertIn('prover_form', response.context)
        self.assertIn('upload_file_form', response.context)
        self.assertIn('upload_folder_form', response.context)
        self.assertIn('directories', response.context)
        self.assertIn('files', response.context)
        self.assertIn('file', response.context)
    def test_open_file_get(self):
        client, user = create_logged_in_client()
        file_object, f = create_file(b'line 1 text.\nline 2 text.\n')
        session = client.session
        session['file_id'] = str(file_object.pk)
        session.save()
        response = client.get(reverse('index'))
        self.assertIn('file', response.context)
        self.assertEquals(file_object.pk, response.context['file'].pk)

class OpenFileAjaxTests(TestCase):
    def test_open_file_ajax_session(self):
        client, user = create_logged_in_client()
        file_object, f = create_file(b'line 1 text.\nline 2 text.\n')
        response = client.post(reverse('open_file_ajax'), {'file_pk' : file_object.pk})
        self.assertIn('file_id', client.session)
        self.assertEquals(str(file_object.pk), client.session.get('file_id'))

    
# render_all_forms():
# class RenderFormsViewsTests(TestCase):
#     client, user = create_logged_in_client()
#     file_object, f = create_file(b'line 1 text.\nline 2 text.\n')
