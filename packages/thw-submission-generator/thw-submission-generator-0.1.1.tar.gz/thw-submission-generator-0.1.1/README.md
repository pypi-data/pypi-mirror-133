Start with a config file:

```yaml
---
map_name: "Dota alstars"
author: "feirfox"
repo_uri: null
contributing: null
introduction: |+
  Dota is very fun game, league of legends stole from dota bascically
screenshots:
  - caption: Invoker
    uri: https://i.imgur.com/smX662W.jpeg
  - caption: Pikachu
    uri: https://i.imgur.com/Czgalle.jpeg
icon_table:
  title: "Heroes"
  contents:
    - caption: "Drow, likes to shot pewpew"
      uri: https://i.imgur.com/XxEwZWP.png
changelog:
  - version: 0.1.0
    date: 16 Jul 1969
    changes:
      - Landed on the moon
credits:
  - peq
  - Frotty
  - hiveworkshop
```

And generate a hive post:

```shell
./generate_submission_template.sh config.yaml
```

Produces:

![Example post](screenshot.png)
