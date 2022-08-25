# TriConvert
Software to convert 3D file types

## Usage

Run the following command: `python ./convert.py`. It will output the following:
```
python convert.py [FLAGS]

REQUIRED FLAGS:
    -i  Input file
    -o  Output file
```

## Currently supported formats
### formats
There are no formats that are currently truely supported. I hope this will change in the future.

### conversions
Nope.

## Partially supported formats
### formats
- `.obj` - WaveFront OBJ. Tags supported:
  - `g` - saved in other formats as an empty body
  - `v` - vertex
  - `vt` - vertex texture coordinate
  - `vn` - vertex normal
  - `f` - face (triangular only)
- `.3mf` - 3D Manufacturing Format. Data supported in 3dmodel.model:
  - `vertex` - a vertex
  - `trianlge` - a triangle

### Almost perfect conversions
- `obj` -> `3mf`
  - Details lost:
    - none
  - Details gained:
    - units (kinda)
- `3mf` -> `obj`
  - Details lost:
    - units
  - Detail gained:
    - none

## Formats to support next:
- `.stl` is next.
- `.dae` (COLLADA) is likely after that.

If you have any formats you would like to add or have me try to add, create an issue.

## Things that need to be done:
- clean up all of the code files

## help needed!
- I am at the end of my knowledge for converting `.obj`'s and `.3mf`s. Help would be appreciated!
