from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()


setup_args = dict(
    name='BVCscrap',
    version='0.1.0',
    description='Python library to scrape financial data from Casablanca Stock Exchange(Bourse des Valeurs de Casablanca)',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='ANDAM Amine',
    author_email='andamamine83@gmail.com',
    keywords=["Web scrapping","financial data"],
    url='https://github.com/AmineAndam04/BVCscrap',

)

install_requires = ['requests','BeautifulSoup','pandas','json','datetime']

