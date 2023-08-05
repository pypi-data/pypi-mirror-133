from distutils.core import setup
setup(
  name = 'afterrealism',
  packages = ['afterrealism'],
  version = '0.1',
  description = 'deep learning tool kit',
  author = 'afterrealism',
  author_email = 'afterrealism@gmail.com',
  url = 'https://github.com/afterrealism/afterrealism',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/afterrealism/afterrealism/archive/v_01.tar.gz',
  keywords = ['deeplearning'],
  install_requires=['numpy'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3.7',
  ],
)
