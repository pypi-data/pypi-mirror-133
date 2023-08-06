# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['clifun']
setup_kwargs = {
    'name': 'clifun',
    'version': '0.0.2',
    'description': 'Construct a comand line interface based on a function or class',
    'long_description': '# clifun\n\nBecause cli\'s should be fun(ctions) ;).\n\n```\nimport clifun\n\ndef my_program(a: int, b: str = "not provided"):\n  print(f"Running some code with: a={a}, b={b}")\n\nif __name__ == "__main__":\n  clifun.call(my_program)\n```\n\nThat\'s all it takes. Clifun will inspect your function and collect the values it needs it from command line arguments, environment variables, or config files, and then call it.\n\n```\npython examples/function --a 1\n```\n```\nRunning some code with: a=1, b=not provided\n```\n\nYou can even run functions in any module without modifying the module at all\n\n```\npython clifun.py examples/module.py my_program --a 1\n```\nif you have the code checked out. Or if you pip installed\n\n```\npython -m clifun some_module.py function ...\n```\n\nOr if you have environment variables defined\n\n```\nexport A=1\nexport B=hi\npython example.py\n```\nagain yields without you having to provide values\n```\nBasic(a=1, b=\'hi\')\n```\n\n`clifun` also supports nested objects (or functions taking complex objects as inputs)\n\n```\nfrom typing import Optional\nimport datetime as dt\n\nimport attr\nimport clifun\n\n\n@attr.s(auto_attribs=True, frozen=True)\nclass Foo:\n    a: dt.datetime\n    b: Optional[str] = None\n\n\n@attr.s(auto_attribs=True, frozen=True)\nclass Bar:\n    f: Foo\n    c: int\n\ndef my_program(f: Foo, c: int):\n    print(Bar(f, c))\n\n\nif __name__ == "__main__":\n    bar = clifun.call(my_program)\n```\n\nYou specify values for the fields in the nested class by referring to them with a their field name in the outer class\n\n```\npython examples/advanced.py --c 1 --f.a 2020-01-01 --f.b hi\n```\n```\nBar(f=Foo(a=datetime.datetime(2021, 1, 1, 0, 0), b=\'hi\'), c=1)\n```\n\nYou can also supply one or more `json` formatted `config` files. Provide the name(s) of these files as positional arguments. `clifun` will search them, last file first, for any keys fields that are not provided at the command line before searching the environment.\n\n```\npython examples/advanced.py --c 1 examples/foo.json\n```\n```\nBar(f=Foo(a=datetime.datetime(2021, 1, 1, 0, 0), b=\'str\'), c=1)\n```\n\n`clifun` is inspired by [clout](https://github.com/python-clout/clout), but I wanted to try being a bit more opinionated to make both the library and code using it simpler.\n\n\n',
    'author': 'Tom Dimiduk',
    'author_email': 'tom@dimiduk.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
