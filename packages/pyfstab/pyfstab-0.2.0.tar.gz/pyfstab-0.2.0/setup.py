# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfstab']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyfstab',
    'version': '0.2.0',
    'description': 'Fstab parsing and formatting library',
    'long_description': '**MIT-licensed libary for parsing and creating fstab files**\n\n|pypi| |docs| |license|\n\nFeatures\n========\n\n* Unlike Canonical\'s fstab Python library, this actually works with Python 3\n  and does not have a cancerous license (GPLv3)\n* Small\n\nInstallation\n============\n\n:code:`pip3 install pyfstab`\n\nExamples\n========\n\n.. code:: python3\n   \n   # Import the classes\n   from pyfstab import Fstab\n\n   # Read the file\n   with open("/etc/fstab", "r") as f:\n       fstab = Fstab().read_file(f)\n\n   # List all devices/identifiers of fstab entries\n   for entry in fstab.entries:\n       print(entry.device)\n\n   # List all mountpoints of CIFS mounts\n   for entry in fstab.entries_by_type["cifs"]:\n       print(entry.dir)\n\n   # Print filesystem type for mount at /mnt/disk\n   print(fstab.entry_by_dir["/mnt/disk"].type)\n\n   # List all mount options for device UUID=123456\n   for entry in fstab.entries_by_device["UUID=123456"]:\n       print(entry.options)\n\n   # Print Tag value for all entries with device defined as\n   # UUID=something or ID=something\n   for entry in fstab.entries:\n       if entry.device_tag_type in {"UUID", "ID"}:\n           print(entry.device_tag_value)\n\n   # Change device tag type from UUID= to ID=\n   entry.device_tag_type = "ID"\n\n   # Change device tag value from "123456" to "4321"\n   # (Changes from "ID=123456" to "ID=4321")\n   entry.device_tag_value = "4321"\n\n   # Print new device string (it\'s "ID=4321" now)\n   print(entry.device)\n\n   # Set both tag type and value at the same time in both valid ways\n   entry.device = ("UUID", "11223344")\n   entry.device = "UUID=11223344"\n\n   # Add an entry (does not update entries_by_device/type/dir)\n   # but it will be printed when formatting the fstab object\n   fstab.entries.append(\n       Entry(\n           "/dev/sdg4",\n           "/mnt/disk",\n           "ext4",\n           "rw,relatime",\n           0,\n           0\n       )\n   )\n\n   # Remove all entries except ext*\n   fstab.entries = [\n       entry\n       for entry in fstab.entries\n       if entry.type.startswith("ext")\n   ]\n\n   # Print and write the formatted fstab file\n   formatted = str(fstab)\n   print(formatted)\n   with open("/etc/myfstab", "w") as f:\n       f.write(formatted)\n\nContributing\n============\n\n* Send any issues to GitHub\'s issue tracker.\n* Before sending a pull request, format it with `Black`_ (-Sl79)\n* Any changes must be updated to the documentation\n* All pull requests must be tested with tox (if you are using pyenv, add the installed versions for py35-py38 and pypy3 to .python-version at the root of this repository before running tox)\n\n\n.. _`Black`: https://github.com/psf/black\n\n.. |pypi| image:: https://img.shields.io/pypi/v/pyfstab.svg\n    :alt: PyPI\n    :target: https://pypi.org/project/pyfstab/\n.. |docs| image:: https://readthedocs.org/projects/pyfstab/badge/?version=latest\n    :alt: Read the Docs\n    :target: http://pyfstab.readthedocs.io/en/latest/\n.. |license| image:: https://img.shields.io/github/license/b10011/pyfstab.svg\n    :alt: License\n    :target: https://github.com/b10011/pyfstab/blob/master/LICENSE\n',
    'author': 'Niko Järvinen',
    'author_email': 'nbjarvinen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/b10011/pyfstab',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
