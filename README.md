# pp.lv WEB Scraper

![My Image](pictures/spider_logo.png)

## Task:

The task involved utilizing the Scrapy framework to gather information about cars from the pp.lv website. The information targeted includes details such as the brand, model, year (if available), mileage, VIN (if available), and plate number (if available).

- Brand
- Model
- Year (if exist)
- Mileage
- VIN (if exist)
- Plate number (if exist)

## About project

To tackle this task, I leveraged API endpoints obtained from the website. I then developed a web spider using the Scrapy framework, designed to efficiently scrape through these API endpoints. This approach ensured systematic extraction of the desired car information, contributing to an active and ongoing project development on the repository.

## Install

In order to install spider type in to your terminal:

```
git clone git@github.com:Alg1mantas/Scraping.git
```

and also don't forget to install libraries:

```
pip install -r requirements.txt
```

## How to use it?

At first, navigate your terminal to pp_lv directory and type:

```
scrapy crawl cars
```

After about five minutes ( depends on how much of pages of data exist) you will get a file named: pp_lv.csv as an output. In file you will find all nessesary data about cars on website.

![My Image](pictures/dataset.PNG)

## Happy scraping!
