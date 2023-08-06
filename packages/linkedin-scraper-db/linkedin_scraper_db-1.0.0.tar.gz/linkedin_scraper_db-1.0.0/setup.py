from setuptools import find_packages, setup

version = "1.0.0"

setup(
    name='linkedin_scraper_db',
    # this must be the same as the name above
    packages=['linkedin_scraper_db'],
    version=version,
    description='Scrapes multiple profiles on Linkedin',
    long_description="",
    long_description_content_type='text/markdown',
    author='Williams Sissoko',
    author_email='',
    # use the URL to the github repo
    url='https://github.com/wcisco17/linkedin_scraper_db',
    download_url='https://github.com/wcisco17/linkedin_scraper_db/dist/' + version + '.tar.gz',
    keywords=['linkedin', 'scraping', 'scraper', 'multiple linkedin profiles'],
    classifiers=[],
    install_requires=[package.split("\n")[0] for package in open(
        "requirements.txt", "r").readlines()]
)
