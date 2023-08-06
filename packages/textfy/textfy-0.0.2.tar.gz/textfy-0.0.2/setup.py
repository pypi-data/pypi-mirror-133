from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="textfy",
    version="0.0.2",
    author="Juyoung Oh",
    author_email="ojy7041@gmail.com",
    description="Send text notification when job is finished.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ojy0216/textfy",
    license='MIT',
    install_requires=['twilio'],
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)