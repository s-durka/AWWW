from django.db import models
from django.contrib.auth.models import User
import re


class Directory(models.Model):
    name = models.CharField(max_length=20)
    desc = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    parent_dir = models.ForeignKey('self', blank=True, null=True, default=None, on_delete=models.CASCADE)
    
    last_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        current_dir = self
        parents_list = []
        while current_dir != None:
            parents_list.append(current_dir)
            current_dir = current_dir.parent_dir
        path = ""
        for p in reversed(parents_list):
            path += "/"+p.name
        if path == "":
            path = "/"    
        return path

class File(models.Model):
    name = models.CharField(max_length=20)
    desc = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    file_field = models.FileField(upload_to = 'files')
    frama_result = models.TextField(blank=True)

    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    directory = models.ForeignKey(Directory, blank=True, null=True, default=None, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True) 
    last_updated = models.DateTimeField(auto_now = True)
    def display_text(self):
        self.file_field.open('r')
        return self.file_field.read()

    def __str__(self):
        if (self.directory == None):
            return "/" + self.name
        else:
            current_dir = self.directory
        parents_list = []
        while current_dir != None:
            parents_list.append(current_dir)
            current_dir = current_dir.parent_dir
        path = ""
        for p in reversed(parents_list):
            path += "/"+p.name
        if path == "":
            path = "/"    
        return path + "/" + self.name

class StatusData(models.Model):
    status_data = models.TextField()
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    prover = models.CharField(max_length=20, null=True, blank=True, default=None)
    last_updated = models.DateTimeField(auto_now = True)
    validity_flag = models.BooleanField(default=True)

class Status(models.Model):
    status = models.CharField(max_length=15)    
    last_updated = models.DateTimeField(auto_now = True)
    validity_flag = models.BooleanField(default=True)
    def __str__(self):
        return self.status

class SectionCategory(models.Model):
    category = models.CharField(max_length=15)
    last_updated = models.DateTimeField(auto_now = True)
    validity_flag = models.BooleanField(default=True)
    def __str__(self):
        return self.category

class FileSection(models.Model):
    line = models.IntegerField()
    name = models.CharField(max_length=20, blank=True)
    desc = models.TextField(blank=True)
    parent_section = models.ForeignKey('self', blank=True,  null=True, default=None, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add = True)
    category = models.OneToOneField(SectionCategory, on_delete=models.DO_NOTHING)
    file_fk = models.ForeignKey(File, on_delete=models.CASCADE, null=True, blank=True)
    status_data_fk = models.OneToOneField(StatusData, on_delete=models.DO_NOTHING, null=True, blank=True)
    status_fk = models.OneToOneField(Status, on_delete=models.DO_NOTHING, null=True, blank=True)

    last_updated = models.DateTimeField(auto_now = True)
    validity_flag = models.BooleanField(default=True)
    def delete(self, *args, **kwargs): #nadpisanie funkcji wbudowanej delete
        self.category.delete()
        self.status_data_fk.delete()
        self.status_fk.delete()
        return super(FileSection, self).delete(args, **kwargs)

    def __str__(self):
        return "category:" + self.category.category + ", line:" + str(self.line)
