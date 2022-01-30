<p align="center">
  <img src="logo.svg" height="100px"/>
</p>

This repository houses a number of Pokémon sprite collections, each of which is indexed by a **sprite index** JSON file. The [sprite-indices.json](sprite-indices.json) is a list of all the sprite indices in the repo. Internally, pkuManager combines them all into a single **master sprite index** which is then referenced for displaying sprites.

## Structure
Each sprite index contains a list of species. Each species (e.g. Pikachu) contains a list of `"Forms"` (e.g. Cosplay), and each form potentially contains a list of `"Appearances"` (e.g. Libre outfit). Note that all species have a default form, whether named or not. For example, Giratina's default form is `"Altered"`, while Pikachu's is simply the empty string `""`.

Each form entry and appearance entry has a `"Sprites"` tag. This tag contains a `"Default"`, `"Egg"`, and `"Shadow"` **sprite block**. Each sprite block contains a `"Regular"` and `"Shiny"` tag, each of which contains a `"Box"`, `"Front"`, and `"Back"` sprite. Each of those three **sprite types** includes a direct `"URL"` to the sprite, and an `"Author"` tag which credits its creator.

Here's an example sprite index:

```jsonc
{
  "Example_Species_1": {
    "Forms": {
      "Example_Form_A": {
        "Sprites": {
          "Default": {
            "Regular": {
              "Box": {
                "URL": "https://url.to/regular/box.png",
                "Author": "https://platform.com/Author1"
              },
              "Front": //..same as "Box"
              "Back": //..same as "Box"
            },
            "Shiny": //...Same as "Regular"
          },
          "Egg": //...Same as "Default"
          "Shadow": //...Same as "Default"
        },
        "Appearance": {
          "Example_Appearance_A": {
            "Sprites": //...Same as "Sprites"
          },
          "Example_Appearance_B": //...Same as "Example_Appearance_A"
        }
      },
      "Example_Form_B": //...Same as "Example_Form_A"
    }
  },
  "Example_Species_2": //...Same as "Example_Species_1"
}
```

## Gender Differences
Some Pokémon species exhibit gender dimorphism or, in Pokémon lingo, gender differences. As such, pkuSprite supports having different urls and authors depending on the gender of the Pokémon. This is done by replacing the value in question with an array of two values, the first being the male value and the second being the female one. For example:
```jsonc
...
"Box": {
  "URL": ["https://url.to/maleSpriteF.png", "https://url.to/femaleSpriteF.png"],
  "Author": "https://platform.com/AuthorOfBoth"
},
"Front": {
  "URL": ["https://url.to/maleSprite.png", "https://url.to/femaleSprite.png"],
  "Author": ["https://platform.com/AuthorOfMale", "https://platform.com/AuthorOfFemale"]
}
...
```

## Author Tag
Each sprite should have a corresponding `"Author"` tag. For official sprites, the tag simply lists `"Game Freak"`, while unofficial sprites include a link to the author's profile on some social platform (e.g. Twitter, DeviantArt, Github, etc.).

### What Constitutes Authorship?
When a sprite is made from scratch by a single person or team then there's usually no confusion. But what if a sprite is a derivative work? Should the both the original author and the new one be credited? What if it is a derivative work of a derivative work, and so on?

The pkuSprite repository has the convention that the *last* author of a sprite be credited. For example, a Shadow Lugia sprite that is an edit of an official Lugia sprite would be credited to the editor and not Game Freak. The idea is that, since each sprite includes a link to its author, information about its creation can be found on their profile or, failing that, by contacting them directly. That said, most sprites on pkuSprite are either official, edits of official work, or original.

### Sprite Takedown
If you are the author of a sprite on any of the sprite indices and wish to have it removed, please email [Prof. 64](mailto:prof64.pku@gmail.com?subject=[pkuSprite]%20Takedown%20Request) to have it taken down.