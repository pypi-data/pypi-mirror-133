# svgsprite

This is a simple script (no external dependencies) to regroup all the SVG files
from a directory into a single sprite.

## Installation

``` sh
pip install svgsprite
```

## Usage

``` sh
svgsprite --src path/to/dir/with/svg/files --dest path/to/sprite/to/create
```

You can then refer to your icons with tags like this:

```html
<svg>
  <use xlink:href="sprite.svg#my-svg-file"></use>
</svg>
```
