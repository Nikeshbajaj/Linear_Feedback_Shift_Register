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
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=['numpy']
)
