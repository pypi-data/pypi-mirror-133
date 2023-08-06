from setuptools import setup
import re

with open('discord/ext/cli/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open("README.md", "r") as f:
	long_desc = f.read()

setup(
name="discord.ext.cli",
author="Alex Hutz",
author_email="frostiiweeb@gmail.com",
keywords=["discord"],
version=version,
packages=['discord.ext.cli'],
license='MIT',
long_description=long_desc,
long_description_content_type="text/markdown",
description="A CLI to talk through console.",
install_requires=['aiohttp>=3.7.3', "discord.py>=1.7.3", "waiting"],
python_requires='>=3.7.0',
project_urls={

"Issue Tracker": "https://github.com/FrostiiWeeb/discord-ext-cli/issues"
},
url="https://github.com/FrostiiWeeb/discord-ext-cli",
classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
)