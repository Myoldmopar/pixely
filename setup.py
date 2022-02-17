from setuptools import setup, find_packages
setup(
    name="Pixely",
    version="0.1",
    packages=find_packages(),
    scripts=['pixely/applications/run_doctor_strange.py'],
    author="Me",
    author_email="me@me.com",
    description="Handling LED operations for costumes driven by Raspberry Pi",
    license="PSF",
    keywords="raspberry pi pixel led strip cosplay",
    url="http://github.com/Myoldmopar/pixely",   # project home page, if any
)
