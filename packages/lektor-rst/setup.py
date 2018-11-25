from setuptools import setup


setup(
    name="lektor-rst",
    description="Adds reStructuredText support to Lektor.",
    version="0.1",
    author="H. Turgut Uyar",
    author_email="uyar@tekir.org",
    url="http://github.com/uyar/lektor-rst",
    license="MIT",
    install_requires=["bs4", "docutils", "pygments", "pytidylib"],
    py_modules=["lektor_rst"],
    entry_points={"lektor.plugins": ["rst = lektor_rst:RstPlugin"]},
)
