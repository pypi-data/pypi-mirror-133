import setuptools

setuptools.setup(
    name="kozip",
    version="1.1.0",
    license="MIT",
    author="Heekang Park",
    author_email="park.heekang33@gmail.com",
    description="Convert Korean ZIP code to address",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/HeekangPark/KoZIP",
    python_requires=">=3",
    packages=["kozip"],
    include_package_data=True,
    package_data={
        "KoZIP": [
            "new_zip.json",
            "old_zip.json"
        ]
    },
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
