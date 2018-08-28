from setuptools import setup

setup(name='bahnbusiness',
      description='Scrape the bahn.de business website for tickets and other information.',
      author='uberspace.de',
      author_email='hallo@uberspace.de',
      url='https://github.com/uberspace/bahnbusiness',
      version='1.2.0',
      license='MIT',
      packages=[
        'bahnbusiness',
      ],
      zip_safe=True,
      install_requires=[
          'beautifulsoup4==4.6.0',
          'requests==2.18.*',
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Information Technology',
          'Intended Audience :: Developers',
          'Topic :: Office/Business',
          'Topic :: Utilities',
          'Natural Language :: English',
          'Operating System :: POSIX :: Linux',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: 3.6',
      ],
)
