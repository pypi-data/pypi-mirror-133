import re
from setuptools import setup, find_packages


requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

version = ""
with open('tanoshi/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')


readme = ""
with open('README.md', encoding="utf-8") as f:
    readme = f.read()

extras_require = {}

packages = find_packages()

setup(
    name='tanoshi',
    author='justanotherbyte',
    url='https://github.com/justanotherbyte/tanoshi',
    project_urls={
        "Documentation": "https://tanoshi.readthedocs.io/en/latest/",
        "Issue tracker": "https://github.com/justanotherbyte/tanoshi/issues",
    },
    version=version,
    packages=packages,
    license='BSD',
    description="A fast, asyncio based web-framework, that you'll enjoy using.",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    python_requires='>=3.8.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
    ]
)