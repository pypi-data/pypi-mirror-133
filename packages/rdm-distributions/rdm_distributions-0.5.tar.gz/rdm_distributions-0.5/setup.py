from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
	
setup(name='rdm_distributions',
      version='0.5',
	  description='Gaussian and Binomial distributions (basics)',
	  long_description=long_description,
	  long_description_content_type="text/markdown",
	  packages=['rdm_distributions'],
	  author='Roberto De Monte',
	  author_email='roberto.de.monte5@gmail.com',
	  zip_safe=False)
