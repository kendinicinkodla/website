from setuptools import setup


setup(
    name="lektor-htu",
    description="Personal tweaks to generated HTML.",
    version="0.1",
    author=u"H. Turgut Uyar",
    author_email="uyar@tekir.org",
    url="http://github.com/uyar/lektor-htu",
    license="LGPL",
    install_requires=["lxml"],
    py_modules=["lektor_htu"],
    entry_points={"lektor.plugins": ["htu = lektor_htu:HTUPlugin"]},
)
