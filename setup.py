from setuptools import find_packages, setup


setup(
    name="sqlai",
    version="1.0.0",
    description="SQLAI Core",
    url="http://github.com/nguyenduyminhthong/sqlai-core",
    author="Nguyen Duy Minh Thong",
    author_email="nguyenduyminhthong@gmail.com",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[line.strip() for line in open("requirements.txt").readlines()],
)
