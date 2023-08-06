blpdecode
=========

![Image](https://img.shields.io/github/license/rstms/blpdecode)

![Image](https://img.shields.io/pypi/v/blpdecode.svg)

![Image](https://circleci.com/gh/rstms/blpdecode/tree/master.svg?style=shield)

![Image](https://readthedocs.org/projects/blpdecode/badge/?version=latest)

![Image](https://pyup.io/repos/github/rstms/blpdecode/shield.svg)

Barracuda LinkProtect Decoder

Barracuda's email security filter product includes a feature which dynamically replaces each URL in the message body with an encoded URL that proxies through a realtime filtering API hosted at linkprotect.cudasvc.com.  The LinkProtect feature is certainly helpful in mitigating 'phishing' attempts.  However, the obfuscated 'hover' text can be annoying to advanced users wishing to observe link URLs in the course of reviewing mail messages.

This program aims to decode these links in order to analyze or deference them directly.  

* Free software: MIT license
* Documentation: [https://blpdecode.readthedocs.io](https://blpdecode.readthedocs.io)

CLI
---
```
Usage: blpdecode [OPTIONS] ENCODED_URL

Options:
  --version    Show the version and exit.
  -d, --debug  debug mode
  --help       Show this message and exit.
```



Credits
-------

This package was created with Cookiecutter and `rstms/cookiecutter-python-cli`, a fork of the `audreyr/cookiecutter-pypackage` project template.

- [Cookiecutter](https://github.com/audreyr/cookiecutter)
- [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
- [rstms/cookiecutter-python-cli](https://github.com/rstms/cookiecutter-python-cli)
