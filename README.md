<div id="top"></div>
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">A Django App</h3>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

We're a trading company and we love cryptocurrencies. We want to give feedback to our users about the value of their portfolios and for that we need to know the price of each cryptocurrency at any given time. For this we have developed a rest api that will be consumed by different applications, webs and mobiles.

<p align="right">(<a href="#top">back to top</a>)</p>


### Built With

* [Django](https://www.djangoproject.com/)
* [Django Rest Framework](https://www.django-rest-framework.org/)
* [Celery](https://docs.celeryproject.org/en/stable/index.html)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Installation

This is an example of how to list things you need to use the software and how to install them.
1. create a virtualenv
  ```sh
  python3 -m venv currencies-env
  ```

2. load virtualenv
  ```sh
  source currencies-env/bin/activate
  ```

3. clone this repo
  ```sh
  git clone git@github.com:sanjmen/currencies
  ```

4. change to repo
  ```sh
  cd currencies
  ```

5. install requirements
  ```sh
  pip install -r requirements.txt
  ```

6. migrate database
  ```sh
  ./manage.py migrate
  ```

7. migrate database
  ```sh
  ./manage.py migrate
  ```

8. run server
  ```sh
  ./manage.py runserver
  ```

7. in other terminal run celery
  ```sh
  celery -A apps.taskapp worker -B -l INFO
  ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

1. You can browse the api with the browser
    * open a browser at [http://127.0.0.1:8000/api/v1/](http://127.0.0.1:8000/api/v1/)
    * then you could navigate to markets and klines

2. You can consume it with curl or using your favourite http client

<p align="right">(<a href="#top">back to top</a>)</p>
