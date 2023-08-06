<div style="display : flex ; justify-content : center ;" align="center">

# Hasta

</div>

----------------------------------------------------

<div style="display : flex ; justify-content : center ;" align="center">

<!-- License -->
<a href="LICENSE.md">
    <img src="https://img.shields.io/badge/License-MIT-%23117a1a?style=for-the-badge&logo=opensourceinitiative" />
</a>

<!-- Python -->
<a href="https://www.python.org/downloads/release/python-399/">
    <img src="https://img.shields.io/badge/Python-3.9.9-blue?style=for-the-badge&logo=python" />
</a>

<!--Code Size-->
<a>
    <img src="https://img.shields.io/github/languages/code-size/anokidev/hasta?color=lightblue&logo=codesandbox&style=for-the-badge" />
</a>

<!--Downloads-->
<a>
    <img src="https://img.shields.io/github/downloads/anokidev/hasta/total?color=green&logo=github&style=for-the-badge" />
</a>

<!--Version-->
<a>
    <img src="" />

</div>

#### Table of contents :



1. [General](#general)
2. [Functions](#functions)
3. [Installation](#installation)
4. [Compabillity](#compabillity)
5. [Version](#version)
6. [Tasks](#tasks)
7. [Contributing](#contributing)
8. [License](#license)
9. [Troubleshooting](#troubleshooting)


----------------------------------------------------

#### General : <a id="general"></a>

A simple WSGI Server, implemented in CPython 3.9.9 .

----------------------------------------------------

#### Functions : <a id="functions"></a>

This software can :

- Handles HTTP request, one at a time.
- Fullfills Python WSGI specification.
- Supports Python web framework.

----------------------------------------------------

#### Installation : <a id="installation"></a>

**PIP :** 

```python

pip install hasta

```

----------------------------------------------------

#### Compabillity : <a id="compabillity"></a>

- Supports Python 3.9.9 .
- Doesn't support PyPy .

----------------------------------------------------

#### Version : <a id="version"></a>

- Current stable version : None.
- Current beta release : None.
- Current alpha release : None.
- Current pre-alpha release : v0.0.0 Pre - Alpha 2 ( SHORT NAME : v0.0.0-pa2 ) - [ BRANCH NAME : v0.0.0/pa2/r ] .

----------------------------------------------------

#### Tasks : <a id="task"></a>

Read [TASKS.md](/.github/NOTES/TASKS.md) for more info.

----------------------------------------------------

#### Contributing : <a id="contributing"></a>

Read [CONTRIBUTING.md](/.github/COMMUNITY/CONTRIBUTING.md) for more info.

----------------------------------------------------

#### License : <a id="license"></a>

Licensed in MIT License. Read [LICENSE.md](/LICENSE.md) for more info.

----------------------------------------------------

#### Troubleshooting : <a id="troubleshooting"></a>

**Command Not Found**

If the command throws a error :

```
zsh: command not found: pip # zsh
```

```
bash: command not found: pip # bash
```

```
'pip' is not recognized as an internal or external command,
operable program or batch file. # Windows
```

Then that means PIP is not installed. Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) , 
and then navigate to the download directory and then type this command :

```
python3 get-pip.py # MacOS, Linux, and UNIX
py get-pip.py # Windows
```

Some system package manager provides PIP, for example : 

Ubuntu :

```
sudo apt-get install python3-pip # Normal users.
apt-get install python3-pip # Root.
```

Arch Linux :

```
sudo pacman -S python-pip # Normal users.
pacman -S python-pip # Root.
```

For CentOS and RedHat, PIP is bundled with every single version of Python :

```
python3 -m ensurepip
```

For more problems, you can create an issue. Make sure you follow the tags rule ! Described in [TAGS.md](/.github/TAGS.md)
