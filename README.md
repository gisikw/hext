# Hext
A text-to-hexmap tool inspired by [TextMapper](https://campaignwiki.org/text-mapper), but using Python rather than Perl.

Hext takes a text description of a map and generates a visualization of it.

```txt
0101 forest "Foxtear Woods"
0102 desert
0103 water
0201 water "Mirror Lake"
0202 desert
0301 water
0401 water
0402 desert
0501 water
0302 water
0303 desert
0101-0202-0301-0402 red
0302-0403-0502-0501-0401 blue
0403 desert
0502 desert
```

<p align="center">
<img src="https://github.com/gisikw/hext/blob/main/examples/map.png" alt="Example Map" />
</p>

# Special Thanks
- [Red Blob Games on Hexagonal Grids](https://www.redblobgames.com/grids/hexagons/)
