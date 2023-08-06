from distutils.core import setup
setup(
  name = 'cppfunctions',         # How you named your package folder (cppfunctions)
  packages = ['cppfunctions'],   # Chose the same as "name"
  version = '2.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'My attempt to bring c/c++ functions to python',   # Give a short description about your library
  author = 'Shamyak',                   # Type in your name
  author_email = 'sj907822@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/ShamyakGoel/cppfunctions/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/ShamyakGoel/cppfunctions/archive/refs/tags/v_20.tar.gz',    # I explain this later on
  keywords = ['c++functions', 'cfunctions'],   # Keywords that define your package best
  install_requires=[],
  long_description_content_type="text/x-rst",
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license 
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3',
  ],
)