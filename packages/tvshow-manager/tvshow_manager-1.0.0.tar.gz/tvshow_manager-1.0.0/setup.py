from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name="tvshow_manager",
      version="1.0.0",
      author="Sven Speckmaier",
      license="MIT",
      url='https://github.com/svensp/next_episode',
      download_url='https://github.com/svensp/next_episode/archive/refs/tags/1.0.0.tar.gz',
      packages=find_packages(where="src"),
      description="console commands to turn video folders into kodi importable tv seriesj",
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=[
          'uuid'
      ],
      package_dir={"": "src"},
      keywords=[
          'kodi'
      ],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      scripts=[
          'bin/next-episode',
          'bin/next-season',
          'bin/remove-episode',
          'bin/fill-episode',
          'bin/generate-nfo',
          'bin/generate-show-nfo',
          'bin/next-artwork',
               ]
      )