import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'Aly_facts',
  packages = ['Aly_facts'],
  version = '1.0',
  license='MIT',
  description = 'A package that provides facts about an user on discord with the name of entity_night aka Aly aka Alyssa',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'NotFaizen',
  author_email = 'munavir370@gmail.com',
  url = 'https://github.com/NotFaizen/Aly_facts',
  keywords = ["aly", "aly.py", "aly_facts", "facts"],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)