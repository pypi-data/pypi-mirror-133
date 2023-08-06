## Version: 0.1.1

# dijkprofile-annotator description

Automatically annotate drijkprofile is qDAMEdit format

Author: Jonathan Gerbscheid <br>
Email: j.gerbscheid@hetwaterschapshuis.nl

# Online Tool
An web version of this tool is available at: 
[https://huggingface.co/spaces/jgerbscheid/dpa-example](https://huggingface.co/spaces/jgerbscheid/dpa-example)
<br>The availability of this tool is not currently guaranteed and it's location might change in the future to a different adress.

# Install
## Warning
This package will install pytorch to run the neural network for prediction. If you wish to use your own pytorch installation or modify the code in any way I recommend cloning the repository and installing locally:<br> [https://gitlab.com/hetwaterschapshuis/kenniscentrum/tooling/dijkprofile-annotator/-/tree/master/](https://gitlab.com/hetwaterschapshuis/kenniscentrum/tooling/dijkprofile-annotator/-/tree/master/) <br>
I recommended installing the package in a fresh conda environment to avoid conflicts with already other installed packages.

## Install directly from PiPI with pip
```
pip install dijkprofile-annotator
```

## Installing locally:
```
git clone git@gitlab.com:hetwaterschapshuis/kenniscentrum/tooling/dijkprofile-annotator.git
cd dijkprofile-annotator
pip install -e . 
```

# Usage
## basic
To annotate a single file, use the annotate function:
```
import dijkprofile_annotator

input_filepath = "/home/documents/surfacelines.csv"
target_filepath = "/home/documents/predicted_characteristpoints.csv"

dijkprofile_annotator.annotate(input_filepath, 
                               target_filepath)
```

## Detailed Exampes
See the example notebooks at:<br>[https://gitlab.com/hetwaterschapshuis/kenniscentrum/tooling/dijkprofile-annotator/-/tree/master/notebooks](https://gitlab.com/hetwaterschapshuis/kenniscentrum/tooling/dijkprofile-annotator/-/tree/master/notebooks) <br>for examples on how to use the package.

