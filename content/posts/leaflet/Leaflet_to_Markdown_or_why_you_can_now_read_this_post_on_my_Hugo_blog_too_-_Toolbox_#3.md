---
title: "Leaflet to Markdown or why you can now read this post on my Hugo blog too - Toolbox #3"
date: 2026-01-07T21:11:39.039Z
original_url: "https://toolbox.leaflet.pub/3mbueyjaxc22b"
author: "mariuskimmina.com"
---

*Originally published at [Marius Toolbox](https://toolbox.leaflet.pub/3mbueyjaxc22b)*

A few days ago I announced on BlueSky that I created a small tool to convert my leaflet posts (like the one you are reading right now) to markdown, so that they can also show up on my [hugo](https://gohugo.io/) based blog.

{{< bsky did="did:plc:tbzfsowmg4zj234pws47u3x6" postid="3mbrxzvw36c22" >}}


I promised to follow up with an article about how I use it and that's what you are reading now. 

In the root directory of your hugo blog you'll need to create a file `.leaflet-sync.yaml` - here is what mine looks like.


```yaml
source:
  handle: "mariuskimmina.com"
  collection: "pub.leaflet.document"
  publication_name: "Marius Toolbox"

output:
  posts_dir: "content/posts/leaflet"
  images_dir: "static/images/leaflet"
  image_path_prefix: "/images/leaflet"

template:
  frontmatter: |
    ---
    title: "{{ .Title }}"
    date: {{ .CreatedAt }}
    original_url: "https://toolbox.leaflet.pub/{{ .Slug }}"
    author: "{{ .Handle }}"
    ---
  content: |
    *Originally published at [Marius Toolbox](https://toolbox.leaflet.pub/{{ .Slug }})*

    {{ .Content }}

    ---
    *Originally published at [Marius Toolbox](https://toolbox.leaflet.pub/{{ .Slug }})*
```

In this same directory you now need to run `leaflet-hugo-sync` - my recommendation for now would be to just use 


```yaml
nix run github:mariuskimmina/leaflet-hugo-sync
```

But I might also look into producing an official release soon.

This will create a folder `content/posts/leaflet` containing all your leaflet posts with sanitized version of the post name as the file name.

If you leave out the `publication_name` it will get all your leaflets which may or may not what you want.

You can then use the `template` section to customize the content a bit, I for example added links back to the leaflet at the top and bottom of the posts. 

If you actually use this I would love to hear feedback <3
I will also soon publish another post to detail the entire setup of how I now host my hugo blog on [mariuskimmina.com](https://mariuskimmina.com) and keep it sync with my leaflet posts. 

Source:

[https://tangled.org/mariuskimmina.com/leaflet-hugo-sync](https://tangled.org/mariuskimmina.com/leaflet-hugo-sync)

[https://github.com/mariuskimmina/leaflet-hugo-sync](https://github.com/mariuskimmina/leaflet-hugo-sync)

You can find my blog, including this posts, on 
[https://mariuskimmina.com/posts/](https://mariuskimmina.com/posts/)





---
*Originally published at [Marius Toolbox](https://toolbox.leaflet.pub/3mbueyjaxc22b)*
