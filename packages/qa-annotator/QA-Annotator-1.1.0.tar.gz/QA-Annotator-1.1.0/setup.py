from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    README = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='QA-Annotator',
    version='1.1.0',
    packages=find_packages(),
    url='https://github.com/impyadav/QA-Annotator',
    download_url='https://github.com/impyadav/QA-Annotator/archive/refs/tags/v_1.1.0.tar.gz',
    install_requires=required,
    license='MIT',
    author='Praveen Singh, Shubham Modi, Prateek Yadav',
    author_email='impyadav.tech@gmail.com',
    description='Data Annotation Tool for NLP-based Question-Answering systems.',
    long_description_content_type='text/markdown',
    long_description=README
)
