import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="permission_check",
    version="0.0.2",
    author="Somesh Garje",
    author_email="someshgarje@gmail.com",
    description="A simple, cross-platform, lightweight utility to check permission of files and folders in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/srgrj/permission_check",
    project_urls={
        "Bug Tracker": "https://github.com/srgrj/permission_check/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
