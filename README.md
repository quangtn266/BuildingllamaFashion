# Buidling llama Fashion

A end to end demo builds a llama model with fashion data (Routine) is a local branch in Vietnam.

## Tasks
1) A script scrapes Routine's data (a fashion data) in Vietnam.
2) Building a llama model with fashion data.
3) Testing model.
4) Run application by streamlit.

## Structure of data:
1) 'Link': Link of item.
2) 'Category_Type': Target gender,
3) 'Image Front': Front Image link,
4) 'Image Back': Back Image link,
5) 'Product_ID': Product Id,
6) 'Description': Product description,
7) 'Price': Product Price,
8) 'Brand': Product brand.

A csv format.

![image](https://github.com/quangtn266/RoutineScrapeData/assets/50879191/8316c3c9-2aed-46ac-9ff8-eb45993cced4)

## Scraping data

```
python data/database_scrape.py
```

## Training llama
- In the demo, I already use TinyPixel/small-llama2 (https://huggingface.co/TinyPixel/small-llama2)

```
python train.py
```

## Inference

```
python inference.py
```

## Running application.

```
streamlit run app.py
```


