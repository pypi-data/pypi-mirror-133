from setuptools import setup, find_packages


setup(
    name='prueba_maths',
    version='0.3',
    license='MIT',
    author="Florentino Perez",
    author_email='email@example.com',
    packages=['maths'],
    keywords='example math',
    install_requires=[
        'scikit-learn',
    ],
)