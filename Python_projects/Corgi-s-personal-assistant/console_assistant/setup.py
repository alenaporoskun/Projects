from setuptools import setup, find_packages

setup(
    name='console_assistant2',
    version='0.2',
    description="A very useful console assistant for Santa's assistant, Mr. Corgi.",
    url='https://github.com/alenaporoskun/Christmas-developers_Corgi-s-personal-assistant-Group14',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'console-assistant = console_assistant.main:main',
        ],
    },
)