<p align="center">
  <img src="logo.svg" height="100px"/>
</p>

This repository is specifically for housing and providing structured access to Pokémon and Pokémon related sprites and graphics in the form of URLs. These URLs are compiled into *Dexes*, which are just json files with a predefined structure, located in the repo's [build branch](https://github.com/project-pku/pkuSprite/tree/build). These dexes are primarily for use in [pkuManager](https://github.com/project-pku/pkuManager), but any application is free to use them.

## Auto-Building
Like it's sister repo [pkuData](https://github.com/project-pku/pkuData), whenever a change is pushed to this repo that affects any of the dexes specified in the [`config.json`](config.json) file (e.g. a sprite is added, updated, removed), all the dexes are rebuilt and the new build is committed to the build branch.

## Structure of SpeciesDex
Each **SpeciesDex** is a type of dex for storing info about Pokémon species. In the case of this repo, that info is just URLs to sprites of this species. Each top level entry in a SpeciesDex is a species (e.g. Pikachu) which contains an entry for `"Forms"` (e.g. Cosplay), and each form potentially contains an entry for `"Appearances"` (e.g. Libre outfit). Note that all species have a default form, whether named or not. For example, Giratina's default form is `"Altered"`, while Pikachu's is simply the empty string `""`.

Each form entry and appearance entry has a `"Sprites"` tag. This tag contains a `"Default"`, `"Egg"`, and `"Shadow"` **sprite block**. Each sprite block contains a `"Regular"` and `"Shiny"` tag, each of which contains a `"Box"`, `"Front"`, and `"Back"` sprite. Each of those three **sprite types** includes a direct `"URL"` to the sprite, and an `"Author"` tag which credits its creator.

Here's an example dex:

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
Some Pokémon species exhibit sexual dimorphism or, in Pokémon lingo, **gender differences**. As such, pkuSprite supports having different URLs and authors depending on the gender of the Pokémon. The syntax for this is given below:
```jsonc
"Box": {
  "URL": ["$Male-Female", "https://url.to/maleSpriteF.png", "https://url.to/femaleSpriteF.png"],
  "Author": "https://platform.com/AuthorOfBoth"
},
"Front": {
  "URL": ["$Male-Female", "https://url.to/maleSprite.png", "https://url.to/femaleSprite.png"],
  "Author": ["$Male-Female", "https://platform.com/AuthorOfMale", "https://platform.com/AuthorOfFemale"]
}
```

## Author Tag
Each sprite should have a corresponding `"Author"` tag. For official sprites, the tag simply lists `"Game Freak"`, while unofficial sprites include a link to the author's profile on some social platform (e.g. Twitter, DeviantArt, Github, etc.).

### What Constitutes Authorship?
When a sprite is made from scratch by a single person or team then there's usually no confusion. But what if a sprite is a derivative work? Should the both the original author and the new one be credited? What if it is a derivative work of a derivative work, and so on?

The pkuSprite repository has the convention that the *last* author of a sprite be credited. For example, a Shadow Lugia sprite that is an edit of an official Lugia sprite would be credited to the editor and not Game Freak. The idea is that, since each sprite includes a link to its author, information about its creation can be found on their profile or, failing that, by contacting them directly. That said, most sprites on pkuSprite are either official, edits of official work, or original.

### Sprite Takedown
If you are the author of a sprite on any of the sprite indices and wish to have it removed, please email [Prof. 64](mailto:prof64.pku@gmail.com?subject=[pkuSprite]%20Takedown%20Request) to have it taken down.