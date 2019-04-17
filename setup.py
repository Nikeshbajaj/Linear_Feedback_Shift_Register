import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lfsr",
    version="0.0.1",
    author="Nikesh Bajaj",
    author_email="nikkeshbajaj@gmail.com",
    description="Linear Feedback Shift Register",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nikeshbajaj/Linear_Feedback_Shift_Register",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
