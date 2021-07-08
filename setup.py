from setuptools import setup

with open("requirements.txt", "r") as requirements:
    install_reqs = [req for req in requirements.read().split("\n")]
print(install_reqs)

setup(
    name='meeting_scheduler',
    version='0.1.0',
    packages=['meeting_scheduler'],
    url='https://github.com/AntonKopiika/meeting_scheduler',
    license='',
    author='Anton Kopiika',
    author_email='toxxa099@gmail.com',
    description='A python service for booking meetings with your colleagues.',
    install_reqs=install_reqs
)
