from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Directory, File, FileSection, SectionCategory, Status, StatusData
from .forms import UploadFileModelForm, UploadDirectoryModelForm, ProverForm, VCForm

import re
import subprocess
from subprocess import Popen
from django.utils import timezone
from django.http import JsonResponse


def add_sections(obj):
    names = {
        "loop invariant" : "loop invariant",
        "requires" : "pre-condition",
        "ensures" : "post-condition",
        "predicate" : "predicate",
        "assert" : "assertion",
    }
    regex_str = "("
    index = 0
    for name in names:
        if index != 0:
            regex_str += "|"
        regex_str += name
        index = index + 1
    regex_str += ")"
    print(regex_str)

    description = ""
    section_object = None
    with obj.file_field.open('r'):
        line_number = 1
        lines = obj.file_field.readlines()
        for line in lines:
            if re.search("@", line):
                cleaned_line = re.sub("^.*@ ", "", line)
                result = re.search(regex_str, cleaned_line)
                if result: # match between the line and one of the section categories
                    category = names[result.group(1)]
                    category_object = SectionCategory(
                        category = category,
                        last_updated = timezone.now()
                    )
                    category_object.save()
                    if section_object is not None:
                        section_object.save()

                    section_object = FileSection(
                        line = line_number, 
                        desc = line, # cała linijka jest na razie desc, potem będziemy dodawać
                        creation_date = timezone.now(),
                        last_updated = timezone.now(),
                        category = category_object,
                        file_fk = obj,
                        status_data_fk = StatusData.objects.create(user=obj.owner),
                        status_fk = Status.objects.create()
                    )
                else:
                    if section_object is not None:
                        section_object.desc += line
            line_number += 1

def open_file(request):
    file_pk = None
    current_file = None
    if request.method == "POST":
        if 'file_id' in request.POST:
            file_pk = request.POST['file_id'] # pk pliku ktory ma byc wyswietlany
        elif 'file_id' in request.session:
            file_pk = request.session['file_id']
    elif request.method == "GET":
        if 'file_id' in request.session:
            file_pk = request.session['file_id']
    if file_pk != None:
        if File.objects.filter(pk=file_pk).exists():
            current_file = File.objects.get(pk=file_pk)

    request.session['file_id'] = file_pk        
    return {'file': current_file}


def upload_file(request):
    if request.method == "POST":
        form = UploadFileModelForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = form.save()
            add_sections(file_obj)
    form = UploadFileModelForm()
    return render(request, 'apka/upload.html', {'form':form})    

def upload_folder(request):
    if request.method == "POST":
        form = UploadDirectoryModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    form = UploadDirectoryModelForm()
    return render(request, 'apka/upload_directory.html', {'form':form}) 

def delete_file(request):
    files = File.objects.filter(is_available=True)
    if request.method == "POST":
        file_pk = request.POST.get('file_to_delete')

        file = File.objects.get(pk=file_pk)
        file.is_available = False
        file.save()
    return render(request, 'apka/delete_file.html', {'files' : files})

def delete_directory(request):
    directories = Directory.objects.filter(is_available=True)
    if request.method == "POST":
        dir_pk = request.POST.get('directory_to_delete')
        directory = Directory.objects.get(pk=dir_pk)
        directory.is_available = False
        directory.save()
    return render(request, 'apka/delete_directory.html', {'directories' : directories})

# def choose_tab(request):
#     current_tab = '1'
#     if request.method =='GET':
#         if 'tab' in request.COOKIES:
#             current_tab = request.COOKIES['tab']
#     elif request.method == 'POST':
#         if 'tab' not in request.POST:
#             current_tab = request.COOKIES['tab']
#         else:
#             current_tab = request.POST['tab']
#     return {'tab' : current_tab}    

def choose_tab(request):
    current_tab = '1'
    if request.method =='GET':
        if 'tab' in request.COOKIES:
            current_tab = request.COOKIES['tab']
    elif request.method == 'POST':
        if 'tab' not in request.POST:
            current_tab = request.COOKIES['tab']
        else:
            current_tab = request.POST['tab']
    return {'tab' : current_tab}

