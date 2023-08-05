import setuptools

setuptools.setup(
    name="ez_aiohttp",
    version="0.0.1",
    author="Rukchad Wongprayoon",
    author_email="contact@biomooping.tk",
    short_description="The aiohttp easiest wrapper",
    description=open("README.md").read(),
    url="https://ez_request.rukchadisa.live",
    packages=["ez_rq"],
    package_dir={"ez_rq": "src/ez_rq"},
    install_requires=open("requirements.txt").readlines(),
    classifiers=[],
    
)