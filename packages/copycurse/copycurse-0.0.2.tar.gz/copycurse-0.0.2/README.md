![Version 1.0](http://img.shields.io/badge/version-v0.0.2-green.svg)
![Python 3.10](http://img.shields.io/badge/python-3.10-blue.svg)
[![MIT License](http://img.shields.io/badge/license-MIT%20License-blue.svg)](https://github.com/0xrytlock/copycurse/blob/main/LICENSE)

CopyCurse is a simple tool for recursively copying files from one directory to another.

## Installation

Windows:
`pip install copycurse`

Linux:
`pip3 install copycurse`

## Usage

`copycurse source destination [--version] [-h]`

| Arguments         | Description                       |
|-------------------|-----------------------------------| 
| source            | Source directory [Default=.]      | 
| destination       | Destination directory             |
| --version         | Show version and exit             |
| -h, --help        | Show help and exit                |

## Examples

**Copy from your current directory:**

`copycurse . C:\directory`

**Copy from directory to another directory:**

`copycurse C:\directory D:\directory`

**Copy from your current directory to network share:**

`copycurse . \\192.168.1.1\directory`