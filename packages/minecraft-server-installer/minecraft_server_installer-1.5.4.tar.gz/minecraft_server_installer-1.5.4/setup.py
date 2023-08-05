import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='minecraft_server_installer',  
     version='1.5.4',
     scripts=['internet_button', 'create_command', 'starting_server_button', 'server_properties_button', 'close_command_button', 'start', 'folder', 'java_windows', 'delete_directory', 'backup_button', 'python_install'] ,
     author="YaFlay",
     author_email="yaflay@vk.com",
     description="minecraft server creator",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/YaFlay/Minecraft_server_creating",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )