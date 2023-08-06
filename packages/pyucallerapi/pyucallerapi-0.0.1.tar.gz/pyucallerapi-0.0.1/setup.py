from setuptools import setup
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
VERSION = '0.0.1'
setup(
    name='pyucallerapi',
    version=VERSION,
    description='Python service for convenient work with uCaller API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['pyucallerapi', ],
    # packages=find_packages(where="src"),
    # package_dir={"": "src"},
    author='kebrick',
    author_email='ruban.kebr@gmail.com',
    license='MIT',
    project_urls={
        'Source': 'https://github.com/kebrick/pyucallerapi',
        'Tracker': 'https://github.com/kebrick/pyucallerapi/issues',
    },
    install_requires=['requests', ],

    python_requires='>=3.5',
    zip_safe=False
)
