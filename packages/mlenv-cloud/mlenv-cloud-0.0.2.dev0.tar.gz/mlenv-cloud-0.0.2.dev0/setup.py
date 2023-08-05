"""Setup script."""
import importlib
import os
import types
import dependencies

from setuptools import find_packages
from setuptools import setup

relative_directory = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
loader = importlib.machinery.SourceFileLoader(
    fullname="version",
    path=os.path.join(relative_directory, "mlenv_cloud/version.py"),
)
version = types.ModuleType(loader.name)
loader.exec_module(version)

setup(
    name="mlenv-cloud",
    version=version.__version__,
    description="The MLEnv repository provides APIs that will allow "
    "to easily create Docker container using local dependencies",
    url="https://github.com/gogasca/mlenv",
    author="The MLEnv authors",
    author_email="gascagonzalo@gmail.com",
    license="Apache License 2.0",
    extras_require={"tests": dependencies.make_required_test_packages()},
    include_package_data=True,
    install_requires=dependencies.make_required_install_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    package_dir={
        "mlenv_cloud": os.path.join(relative_directory, "mlenv_cloud")
    },
    packages=find_packages(where=relative_directory),
)