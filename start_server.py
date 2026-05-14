import os
import sys
import subprocess

os.chdir(r'C:\Users\Administrator\TraeProject\mysite')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

subprocess.Popen([sys.executable, 'manage.py', 'runserver'],
                 creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS)