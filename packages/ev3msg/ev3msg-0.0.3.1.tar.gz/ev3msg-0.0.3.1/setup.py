from setuptools import setup

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3'
]

setup(
    name='ev3msg',
    version='0.0.3.1',
    description='A EV3 Messaging Library for Python',
    author='JJTV',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read() + '\n\n\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    license='OSI Approved :: GNU General Public License v3 (GPLv3)',
    classifiers=classifiers,
    keywords=["ev3", "messaging", "robotics", "communication", "protocol",
              "mailbox", "py", "python"],
    packages=["ev3msg"],
    install_requires=['pybluez2'],
    include_package_data=True
)
