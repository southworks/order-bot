from setuptools import setup

setup(
   name='slack_adapter',
   version='1.0',
   description='An adapter to interact with Slack & the Bot Framework',
   author='SOUTHWORKS',
   author_email='manx@southworks.com',
   packages=['slack_adapter'],
   install_requires=['slackclient'],
)
