from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='sky_bkg',
    version='0.1.1',
    description='sky background',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    author='linlin',
    url='http://github.com',
    author_email='linlin@shao.ac.cn',
    license='MIT',
    packages=find_packages(),
    include_package_data=False,
    zip_safe=True,
)
