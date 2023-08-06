from setuptools import setup, find_packages
setup(
    name='sky_bkg',
    version='0.1.0',
    description='sky background',
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
