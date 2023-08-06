from setuptools import setup, find_packages

setup(name='dijkprofile_annotator',
      version='0.1.5',
      description='Automatically annotate dijkprofiles in qDAMEdit format',
      long_description_content_type='text/markdown',
      long_description=open('README.md').read(),
      url='https://gitlab.com/hetwaterschapshuis/kenniscentrum/tooling/dijkprofile-annotator',
      project_urls={
            "Bug Tracker": "https://gitlab.com/hetwaterschapshuis/kenniscentrum/tooling/dijkprofile-annotator/-/issues",
            "Source Code": "https://gitlab.com/hetwaterschapshuis/kenniscentrum/tooling/dijkprofile-annotator/-/tree/master",
      },
      author='Jonathan Gerbscheid',
      maintainer='Jonathan Gerbscheid',
      author_email='j.gerbscheid@hetwaterschapshuis.nl',
      maintainer_email='j.gerbscheid@hetwaterschapshuis.nl',
      license='MIT',
      packages=['dijkprofile_annotator',
                "dijkprofile_annotator.utils", 
                "dijkprofile_annotator.app",
                "dijkprofile_annotator.models", 
                "dijkprofile_annotator.training", 
                "dijkprofile_annotator.preprocessing",
                "dijkprofile_annotator.datasets"],
      zip_safe=False,
      python_requires='>=3.6',
      install_requires=["joblib>=1.1.0",
                        "numpy>=1.21.4",
                        "Pillow>=8.4.0",
                        "scikit_learn>=1.0.1",
                        "torch>=1.9.0",
                        "matplotlib>=3.4.3",
                        "seaborn",
                        "tqdm",
                        "Jinja2>=3.0",
                        "gradio"],
      extras_require={
        'interactive': ["jupyter"],
      },
      entry_points={
            'console_scripts': [
                  'dijkprofile_annotator-gui=dijkprofile_annotator.app:run',
                  'dijkprofile_annotator=dijkprofile_annotator.__main__:main']
      },
      package_data={'dijkprofile_annotator': ['data/trained_models/*.pt', 'data/trained_models/*.pik']}
      )
