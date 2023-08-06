from distutils.core import setup
setup(
  name = 'lipycense',         # How you named your package folder (MyLib)
  packages = ['lipycense'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='GPL-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = "Helps you find out how your project's dependencies are licensed.",   # Give a short description about your library
  author = 'Aiman Al Masoud',                   # Type in your name
  author_email = 'luxlunarislabs@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/aiman-al-masoud/lipycense',   # Provide either the link to your github or to your website
  
  download_url = 'https://github.com/aiman-al-masoud/lipycense/archive/refs/tags/v_01.tar.gz',    # I explain this later on
  keywords = ['license', 'python', 'packages'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)', # Again, pick a license
    'Programming Language :: Python :: 3.8', #Specify which pyhton versions that you want to support
  ],
)