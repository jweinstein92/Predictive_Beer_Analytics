Predictive Beer Analytics
========================

Predictive Beer Analytics is a project that aims to 
gather, process, and present beer data in such a way that
the user can find out based on the desired characteristics of the beer where in the world that  
particular beer is enjoyed. Other fun tools for beer marketing is also included such as color 
and word rating analyser.

## Authors

Josh Weinstein
Jim Sundkvist
Marek Kühn

## Whats included
Within the project you'll find the following directories:

```
Predictive_Beer_Analytics/
├── app/
├── docs/
├── machine_learning/
│   ├── data/
│	├── graphics/
│   └── lib/
└── static/
    ├── css
    ├── images
    └── js
```
In the app directory you will find the project's Django project that is used as a GUI for the mined and processed data.
In the docs directory you will find the projects documentation.
In the machine_learning directory you will find the data mining and machine learning scripts as well as sample data.
In the static directory you will find css, images, and javascript files that are used in the Django web application.

## Documentation

Predictive Beer Analytics documentation is included in the project, under the docs directory.
Or can be accessed [here](http://www.predictive-beer-analytics.readthedocs.org)

## Dependencies
```
argparse>=1.2
jsonpickle>=0.8
nltk>=3.0
matplotlib>=1.4.2
numpy>=1.9.0
scikit-learn>=0.15.2
scipy>=0.14.0
sphinx>=1.2.3
django>=1.7.0
mysql>=5.6.22
```

## Usage
See [documentation](http://www.predictive-beer-analytics.readthedocs.org)

## Contact
Josh Weinstein: joshweinstein92@gmail.com
Marek Kühn: kuhnm@centrum.cz
Jim Sundkvist: jimsudket@gmail.com
## Acknowledgements
Thanks to [Untappd.com](https://untappd.com/) for allowing us to mine the data necessary to bring this project about.