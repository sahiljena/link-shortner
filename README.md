# link-shortner
This is a simple link shortner built with Flask and MongoDB, it also tracks the number of clicks and redirects from the link.
Check out the deployed link <a href="https://linnks.herokuapp.com/">here</a>

## Live Demo
<a href="https://linnks.herokuapp.com/">https://linnks.herokuapp.com/</a>

## Built With:
| Software/ Language | Version |
|----------|---------|
| Python | 3.8 |
| Flask | 2.0.0 |
| MongoDB Atlas | 4.4 |

## Features:

* ### Tracker
  * Number of clicks and redirects from the short link can be tracked
  
* ### Short Link Preview
  * Short links also comes with meta tags.
  
  
Project Organization
------------

    ├── README.md          <- The top-level README for developers using this project.
    │
    ├── requirements.txt   <- The requirements file for reproducing the environment
    │
    ├── Procfile           <- for heroku deployment
    │
    └── app.py             <- Main python app containing the flask app

## How to get started
To use this project, follow these steps:

* Make a `.env` file using the command `virtualenv env`
* Clone this repository 
```
git clone https://github.com/sahiljena/link-shortner.git
```
* Install dependencies 
```
pip install -r requirements.txt
```
* Run the App  `python app.py` or `flask run`