def get_directory_tree(directory):
    children = directory.directory_set.all()
    files_in_dir = directory.file_set.all()
    if not children:
        # this folder has no children, recursion ends here
        return {'dir': directory, 'children': [], 'files': files_in_dir,}

    # this folder has children, get every child's directory_tree
    return {
        'dir': directory,
        'children': [get_directory_tree(child) for child in children],
        'files': files_in_dir,
    }

def tabs(request):
    vc_list = []
    prover = "Alt-Ergo"
    if request.method == 'POST':
        if 'prover' in request.POST:
            prover_form = ProverForm(request.POST)
            if prover_form.is_valid():
                prover = request.POST.get('prover')
                request.session['prover'] = prover
        elif 'submit_vc' in request.POST:
            vc_form = VCForm(request.POST)
            if vc_form.is_valid():
                vc_list = request.POST.getlist('vc_list')
                request.session['vc_list'] = vc_list

    prover_form = ProverForm()
    vc_form = VCForm()
    
    if 'prover' in request.session:
        prover = request.session['prover']
    if 'vc_list' in request.session:
        vc_list = request.session['vc_list']
    
    vc_form.fields['vc_list'].initial = vc_list
    prover_form.fields['prover'].initial = prover

    request.session['prover'] = prover
    request.session['vc_list'] = vc_list

    return {'vc_form' : vc_form, 'prover_form' : prover_form}
    
def run_frama(request):
    print("run frama")
    file_pk = request.session['file_id']
    if file_pk != None:
        file_obj = File.objects.get(pk=file_pk)
        file_path = [file_obj.file_field.path]
        default_params =  ["-wp", "-wp-print", "-wp-log=r:result.txt"]
        prover_param = ["-wp-prover", request.session['prover'].lower()]
        extra_params = request.session['vc_list']
        params = default_params + prover_param + extra_params + file_path
        p = Popen(["frama-c"] + params, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output, errors = p.communicate()
        print(output)
        result = open('result.txt', 'r')
        file_obj.frama_result = result.read()
        file_obj.save()

        sections = FileSection.objects.filter(file_fk=file_pk)
        for section in sections:
            section.status_data_fk.validity_flag = False
            section.status_data_fk.save()

        matches = re.split("[\-]+\n", output)
        for m in matches:
            #sprawdzenie czy pierwsza linia zaczyna się od Goal
            first_line = re.search("^\nGoal.*\n", m)
            if first_line != None:
                line_nr = re.search("line \d+", first_line.group(0)).group(0)
                line_nr = int(line_nr.split()[1])

                sec = next((x for x in sections if x.line == line_nr), None)
                if sec == None:
                    continue
                m = m.split('\n', 2)[2] # usuniecie dwoch pierwszych linii (newline i ta z Goal...)
                status_line = re.findall("Prover ([^ ]*) returns ([a-zA-Z]*).*\n", m)
                if not status_line:
                    return
                m = m.rsplit("\n", 3)[0] # usuniecie trzech ostatnich linii (newliny i z status)
                sec.status_data_fk.validity_flag = True
                sec.status_data_fk.status_data = m
                sec.status_data_fk.prover = status_line[0][0]
                sec.status_data_fk.save()
                sec.status_fk.status = status_line[0][1].lower()
                sec.status_fk.save()

def index(request):
    print("INDEX")
    context = {}
    if request.method == "POST" and 'run' in request.POST:
        run_frama(request)
    dir_tree_list = []
    root_dirs = Directory.objects.filter(parent_dir=None)
    parentless_files = File.objects.filter(directory=None)
    for r_dir in root_dirs:
        directory_tree = get_directory_tree(r_dir)
        dir_tree_list.append(directory_tree)

    context.update({'free_files' : parentless_files})
    context.update({'tree_list' : dir_tree_list})
    context.update(open_file(request))
    context.update(choose_tab(request))
    context.update(tabs(request))
            
    response = render(request, 'apka/index.html', context)
    response.set_cookie('tab', context['tab'])
    return response

