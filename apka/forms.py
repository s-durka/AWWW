from django import forms
from django.db import models
from django.forms.widgets import RadioSelect

from .models import File
from .models import Directory
    

class UploadFileModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'desc', 'file_field', 'directory', 'owner']
        def __init__(self, *args, **kwargs):
            super(UploadFileModelForm, self).__init__(*args, **kwargs)
            self.fields['directory'] = forms.ModelChoiceField(queryset=Directory.objects.exclude(is_available=False))

class UploadDirectoryModelForm(forms.ModelForm):
    class Meta:
        model = Directory
        fields = ['name', 'desc', 'parent_dir', 'owner']
        def __init__(self, *args, **kwargs):
            super(UploadFileModelForm, self).__init__(*args, **kwargs)
            self.fields['parent_dir'] = forms.ModelChoiceField(queryset=Directory.objects.exclude(is_available=False))



class ProverForm(forms.Form):
    CHOICES = (('Alt-Ergo', 'Alt-Ergo'), ('Z3', 'Z3'), ('CVC4', 'CVC4'))
    prover = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES, label="Select prover:")

class VCForm(forms.Form):
    VC_CHOICES = (
    ('-wp-rte', 'rte'),    
    ('-wp-prop="@lemma"', 'lemma'),
    ('-wp-prop="@requires"', 'requires'),
    ('-wp-prop="@assigns"', 'assigns'),
    ('-wp-prop="@ensures"', 'ensures'),
    ('-wp-prop="@exits"', 'exits"'),
    ('-wp-prop="@assert"', 'assert'),
    ('-wp-prop="@complete_behaviors"', 'complete_behaviors'),
    ('-wp-prop="@disjoint_behaviors"', 'disjoint_behaviors'),
    ('-wp-prop="@-lemma"', 'lemma'),
    ('-wp-prop="@-assigns"', 'assigns'),
    ('-wp-prop="@-ensures"', 'ensures'),
    ('-wp-prop="@-exits"', 'exits'),
    ('-wp-prop="@-assert"', 'assert'),
    ('-wp-prop="@-complete_behaviors"', 'complete_behaviors'),
    ('-wp-prop="@-disjoint_behaviors"', 'disjoint_behaviors'),
    )
    vc_list = forms.MultipleChoiceField(choices=VC_CHOICES, widget=forms.CheckboxSelectMultiple(
                                        attrs={
                                            'class':'choices',
                                            }
                                        ),
                                        label="Choose VCs",
                                        required=False,                    
                                    )