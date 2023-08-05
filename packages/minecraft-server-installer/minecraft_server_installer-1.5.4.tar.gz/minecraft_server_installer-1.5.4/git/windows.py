
from tkinter import Tk, BooleanVar, Button, Checkbutton
from commands import *

def windows():

    window=Tk()
    window.title('Minecraft server')
    window.geometry('500x300') #500/\, 250>
    # creating window
    create_server = BooleanVar()  
    create_server.set(True)
    create_server=Checkbutton(window, text='1)Create server EULA, .bat files and folder', var=create_server, command=create_command)  
    create_server.grid(column=1, row=1)
    # 4rd checkbox
    start_server = BooleanVar()  
    start_server.set(True)  
    start_server = Checkbutton(window, text='2)Downloading core', var=start_server, command=starting_server_button)  
    start_server.grid(column=1, row=2) 
    # first checkbox
    server_properties = BooleanVar()  
    server_properties.set(True)  
    server_properties = Checkbutton(window, text='3) Create server.properties', var=server_properties, command=server_properties_button)  
    server_properties.grid(column=1, row=3) 
    # second checkbox
    close_command = BooleanVar()  
    close_command.set(True)  
    close_command = Checkbutton(window, text='4) Delete installer', var=close_command, command=close_command_button)  
    close_command.grid(column=1, row=4) 
    # replace minecraft.py command
    open_folder = BooleanVar()  
    open_folder.set(True)  
    open_folder = Checkbutton(window, text='Open minecraft server folder', var=close_command, command=folder)  
    open_folder.grid(column=1, row=5) 
    # third checkbox
    button = Button(window, text='OK', command=ok)
    button.grid(column=1, row=7)
    # close program button
    starting_button = Button(window, text='Start server and open server.properties!', command=start)
    starting_button.grid(column=1, row=6)
    # starting server button
    delete_button=Button(window, text='Delete folder and files', command=delete_directory)
    delete_button.grid(column=1, row=10)
    # delete folder button

    java_32=Button(window, text='Downloading Java', command=java_windows)
    java_32.grid(column=1, row=11)
    # java for x32
    backup=Button(window, text='Backup minecraft-server files', command=backup_button)
    backup.grid(column=1, row=12)
    # Backup button
    python_download=Button(window, text='Downloading Python with official site', command=python_install)
    python_download.grid(column=0, row=12)
    # downloading python
    window.mainloop()
    # create window and button for start and create server
# creating def for index.py 