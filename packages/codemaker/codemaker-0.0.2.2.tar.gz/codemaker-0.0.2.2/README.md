# codemaker
Utils to easily generate code, speed up your workflow.
# Usage


### quick start

```shell
# Assume we are going to create a python package (which can be uploaded to pypi.org adn be installed using pip) named foopkg
# 1. Export the template files for a normal python package project.
pip3 install codetmpl
codetmpl export pypkg foopkg
# 2. Edit file foopkg/maker.yml, fill in some information such as author and package name
# 3. Make your project code from template, 
cd foopkg
codemaker make
```


