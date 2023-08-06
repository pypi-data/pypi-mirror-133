import setuptools

setuptools.setup(
    name="ez_aiohttp",
    version="0.1.0",
    author="Rukchad Wongprayoon",
    author_email="contact@biomooping.tk",
    description="Make aiohttp easier",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://ez-aiohttp.rukchadisa.live/en/latest/",
    packages=["ez_rq"],
    package_dir={"ez_rq": "src/ez_rq"},
    install_requires=open("requirements.txt").readlines(),
    classifiers=[],
    
)