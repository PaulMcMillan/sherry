from setuptools import setup

setup(
    name='Sherry',
    version='0.1',
    description='Sherry makes pxe easy',
    url='https://github.com/PaulMcMillan/sherry',
    packages=['sherry'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask'],
    license='BSD 2-Clause',
)
