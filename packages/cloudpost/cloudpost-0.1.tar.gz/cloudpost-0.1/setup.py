from setuptools import setup
setup(
  name = 'cloudpost',
  packages = [
    'cloudpost', 
    "cloudpost.depres",
    "cloudpost.collector", 
    "cloudpost.cli",
    "cloudpost._deploy.gcp",
    "cloudpost._deploy.local",
    "cloudpost._backends.gcp",
    "cloudpost._backends.local",
  ],
  version = '0.1',
  description = 'A tool which enables to construct your serverless infrastructure in Python code.',
  author = 'Stefan Nozinic and Nikola Bebic',
  url = 'https://github.com/lambda-lab/cloudpost',
  download_url = 'https://github.com/lambda-lab/cloudpost/tarball/0.1',
  keywords = ['web', 'IaaC', 'cloud'],
  entry_points = {
    "console_scripts": [
      "cloudpost = cloudpost"
    ]
  }
)