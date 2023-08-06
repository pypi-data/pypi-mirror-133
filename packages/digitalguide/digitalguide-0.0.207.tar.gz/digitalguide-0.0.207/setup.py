from setuptools import find_packages, setup

setup(
    name='digitalguide',
    packages=find_packages(),
    version='0.0.207',
    description='A Python Library to write digital guides for telegram',
    author='Soeren Etler',
    license='MIT',
    install_requires=["python-telegram-bot",
                      "ctparse",
                      "boto3",
                      "pymongo[srv]>= 3.4, < 4.0",
                      "mongoengine",
                      "Pillow",
                      "openpyxl",
                      "PyYAML",
                      "twilio",
                      "flask",
                      "requests",
                      "gunicorn",
                      "google-api-python-client",
                      "google-auth-httplib2",
                      "google-auth-oauthlib"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'digitalguide = digitalguide.bot:bot',
        ],
    }
)
