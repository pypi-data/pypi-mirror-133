from setuptools import setup
from setuptools import setup
from setuptools import find_namespace_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = '''
setuptools==60.1.0
wheel==0.37.1
pytest==6.1.2
pandas==1.1.4
'''

setup(
    name='file-reader-utility',
    version='0.1.0',
    author='Lahiru Madhawa',
    author_email='kmlahiru24@gmail.com',
    description='file reader utility',
    long_description="file: README.md",
    long_description_content_type="text/markdown",
    url='https://github.com/LahiruMadhawa2020/file-reader-tester.git',
    packages=[''],
    # install_requires=["setuptools==60.1.0", "wheel==0.37.1", "pytest==6.1.2", "pandas==1.1.4"],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        # Programming Languages Used..
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
