import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

top_dir, _ = os.path.split(os.path.abspath(__file__))

with open(os.path.join(top_dir, 'Version')) as f:
    version = f.readline().strip()

setuptools.setup(
    name="pylfsr",
    version= version,
    author="Nikesh Bajaj",
    author_email="nikkeshbajaj@gmail.com",
    description="Linear Feedback Shift Register",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nikeshbajaj/Linear_Feedback_Shift_Register",
    download_url = 'https://github.com/Nikeshbajaj/Linear_Feedback_Shift_Register/tarball/' + version,
    packages=setuptools.find_packages(),
    license = 'MIT',
    keywords = 'lfsr linear-feedback-shift-register random generator gf(2)',
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Natural Language :: English',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Education',
        'Intended Audience :: Telecommunications Industry',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Games/Entertainment :: Puzzle Games',
        'Topic :: Communications',


    ],
    include_package_data=True,
    install_requires=['numpy']
)
