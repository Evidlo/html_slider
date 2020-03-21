from setuptools import setup
from pathlib import Path

setup(
    name='html_slider',
    version='1',
    packages=['html_slider'],
    author="Evan Widloski",
    author_email="evan@evanw.org",
    description="static html slider generator for images",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    license="GPLv3",
    keywords="static slider html numpy image",
    url="https://github.com/evidlo/html_slider",
    package_data={'passhole':['template.html', 'slider.html']},
    install_requires=[
        "imageio",
        "setuptools"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
