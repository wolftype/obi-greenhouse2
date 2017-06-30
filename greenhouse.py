'''
Template for creating new greenhouse apps
'''
from __future__ import print_function
from subprocess import call
import errno
import jinja2
import os
import re
import subprocess

def ensure_dir(path):
    '''
    mkdir -p for python
    '''
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def get_yobuild(g_speak_version):
    '''
    Look up which yobuild this gspeak depends on
    '''
    p = re.compile(r'YOBUILD_PREFIX.*"(.*)"')
    with open("/opt/oblong/g-speak%s/include/libLoam/c/ob-vers-gen.h" % g_speak_version, 'r') as f:
        for line in f:
            m = p.search(line)
            if (m):
                return m.group(1)

    # If g-speak wasn't installed, fall back to asking obs
    # NOTE: if the following line fails, please install the Oblong obs package
    return "/opt/oblong/deps-64-" + subprocess.check_output(["obs", "yovo2yoversion", g_speak_version]).rstrip()

def get_cef_branch(g_speak_version):
    '''
    Look up which cef this g-speak's webthing depends on
    '''
    p = re.compile(r'cefbranch=(.*)')
    webthingpath = "/opt/oblong/g-speak%s/lib/pkgconfig/libWebThing.pc" % g_speak_version
    if (os.path.exists(webthingpath)):
        with open(webthingpath, 'r') as f:
            for line in f:
                m = p.search(line)
                if (m):
                    return "cef" + m.group(1)

    # If webthing wasn't installed, fall back to asking obs
    # NOTE: if the following line fails, please install the Oblong obs package
    return subprocess.check_output(["obs", "yovo2cefversion", g_speak_version]).rstrip()

def obi_new(**kwargs):
    '''
    obi new greenhouse project_name --gspeak=g_speak_home
    '''

    kwargs['yobuild'] = get_yobuild(kwargs['g_speak_version'])
    kwargs['cef_branch'] = get_cef_branch(kwargs['g_speak_version'])

    project_name = kwargs['project_name']
    pairs = list([
        [os.path.join("debian", "changelog"), "changelog"],
        [os.path.join("debian", "compat"), "compat"],
        [os.path.join("debian", "control"), "control"],
        [os.path.join("debian", ".gitignore"), "debian.gitignore"],
        [os.path.join("debian", 'oblong-' + kwargs['project_name'] + '-gs' + kwargs['g_speak_version'] + 'x1.install'), "install"],
        [".gitignore", "gitignore"],
        [os.path.join("src", "main.cpp"), "main.cpp"],
        ["{0}.sublime-project".format(project_name), "proj.sublime-project"],
        ["project.yaml", "project.yaml"],
        ["README.md", "README.md"],
        [os.path.join("debian", "rules"), "rules"],
        ["three-feld.protein", "three-feld.protein"],
        ["three-screen.protein", "three-screen.protein"],
        ["oblong.cmake", "oblong.cmake"],
        ["baugen.sh", "baugen.sh"],
        ["CMakeLists.txt", "CMakeLists.txt"]])
    env = jinja2.Environment(loader=jinja2.PackageLoader(__name__),
                             keep_trailing_newline=True)
    project_path = kwargs['project_path']
    for file_path, template_name in pairs:
        file_path = os.path.join(project_path, file_path)
        ensure_dir(os.path.dirname(file_path))
        # look for the template in any of the envs
        # break as soon as we find it
        try:
            template = env.get_template(template_name)
            with open(file_path, 'w+') as fil:
                fil.write(template.render(kwargs))
        except jinja2.TemplateNotFound:
            print("Warning: Could not find template {0}".format(template_name))

    os.chmod(project_path + '/baugen.sh', 0755)
    os.chmod(project_path + '/debian/rules', 0755)
    # git init
    os.chdir(project_path)
    call(["git", "init"])
    call(["git", "add", "--all"])
    call(["git", "commit", "-m", "initial commit from obi template greenhouse"])
    call(["git", "tag", "-am", "dev-0.1", "dev-0.1"])
    return 0
