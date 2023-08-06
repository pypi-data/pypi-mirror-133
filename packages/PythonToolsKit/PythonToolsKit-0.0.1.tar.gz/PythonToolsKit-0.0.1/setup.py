import platform
import PyCommons as package
from subprocess import check_call, DEVNULL
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install


class PostDevelopScript(develop):
    def run(self):

        if platform.system() == "Windows":
            check_call(
                [
                    r"C:\WINDOWS\system32\reg.exe",
                    "add",
                    r"HKEY_CURRENT_USER\Console",
                    "/v",
                    "VirtualTerminalLevel",
                    "/t",
                    "REG_DWORD",
                    "/d",
                    "0x00000001",
                    "/f",
                ],
                stdout=DEVNULL,
                stderr=DEVNULL,
            )  # Active colors in console

        develop.run(self)


class PostInstallScript(install):
    def run(self):

        if platform.system() == "Windows":
            check_call(
                [
                    r"C:\WINDOWS\system32\reg.exe",
                    "add",
                    r"HKEY_CURRENT_USER\Console",
                    "/v",
                    "VirtualTerminalLevel",
                    "/t",
                    "REG_DWORD",
                    "/d",
                    "0x00000001",
                    "/f",
                ],
                stdout=DEVNULL,
                stderr=DEVNULL,
            )  # Active colors in console

        install.run(self)


setup(
    name="PythonToolsKit",
    version=package.__version__,
    packages=find_packages(include=[package.__name__]),
    install_requires=[],
    author=package.__author__,
    author_email=package.__author_email__,
    maintainer=package.__maintainer__,
    maintainer_email=package.__maintainer_email__,
    description=package.__description__,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url=package.__url__,
    project_urls={
        "Documentation Timeout": "https://mauricelambert.github.io/info/python/code/PyCommons/Timeout.html",
        "Documentation Terminal": "https://mauricelambert.github.io/info/python/code/PyCommons/Terminal.html",
        "Documentation StringF": "https://mauricelambert.github.io/info/python/code/PyCommons/StringF.html",
        "Documentation PrintF": "https://mauricelambert.github.io/info/python/code/PyCommons/PrintF.html",
        "Documentation Process": "https://mauricelambert.github.io/info/python/code/PyCommons/Process.html",
        "Documentation Logs": "https://mauricelambert.github.io/info/python/code/PyCommons/Logs.html",
        "Documentation GetPass": "https://mauricelambert.github.io/info/python/code/PyCommons/GetPass.html",
        "Documentation Encodings": "https://mauricelambert.github.io/info/python/code/PyCommons/Encodings.html",
        "Documentation DictObject": "https://mauricelambert.github.io/info/python/code/PyCommons/DictObject.html",
        "Documentation Report": "https://mauricelambert.github.io/info/python/code/PyCommons/Report.html",
        "Documentation urlopen": "https://mauricelambert.github.io/info/python/code/PyCommons/urlopen.html",
        "Documentation cleandict": "https://mauricelambert.github.io/info/python/code/PyCommons/cleandict.html",
    },
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.6",
    keywords=[
        "Timeout",
        "Terminal",
        "Colors",
        "Formatting",
        "Print",
        "Object",
        "Process",
        "CSV",
        "Logs",
        "Getpass",
        "Password",
        "Ask",
        "*",
        "Encodings",
        "Report",
        "Markdown",
        "HTML",
        "JSON",
    ],
    platforms=["Windows", "Linux", "MacOS"],
    license=package.__license__,
    cmdclass={
        "develop": PostDevelopScript,
        "install": PostInstallScript,
    },
)