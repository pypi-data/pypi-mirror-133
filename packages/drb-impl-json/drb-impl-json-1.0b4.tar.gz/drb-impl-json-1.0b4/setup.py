import versioneer
from setuptools import find_packages, setup

with open('requirements.txt') as f:
    REQUIREMENTS = f.readlines()

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name='drb-impl-json',
    packages=find_packages(include=['drb_impl_json']),
    description='DRB json implementation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='GAEL Systems',
    author_email='drb-python@gael.fr',
    url='https://gitlab.com/drb-python/impl/json',
    install_requires=REQUIREMENTS,
    setup_requires=['setuptools_scm'],
    test_suite='tests',
    data_files=[('.', ['requirements.txt'])],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.8',
    entry_points={'drb.impl': 'json = drb_impl_json.drb_impl_signature'},
    use_scm_version=True,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
