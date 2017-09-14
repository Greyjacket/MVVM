from setuptools import setup

setup(
    name='MVVM',
    packages=['MVVM'],
    include_package_data=True,
    install_requires=[
        'flask',
        "flask-sqlalchemy",
    ],
)