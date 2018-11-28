from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent
readme = (here / "README.rst").read_text(encoding="utf-8")
changelog = (here / "CHANGELOG.rst").read_text(encoding="utf-8")

setup(
    name="epiweeks",
    version="1.0.0",
    description="Epidemiological weeks by US CDC and WHO calculation methods.",
    long_description=readme + "\n" + changelog,
    url="",
    project_urls={
        "Source Code": "https://github.com/dralshehri/epi-weeks",
        "Documentation": "https://epiweeks.readthedocs.io/en/latest",
    },
    author="Mohammed Alshehri",
    author_email="",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering",
        "Topic :: Utilities",
    ],
    keywords="epidemiology epi weeks date calendar cdc who",
    py_modules=[module.stem for module in here.glob("src/*.py")],
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.5",
)
