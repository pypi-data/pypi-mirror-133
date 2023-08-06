import setuptools 

with open("README.md", "r", encoding="utf-8") as fh: 
   long_description = fh.read()

setuptools.setup(
   name = "Basic Data Science",
   version = "1.0",
   author = "Datamics",
   author_email = "saumya.goyal@datamics.com",
   description = "A small package - to extract basic information from csv file",
   long_description = long_description,
   long_description_content_type = "text/markdown",
   url = "https://github.com/user0000/package",
   classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
   ],
   package_dir={"": "src"},
   packages=setuptools.find_packages(where="src"),
   python_requires=">=3.6",
   install_requires=['pandas'],
) 