from setuptools import setup, find_packages

setup(name='dijkprofile_annotator',
      version='0.1.0',
      description='Automatically annotate drijkprofile in qDAMEdit format',
      long_description_content_type='text/markdown',
      long_description=open('README.md').read(),
      url='',
      project_urls={
            "Bug Tracker": "https://gitlab.com/hetwaterschapshuis/kenniscentrum/tooling/dijkprofile-annotator/-/issues"
      },
      author='Jonathan Gerbscheid',
      author_email='j.gerbscheid@hetwaterschapshuis.nl',
      license='MIT',
      package_dir={"": "dijkprofile_annotator"},
      packages=find_packages(where='dijkprofile_annotator'),
      zip_safe=False,
      python_requires='>=3.6',
      install_requires=["joblib>=1.1.0",
                        "matplotlib>=3.4.3",
                        "numpy>=1.21.4",
                        "Pillow>=8.4.0",
                        "scikit_learn>=1.0.1",
                        "seaborn>=0.11.2",
                        "torch>=1.9.0",
                        "tqdm"]
      )
