from setuptools import setup

setup(
    name='Task_Tracker_CLI',
    version='0.0',
    description='Program do zarządzania zadaniami.',
    py_modules=["main"],
    entry_points={
        'console_scripts': [
            "task-cli = main:main"
        ],
    },
)
