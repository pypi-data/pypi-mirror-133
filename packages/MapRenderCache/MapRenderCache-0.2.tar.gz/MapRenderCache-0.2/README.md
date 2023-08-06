# MapRenderCache

## features

- [X] rendering
- [X] caching
- [X] python bindings

## install

`pip3 install MapRenderCache`

## usage

```python
from MapRenderCache import MapRenderCache

stylesheet = "mapnik.xml"
caching_directory = "/tmp/cache"
tile_width = 512
tile_height = 512
cache = MapRenderCache(stylesheet, caching_directory, tile_width, tile_height)

# This will create a directory 'cache' in the current working directory
# cache = MapRenderCache(stylesheet, tile_width, tile_height) 
```