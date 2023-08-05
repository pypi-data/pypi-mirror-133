# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leetit', 'leetit.leetit', 'leetit.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'leetit',
    'version': '31.3.373',
    'description': '1337 translator lib',
    'long_description': '# leetit\n1337 translator lib\n\n# Instalation\n```\n$ pip install leetit\n```\n\n# Usage\nSimple example:  \n```Py\nimport leetit\n \nprint(leetit.leet("xacker"))\nprint(leetit.leet("xacker", seed=12345, percent=30))\n```\n\n# Transformations\nIn order to get a leetspeak from ordinary English, you need to make three transformations:  \nFirst you need to replace words and phrases with slang acronyms like "nice one" => "n1" or "owned" => "pwnd". To do this, the leetit library provides the `acronyms` function, which accepts text and an optional seed for the PRNG.\n```Py\nimport leetit\n\nprint(leetit.acronyms("yeah, easy"))\nprint(leetit.acronyms("yeah, easy"), seed=12345)\n```\nSecondly, you need to change the morphology of words, for example, replacing the suffixes **-er** and **-or** with **-xor** or **-zor**. To do this, the leetit library provides the `morphology` function.  \n```Py\nimport leetit\n\nprint(leetit.morphology("xacker"))\nprint(leetit.morphology("xacker"), seed=12345)\n```\nThirdly, you need to replace all or some of the characters with others similar to them in various ways, for example, **e** can be replaced with **3** or **&**.  To do this, the `substitution` function is provided. In addition to text, this function can also accept the following parameters:  \n1) The "seed" parameter accepts the seed for the rng.\n2) The "percent" parameter specifies which part of the letters will be changed.\n3) The "alphabet" parameter accepts a dictionary describing the rules for replacing letters (about dictionaries below).\n4) The "chars" parameter accepts a list of letters for which replacement will be performed. By default, all Latin letters are included in this list.\n\n## Alphabets\nAlphabets are dictionaries in which lowercase letters act as the key, and arrays with characters with which this letter can be replaced as the value.  \nThe leetit library provides several alphabets out of the box:  \n- leetit.ALPHABET_NUMBERS - contains options for replacing letters with numbers. For example, **e** to **3**.\n- leetit.ALPHABET_ASCII - contains everything that is in leetit.ALPHABET_NUMBERS, and in addition options for replacing letters with other letters and combinations of letters and numbers. For example, **e** to **&**.\n- leetit.ALPHABET_UNICODE_ONLY - contains options for replacing latin letters with special characters and letters of other languages.\n- leetit.ALPHABET_UNICODE - contains a union of leetit.ALPHABET_ASCII and leetit.ALPHABET_UNICODE_ONLY\n\nYou can also compose your alphabets.\n\n```Py\nimport leetit\n\nprint(leetit.substitution("To be, or not to be, that is the question"))\nprint(leetit.substitution("To be, or not to be, that is the question"), seed=12345)\nprint(leetit.substitution("To be, or not to be, that is the question"), percent=100, alphabet=leetit.ALPHABET_NUMBERS)\nprint(leetit.substitution("To be, or not to be, that is the question"), percent=100, alphabet=leetit.ALPHABET_ASCII)\nprint(leetit.substitution("To be, or not to be, that is the question"), percent=100, alphabet=leetit.ALPHABET_UNICODE_ONLY)\nprint(leetit.substitution("To be, or not to be, that is the question"), percent=100, alphabet=leetit.ALPHABET_UNICODE)\n\nMY_ALPHABET = {\n  "e": ["eeeeeeee"],\n  "o": ["oooooooo"],\n}\n\nprint(leetit.substitution("To be, or not to be, that is the question"), percent=100, alphabet=MY_ALPHABET)\n```\n\nAnd finally, the leetit library provides a `leet` function that performs all three transformations on the text in turn:  \n```Py\ndef leet(text: str, seed: int = 1337, percent:int = 50, alphabet = ALPHABET_ASCII, chars = string.ascii_lowercase) -> str\n```\n```Py\nimport leetit\n \nprint(leetit.leet("To be, or not to be, that is the question"))\n```\n',
    'author': 'DomesticMoth',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DomesticMoth/leetit',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
