import setuptools


setuptools.setup(
    name='DataScalerSelector',
    version='1.1.0',
    author='Asif Ahmed Neloy',
    author_email='neloyn@myumanitoba.ca',
    description='Data Scaler Selector is an open-source python library to select the appropriate data scaler (Min-Max, Robust or Standard Scaler) for your Machine Learning model.',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    License='MIT',
    long_description_content_type="text/markdown",
    url='https://github.com/aaneloy/data-scaler',
    keywords='scaler',
    py_module=["DataScalerSelector"],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)