import setuptools
from setuptools import setup, find_packages
from setuptools.command.install import install as InstallCommand

class Install(InstallCommand):
    """ Customized setuptools install command which uses pip. """

    def run(self, *args, **kwargs):
        import pip
        pip.main(['install', '.'])
        InstallCommand.run(self, *args, **kwargs)

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent

long_description = (this_directory/"README.md").read_text()

install_requires = ['importlib-resources',
                    '--extra-index-url https://google-coral.github.io/py-repo/ tflite_runtime']

setuptools.setup(
    name="pyoxynet",
    version="0.0.3.0",
    author="Andrea Zignoli",
    author_email="andrea.zignoli@unitn.it",
    description="Python package of the Oxynet project (visit www.oxynet.net)",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    cmdclass={
        'install': Install,
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_data={'': ['pics/*', 'models/*']},
    #exclude_package_data={
    #    '': 'debugging.py.c'},
    python_requires='>=3.8',
)