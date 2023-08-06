import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='magic_dao',
     version='0.0.1',
     author="Peng Xiong",
     author_email="xiongpengnus@gmail.com",
     description="Magic commands used in NUS DAO classes",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/XiongPengNUS/magic_dao",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
 )
