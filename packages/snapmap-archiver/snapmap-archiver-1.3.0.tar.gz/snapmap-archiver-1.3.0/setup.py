# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snapmap_archiver', 'snapmap_archiver.utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'snapmap-archiver',
    'version': '1.3.0',
    'description': 'Download all Snapmaps content from a specific location.',
    'long_description': '# snapmap-archiver\n\nA tool written in Python to download all Snapmaps content from a specific location.\n\n![snapmap-archiver splash](/.github/img/Splash.png)\n\n## Setup\n\n`pip3 install snapmap-archiver`\n\n[View on PyPI](https://pypi.org/project/snapmap-archiver/)\n\nInstall dependencies with `pip3`.\n\n```sh\npip3 install -r requirements.txt\n```\n\n### Install [aria2c](http://aria2.github.io/)\n\nDownload `aria2c` from here:\n\n[https://aria2.github.io/](https://aria2.github.io/)\n\nThis is the downloader used for the fastest Snap download speeds.\n\n## Usage\n\n```sh\npython3 -m snapmap_archiver -o [OUTPUT DIR] -l="[LATITUDE],[LONGITUDE]"\n```\nUnfortunately you have to use the arbitrary `-l="lat,lon"` rather than just `-l "lat,lon"` when parsing negative numbers as `argsparse` interprets said numbers as extra arguments.\n\n### Optional Arguments\n\n#### Location\n\n`-l` is not required if an input file or Snap URL is provided. It can also be used multiple times to download Snaps from multiple locations in one command.\n\nE.g\n\n```sh\npython3 -m snapmap_archiver -o ~/Desktop/snap -l=\'123.123,123.123\' -l \'445.445,445.445\'\n```\n\n#### Input File\n\nWith `-t`, you can specify a file containing a list of line-separated Snap URLs or IDs.\n\nE.g\n\n```sh\npython3 -m snapmap_archiver -o ~/Desktop/snap -t ~/snaps.txt\n```\n\nInside `snaps.txt`:\n\n```\nhttps://map.snapchat.com/ttp/snap/Example/@-33.643495,115.741281,11.86z\nExample\nhttps://map.snapchat.com/ttp/snap/Example/\nhttps://map.snapchat.com/ttp/snap/Example/\n```\n\n#### Snap URL\n\nYou can also just pass 1 or more normal Snap URLs to the package to download it individually like this:\n\n```sh\npython3 -m snapmap_archiver -o ~/Desktop/snap \'https://map.snapchat.com/ttp/snap/Example/@-33.643495,115.741281,11.86z\'\n```\n\n#### Export JSON\n\nYou can export a JSON file with info about downloaded snaps with the `--write-json` argument, which will contain information like the time the Snap was posted, and the Snap location.\n\n#### Snap Radius\n\nThe radius from the coordinates you provide that will be included for downloads. `-r 20000` will download all Snaps within a 20km radius of your coordinates.\n\n#### No Overlay\n\nBy default the script merges the video and the overlay file into one file. With the `--no-overlay` argument you can disable this and only download the raw video.  \n',
    'author': 'king-millez',
    'author_email': 'Millez.Dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
