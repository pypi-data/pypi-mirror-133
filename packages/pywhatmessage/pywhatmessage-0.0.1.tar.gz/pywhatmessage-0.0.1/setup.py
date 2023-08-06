from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))


VERSION = '0.0.1'
DESCRIPTION = 'Send whatsapp messages'
LONG_DESCRIPTION = 'A package that allows to send whatsapp messages.'

# Setting up
setup(
    name="pywhatmessage",
    version=VERSION,
    author="Sabaris",
    author_email="spssabaris@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['time', 'webbrowser', 'datetime',
                      'typing', 'urllib', 'pyautogui', 'pywhatkit'],
    keywords=['python', 'whatsapp', 'message',
              'whatmessage', 'whatmsg', 'automation'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
