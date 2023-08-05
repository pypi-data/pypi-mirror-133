from setuptools import setup, find_packages


setup(
    long_description=open("README.md", "r").read(),
    name="pytilesrv",
    version="0.1",
    description="mapnik server",
    author="Pascal Eberlein",
    author_email="pascal@eberlein.io",
    url="https://github.com/nbdy/pytilesrv",
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords="mapnik render server",
    packages=find_packages(),
    long_description_content_type="text/markdown",
    install_requires=[
        "loguru", "flask", "MapRenderCache"
    ],
    entry_points={
        'console_scripts': [
            'pytilesrv = pytilesrv.__main__:main'
        ]
    }
)
