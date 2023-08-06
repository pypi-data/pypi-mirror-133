import setuptools

# Load README
with open('README.md', 'r', encoding = 'utf8') as file:
    long_description = file.read()

# Define package metadata
setuptools.setup(
    name = 'cb_badges',
    version = '0.3.1',
    author = 'Martin Folkers',
    author_email = 'hello@twobrain.io',
    description = '',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://codeberg.org/S1SYPHOS/cb-badges',
    license = 'MIT',
    project_urls = {
        'Issues': 'https://codeberg.org/S1SYPHOS/cb-badges/issues',
    },
    entry_points = """
        [console_scripts]
        badges=cb_badges.cli:cli
    """,
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages = setuptools.find_packages(),
    package_data = {'cb_badges': [
        'data/fonts/**/*.ttf',
        'data/fonts/**/*.otf',
        'data/templates/**/*.j2',
        'data/templates/**/*.json',
        'data/templates/**/themes/*.json',
    ]},
    install_requires = [
        'bs4',
        'click',
        'diskcache',
        'font-line',
        'jinja2',
        'lxml',
        'pycairo',
        'pytest',
        'requests',
        'svgpathtools',
    ],
    python_requires = '>= 3.7'
)
