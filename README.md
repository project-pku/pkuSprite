<p align="center">
  <img src="logo.svg" height="100px"/>
</p>

This repository is specifically for housing and providing structured access to Pokémon related sprites and graphics in the form of URLs. These URLs grouped into *dexes*, which are just json files with a predefined structure. These dexes, when compiled, are primarily for use in [pkuManager](https://github.com/project-pku/pkuManager), but any application is free to use them.

## Auto-Building
Like it's sister repo [pkuData](https://github.com/project-pku/pkuData), whenever a change is pushed to this repo that affects any of the dexes specified in the [`config.json`](config.json) file (e.g. a sprite is added, updated, removed), all the dexes are rebuilt and the new build is committed to the [build branch](https://github.com/project-pku/pkuSprite/tree/build).

## Structure of SpeciesDex
While the structure of other dexes is self-explanatory, SpeciesDexes are a little more complex. A **SpeciesDex** is a type of dex for storing info about Pokémon species. In the case of this repo, that info is just URLs to sprites of this species. Each top level entry in a SpeciesDex is a species (e.g. Pikachu) which contains an entry for `"Forms"` (e.g. Cosplay), and each form potentially contains an entry for `"Appearances"` (e.g. Libre outfit). Note that all species have a default form, whether named or not. For example, Giratina's default form is `"Altered"`, while Pikachu's is simply the empty string `""`.

In this repo, each form entry and appearance entry may have a `"Sprites"` tag. Every entry in this tag corresponds to a different **sprite type** (e.g. box, front, back, etc.). The value for each of these sprite types should be an array of length 2, with the first entry being a direct URL to the sprite, and the second being a URL to one of the Author's accounts on some social platform (e.g. deviantart, github, twitter, etc.). Note that for official sprites, we simply list `"Game Freak"`.

Here's an example of a basic dex:

```jsonc
{
  "Pikachu": {
    "Forms": {
      "Cosplay": {
        "Sprites": {
          "Box": ["https://url.to/box/sprite.png", "https://platform.com/author"],
          "Front": [ ... ], //..same as "Box"
          "Back": [ ... ] //..same as "Box"
        },
        "Appearance": {
          "Libre Outfit": {
            "Sprites": { ... } //...Same as "Sprites"
          },
          "Rock-Star Outfit": { ... } //...Same as "Libre Outfit"
        }
      },
      "Partner": { ... } //...Same as "Cosplay"
    }
  },
  "Raichu": { ... }, //...Same as "Pikachu"
}
```

## Modifiers
After reading about the structure described above, you may be wondering "How do I add sprites for Female, Shiny, or Shadow variants?" SpeciesDexes have a unified way of dealing with this: **modified values.** Consider the following front sprite entry:

```jsonc
"Front$": {
  "Shiny": ["https://url.to/spriteS.gif", "https://platform.com/author"],
  "": ["https://url.to/spriteR.gif", "https://platform.com/author"],
}
```

Notice how a `"$"` has been appended to it. This denotes that a value is *modified*. This just means that when searching for a particular value (in this case `"Front"`), the SFAM should be used to decide which value to take until an unmodified value (i.e. one without a `"$"` is found). Note that this means we can nest modifiers:

```jsonc
"Front$": {
  "Egg$": {
    "Shiny": ["https://url.to/shiny/egg.png", "https://platform.com/authorShinyEgg"],
    "": ["https://url.to/regular/egg.png", "https://platform.com/authorRegEgg"],
  },
  "Shadow$": {
    "Shiny": [ ... ],
    "": [ ... ],
  },
  "$": {
    "Shiny": [ ... ],
    "": [ ... ],
  }
}
```

Also note that the order the options appear and the order of the nesting determines what value is returned. In the example above, first `"Egg"` is checked, if it fails `"Shadow"` is checked, and finally `""` is chosen (the default value `""` is always chosen). Then in each of the cases, `"Shiny"` is checked. Note that if the search process turns up no match (which can only occur if there is no default value), then the search will come up negative.

Below is a list of modifiers:

- `"Shiny"` for shiny sprites.
- `"Egg"` for egg sprites.
- `"Shadow"` for shadow sprites.
- `"Female"` for female sprites (note that this only applies to species with gender differences, with the default `""` being used for male sprites).

## What Constitutes Authorship?
When a sprite is made from scratch by a single person or team then there's usually no confusion. But what if a sprite is a derivative work? Should the both the original author and the new one be credited? What if it is a derivative work of a derivative work, and so on?

The pkuSprite repository has the convention that the *last* author of a sprite be credited. For example, a Shadow Lugia sprite that is an edit of an official Lugia sprite would be credited to the editor and not Game Freak. The idea is that, since each sprite includes a link to its author, information about its creation can be found on their profile or, failing that, by contacting them directly. That said, most sprites on pkuSprite are either official, edits of official work, or original.

### Sprite Takedown
If you are the author of a sprite on any of the sprite indices and wish to have it removed, please email [Prof. 64](mailto:prof64.pku@gmail.com?subject=[pkuSprite]%20Takedown%20Request) to have it taken down.