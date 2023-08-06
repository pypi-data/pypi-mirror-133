# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['biopeaks', 'biopeaks.benchmarks', 'biopeaks.tests']

package_data = \
{'': ['*'], 'biopeaks': ['images/*'], 'biopeaks.tests': ['testdata/*']}

install_requires = \
['PySide6>=6.2.2',
 'matplotlib>=3.5.0',
 'numpy>=1.21.4',
 'pandas>=1.3.4',
 'scipy>=1.7.3']

extras_require = \
{'pyinstaller': ['pyinstaller>=4.7']}

entry_points = \
{'console_scripts': ['biopeaks = biopeaks.__main__:main']}

setup_kwargs = {
    'name': 'biopeaks',
    'version': '1.4.3',
    'description': 'A graphical user interface for feature extraction from heart- and breathing biosignals.',
    'long_description': '<img src="https://github.com/JanCBrammer/biopeaks/raw/master/docs/images/logo.png" alt="logo" style="width:600px;"/>\n\n![GH Actions](https://github.com/JanCBrammer/biopeaks/workflows/test/badge.svg?branch=dev)\n[![codecov](https://codecov.io/gh/JanCBrammer/biopeaks/branch/master/graph/badge.svg)](https://codecov.io/gh/JanCBrammer/biopeaks)\n[![DOI](https://www.zenodo.org/badge/172897525.svg)](https://www.zenodo.org/badge/latestdoi/172897525)\n[![PyPI version](https://img.shields.io/pypi/v/biopeaks.svg)](https://pypi.org/project/biopeaks/)\n[![JOSS](https://joss.theoj.org/papers/10.21105/joss.02621/status.svg)](https://doi.org/10.21105/joss.02621)\n\n\n# General Information\n\n`biopeaks` is a straightforward graphical user interface for feature extraction from electrocardiogram (ECG), photoplethysmogram (PPG) and breathing biosignals.\nIt processes these biosignals semi-automatically with sensible defaults and offers the following functionality:\n\n+ processes files in the open biosignal formats [EDF](https://en.wikipedia.org/wiki/European_Data_Format), [OpenSignals (Bitalino)](https://bitalino.com/en/software)\nas well as plain text files (.txt, .csv, .tsv)\n+ interactive biosignal visualization\n+ biosignal segmentation\n+ benchmarked, automatic extrema detection (R-peaks in ECG, systolic peaks in PPG, exhalation troughs and inhalation\npeaks in breathing signals) with signal-specific, sensible defaults\n+ automatic state-of-the-art [artifact correction](https://www.tandfonline.com/doi/full/10.1080/03091902.2019.1640306)\n for ECG and PPG extrema\n+ manual editing of extrema\n+ extraction of instantaneous features: (heart- or breathing-) rate and period, as well as breathing amplitude\n+ .csv export of extrema and instantaneous features for further analysis (e.g., heart rate variability)\n+ automatic analysis of multiple files (batch processing)\n\n\n![GUI](https://github.com/JanCBrammer/biopeaks/raw/master/docs/images/screenshot_statistics.png)\n\n\n# Installation\n\n`biopeaks` can be installed from PyPI:\n\n```\npip install biopeaks\n```\n\nAlternatively, on Windows, download [biopeaks.exe](https://github.com/JanCBrammer/biopeaks/releases/latest)\nand run it. Running the executable does not require a Python installation.\n\nYou can find more details on the installation [here](https://jancbrammer.github.io/biopeaks/installation.html).\n\n\n# Documentation\n\nHave a look at the [user guide](https://jancbrammer.github.io/biopeaks/user_guide.html) to get started with `biopeaks`.\n\n\n# Contributors welcome!\n\nImprovements or additions to the repository (documentation, tests, code) are welcome and encouraged.\nSpotted a typo in the documentation? Caught a bug in the code? Ideas for improving the documentation,\nincrease test coverage, or adding features to the GUI? Get started with the [contributor guide](https://jancbrammer.github.io/biopeaks/contributor_guide.html).\n\n\n# Citation\n\nPlease refer to the [biopeaks paper](https://joss.theoj.org/papers/10.21105/joss.02621) in The Journal of Open Source Software.\n\n\n# Changelog\n\nHave a look at the [changelog](https://jancbrammer.github.io/biopeaks/changelog.html) to get an overview of what has changed throughout the versions of `biopeaks`.\n\n\n\n\n',
    'author': 'Jan C. Brammer',
    'author_email': 'jan.c.brammer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JanCBrammer/biopeaks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
