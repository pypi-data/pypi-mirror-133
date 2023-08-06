from distutils.core import setup
from setuptools import find_packages


setup(
    name='DiscordDankBot',         
    packages=find_packages(),
    version='0.1.2',     
    license='MIT',        
    description='All in one bot to manage your dankmemer account. Easy automaton for grinding money and collectables.',  
    author='Adithya Narayan',                  
    author_email='narayanadithya1234@gmail.com',     
    entry_points={'console_scripts': ['dankbot = dankbot.dankcli:run_bot']},
    url='https://github.com/NarayanAdithya/Dankbot',   
    download_url='https://github.com/NarayanAdithya/Dankbot/archive/refs/tags/v_0.1.1-beta.tar.gz',    
    keywords=['Discord', 'Automation', 'DankBot', 'Dank Memer'],  
    install_requires=['selenium', 'windows-curses'],
    classifiers=[
        'Development Status :: 4 - Beta',     
        'Intended Audience :: Developers',      
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)
