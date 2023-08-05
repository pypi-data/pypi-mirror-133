import os, shutil, datetime, psutil, time
from tkinter import messagebox
import urllib.request as urlreq
from platform import architecture

def time_user_def():
     date = datetime.date.today()
     clock = datetime.datetime.today()
     time_user = 'Date today: '+ str(date)+ ', time now '+str( clock.strftime('%H.%M.%S'))
     return time_user
# take time, date and directory
print(str(time_user_def()))
print('Starting to create a server!')
# User time
def internet_button():
     print('Internet checking!')
     try:
          urlreq.urlopen("http://github.com")
          print('Internet connected!')
          return True
     except IOError:
          print("Internet is broken!")
          messagebox.showerror(title='Internet', message='Internet don`t connected, function download core, java, python and backup don`t working.')
          return False
internet = internet_button()
def create_command():
     check_file = os.path.isdir('C:/minecraft')
     if   check_file == False:
          os.mkdir("C:/minecraft")
          os.chdir('C:\minecraft')
     else: 
          os.chdir('C:/minecraft')
     print('EULA text create...')
     # downloading server files in folder
     eula =  open('eula.txt', 'w+')
     eula_text = '''#Mojang EULA(https://account.mojang.com/documents/minecraft_eula).
# Time is not aviable
# Made by https://github.com/yaflay

eula=true
 '''
     eula.write(str(eula_text))
     eula.close()
     print('EULA text has been created!')
     print('Creating .bat file')
     bat = open('mine.bat', 'w+')
     bat_text = '''
java -Xmx1024M -Xms1024M -jar server.jar nogui
'''
     bat.write(str(bat_text))
     bat.close()
     # crate bat file and downloading jar core
     print('Created .bat file!')
     #  creating EULA text, and write in eula.txt
     # this is 4rd checkbox
     messagebox.showinfo('EULA', 'EULA and folders create! Press OK for leave')

def starting_server_button():  
     os.chdir('C:/minecraft')
     print('Downloading core...')
     url = 'https://launcher.mojang.com/v1/objects/a16d67e5807f57fc4e550299cf20226194497dc2/server.jar'
     urlreq.urlretrieve(url, 'C:/minecraft/server.jar') 
     print('Core downloaded!')
     messagebox.showinfo('bat file created', '.bat file and core created Press OK for leave')

#     first checkbox command
def server_properties_button():
     if internet_button():
          os.chdir('C:/minecraft')
          url_server_properties = 'https://raw.githubusercontent.com/YaFlay/Minecraft_server_creating/main/server_properties.py'
          urlreq.urlretrieve(url_server_properties, 'C:/minecraft/server_properties.py')
          os.system('python3 C:/minecraft/server_properties.py')
          print('Creating server.properties')
          messagebox.showinfo('server.properties created', 'Minecraft server.properties created Press OK for leave')
          os.remove('C:/minecraft/server_properties.py')
          return True
     else: messagebox.showerror(title='Internet', message='Internet don`t connected')
# second checkbox command
def close_command_button():
     os.remove(str(__file__))
     os.remove('index.py')
     os.remove('windows.py')
     messagebox.showinfo('file deleted', 'minecraft.exe closed and deleted! Press OK for leave')
#    deleting main file
def ok():
     window.destroy()
     # close window button

def start():
     os.chdir('C:/minecraft')
     os.system('start mine.bat')
     messagebox.showinfo('Server_start', 'Server started!! Press OK for leave')
#  starting server

def folder():
     os.startfile('C:/minecraft')
# start folder

def java_windows():
     if internet_button():
          if architecture() == '32bit':
                    java='https://bit.ly/java32python'
                    urlreq.urlretrieve(java, 'C:/minecraft/jre-8u311-windows-i586-iftw.exe')
                    print('Core downloaded')
                    print('Openning...')
                    os.chdir('C:/minecraft/')
                    os.startfile(r'C:/minecraft/jre-8u311-windows-i586-iftw.exe')
                    def process_name_32():
                         for proce in psutil.process_iter():
                              name = proce.name()
                              if name == 'jre-8u311-windows-i586-iftw.exe':
                                   return True
                    while process_name_32():
                         time.sleep(5)
                    print('Java downloaded')
                    if os.path.isfile('C:/minecraft/jre-8u311-windows-i586-iftw.exe'):
                         os.remove('jre-8u311-windows-i586-iftw.exe')
                         print('Java installer deleted')
                    pass
                    messagebox.showinfo('Java_32', 'Java has been downloaded! Press ok for leave')
          elif architecture() == '64bit':
               java_64='https://bit.ly/java64python'
               urlreq.urlretrieve(java_64, 'C:/minecraft/jre-8u311-windows-x64.exe')
               print('Core downloaded')
               print('Openning...')
               os.chdir('C:/minecraft/')
               os.startfile(r'C:/minecraft/jre-8u311-windows-x64.exe')
               def process_name_64():
                    for proce in psutil.process_iter():
                         name = proce.name()
                         if name == 'jre-8u311-windows-x64.exe':
                              return True
               while process_name_64():
                    time.sleep(5)
               print('Java downloaded')
               if os.path.isfile('C:/minecraft/jre-8u311-windows-x64.exe'):
                    os.remove('jre-8u311-windows-x64.exe')
                    print('Java installer deleted')
               pass
          pass 
          messagebox.showinfo('Java_64','Java has been downloaded! Press ok for leave')
     else:
          messagebox.showerror(title='Internet', message='Internet don`t connected')
          
# for downloading java 8u311 for windows

def delete_directory():
          if os.path.isdir('C:/minecraft'):
               os.chdir('C:/minecraft')
               if os.path.isfile('eula.txt'):
                    os.remove('eula.txt')
                    print('EULA deleted')
               # deleting eula
               if os.path.isfile('mine.bat'):
                    os.remove('mine.bat')
                    print('mine.bat deleted')
               # deleting .bat file
               if os.path.isfile('server.jar'):
                    os.remove('server.jar')
                    print('server.jar deleted')
               # deleting core
               if os.path.isfile('server.properties'):
                    os.remove('server.properties')
                    print('server.properties deleted')
               # deleting server.properties
               if os.path.isfile('banned-ips.json'):
                    os.remove('banned-ips.json')
                    print('banned-ips.json deleted')
                    # deleting banned-ips.json
               if os.path.isfile('banned-players.json'):
                    os.remove('banned-players.json')
                    print('banned-players.json deleted')
                    # deleting banned-players.json
               if os.path.isfile('ops.json'):
                    os.remove('ops.json')
                    print('ops.json deleted')
                    # deleting ops.json
               if os.path.isfile('usercache.json'):
                    os.remove('usercache.json')
                    print('usercashe.json deleted')
                    # deleting ops.json
               if os.path.isfile('whitelist.json'):
                    os.remove('whitelist.json')
                    print('whitelist deleted')
                    # deleting whitelist.json
          #  deleting all files in C:/minecraft
               directory_file = os.listdir()
               print(directory_file)
               if directory_file == ['logs', 'world', 'backup']:
                    os.chdir('C:/')
                    shutil.rmtree('C:/minecraft')
               else:
                    os.chdir('C:/')
                    shutil.rmtree('C:/minecraft')
                    # delete directory with files
          else:
               print('Folder already deleted')
                    
def backup_button():
     if internet_button():
          if os.path.isdir('C:/minecraft/backup/'):
               os.chdir('C:/minecraft/backup')
          else: 
               os.mkdir('C:/minecraft/backup')
               os.chdir('C:/minecraft/backup')
          # create folder

          url_backup_text='https://raw.githubusercontent.com/YaFlay/Minecraft_server_creating/main/backup.py'
          if os.path.isfile('C:/minecraft/backup/backup.py'):
               os.remove('C:/minecraft/backup/backup.py')
          urlreq.urlretrieve(url_backup_text, 'C:/minecraft/backup/backup.py')
          os.chdir('C:/minecraft/backup/')
          os.popen('python3 C:/minecraft/backup/backup.py')
          #  backuping minecraft files using python code from my github
     else: messagebox.showerror(title='Internet', message='Internet don`t connected')
def python_install():
     if internet_button():
          url = 'https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe'
          urlreq.urlretrieve(url, 'C:/minecraft/python-3.10.0-amd64.exe')
          os.chdir('C:/minecraft/')
          os.startfile(r'C:/minecraft/python-3.10.0-amd64.exe')
          for process_python in psutil.process_iter():
               name_python = process_python.name()
               if name_python == 'python-3.10.0-amd64.exe':
                    print('Wait...')
                    time.sleep(30)
                    print('And 10 sec more')
                    time.sleep(10)
                    named_64 = process_python.name()
                    if not named_64 == 'python-3.10.0-amd64.exe':
                         process_python.kill()
                    print('Process has been eliminated!')
               pass
          pass
          os.remove('python-3.10.0-amd64.exe')
          messagebox.showinfo('Python','Python has been downloaded! Press ok for leave')
     else: messagebox.showerror(title='Internet', message='Internet don`t connected')
# download python
# take def for checkboxes and buttons
