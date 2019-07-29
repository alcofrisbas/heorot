import setuptools
setuptools.setup(name='heorot',
      version='0.1',
      packages=setuptools.find_packages(),
      entry_points={
        "console_scripts": [
            'heorot-create = heorot.create:main'
        ]
      }
    )