import setuptools

setuptools.setup(
    name="scrapzon",
    version="0.0.3",
    author="sachin Sankar",
    author_email="sachinpannadi@gmail.com",
    description='Amazon product details scraper',
    url='https://github.com/Chicken1Geek/scrapzon',
    keywords='amazon, scraper, crawlwer, lightweight',
    python_requires='>=3.6, <4',
    package_dir={'': 'scrapzon'},
    install_requires=['requests','bs4'],
)
