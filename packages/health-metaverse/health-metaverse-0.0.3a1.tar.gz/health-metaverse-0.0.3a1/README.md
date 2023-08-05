# Health Metaverse

A virtual 3D world framework for medical and health informatics applications

## Installation
```pip
pip install health-metaverse
```

## Examples

Example 1: Build a word cloud for Health Metaverse
```python
from healthmetaverse.wordcloud import HealthWordCloud
if __name__=="__main__":
    hwc = HealthWordCloud(data_path="metaverse-news.txt")
    hwc.show(save_figure="health_metaverse_wordcloud-small.jpg",figure_dpi=300)
```

Example 2: Build a topic model for Health Metaverse
```python
from healthmetaverse.topicmodel import *
import pickle
list_abstract=pickle.load(open("datasets/virtual reality and health.pickle","rb"))
start_to_build_topic_model(list_abstract=list_abstract,MAX_TOPICS=10,
                           MIN_PERC=0.8,export_html=True,
                           need_format=True,save_model=True)
```

The Official Health Metaverse Website is [here](https://health-metaverse.github.io/)

## License
The `health-metaverse` project is provided by [Donghua Chen](https://github.com/dhchenx). 

