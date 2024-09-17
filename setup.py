from setuptools import find_packages, setup


setup(
    name='jounce',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    zip_safe=False,
    url='',
    install_requires=[
        'Flask',
        'Flask-Migrate',
        'Flask-SQLAlchemy',
        'Flask-Injector', 
        'injector',
        'Celery',
        'SQLAlchemy',
        'psycopg2-binary',
        'gunicorn',
        'requests',
    ],
    test_requires=[]
)