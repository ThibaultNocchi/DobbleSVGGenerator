# Dobble SVG Generator
The goal of this Python script is to generate a [Dobble](http://eng.foxmind.co.il/game-103) card game only from a handful of given symbols.

"Each card in Dobble features eight different symbols, with the symbols varying in size from one card to the next. Any two cards have exactly one symbol in common. For the basic Spot it! game, reveal one card, then another. Whoever spots the symbol in common on both cards claims the first card, then another card is revealed for players to search, and so on. Whoever has collected the most cards when the 55-card deck runs out wins!" - [Rules of Play](https://rulesofplay.co.uk/products/dobble)

## How does it work?
In a folder, download the Python script and put your different symbols in a subfolder named "img" as PNG images. Thoses images must be named 1.png, 2.png, etc.  
After running the script (which may take a minute), a "svg" folder is created with each card. You can then edit them to further improve the generation, and print them.

## Requirements
* Python 3
* [svgwrite library](https://pypi.org/project/svgwrite/)
* Symbols as PNG files.

## Copyright and license
* [svgwrite](https://github.com/mozman/svgwrite) - [MIT License](https://github.com/mozman/svgwrite/blob/master/LICENSE.TXT)
* [Code snippet from StackOverflow](https://stackoverflow.com/a/20380514) by [Fred the Fantastic](https://stackoverflow.com/users/2372270/fred-the-fantastic) - [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/legalcode)
* [Code snippet from Wikipedia](https://fr.wikipedia.org/wiki/Dobble#Algorithme_de_g%C3%A9n%C3%A9ration) - [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/legalcode)