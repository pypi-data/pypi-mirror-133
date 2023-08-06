from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ui2utils",
    version="0.0.6",
    author="xyz",
    author_email="940724376@qq.com",
    description="A simple package of uiautomator2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hqwander9527/ui2utils",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        'uiautomator2>=2.16.3',
    ],
    packages=find_packages(),
)
