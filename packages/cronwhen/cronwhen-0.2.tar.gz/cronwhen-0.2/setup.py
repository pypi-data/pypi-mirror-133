from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

    setup(
        name="cronwhen",
        version="0.2",
        description="A library computing next occurrence of a cron pattern",
        url="https://github.com/Silverspur/cronwhen",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Charles Lumet",
        author_email="charles.lumet@gmail.com",
        packages=['cronwhen'],
        install_requires=[],
        license="GNU General Public License v3.0",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Topic :: System",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ]
    )
