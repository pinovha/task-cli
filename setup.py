from setuptools import setup

setup(
    name='Task Tracker CLI',
    version='0.1',
    author="Kamil",
    description='This is a simple CLI task manager/ tracker written in Python.',
    py_modules=["main"],
    entry_points={
        'console_scripts': [
            "task-cli = main:main"
        ],
    },
    tests_require=[
        'pytest==8.3.5'
    ],
)
