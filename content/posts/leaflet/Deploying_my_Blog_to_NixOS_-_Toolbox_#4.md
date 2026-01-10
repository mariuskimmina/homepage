---
title: "Deploying my Blog to NixOS - Toolbox #4"
date: 2026-01-09T16:29:06.245Z
original_url: "https://toolbox.leaflet.pub/3mbyw54q7gc22"
author: "mariuskimmina.com"
---

*Originally published at [Marius Toolbox](https://toolbox.leaflet.pub/3mbyw54q7gc22)*

Now I know most people think that a blog should be easy, you write something, you press publish and then it shows up online and I like that too - that's why I am writing this on [leaflet.pub](https://leaflet.pub) where it works exactly like this. But I also have my other page at [mariuskimmina.com](https://mariuskimmina.com) which is running on NixOS because.... reasons!
And I want my posts that I write here on leaflet also to show up on my blog which is why I created [leaflet-hugo-sync](https://github.com/mariuskimmina/leaflet-hugo-sync), a tool that fetches all your leaflet posts and converts them to markdown.

Today I want to introduce you to the slightly overengineered way of how my leaflets end up on my page. This will involve no more then 3 repositories, easy peasy:

- leaflet-hugo-sync - the tool that converts leaflets to markdown
- homepage - my page created with hugo
- nix-hetzner-lab - the nix configuration of my server setup with nixos-anywhere

I am still new to the nix world and if you have any ideas for improvements to this whole process then please let me know, my DMs are open on BlueSky.

After I press publish on a Leaflet I go to my [homepage repo](https://github.com/mariuskimmina/homepage) on Github and I trigger a pipeline, this pipeline will run `leaflet-hugo-sync` and directly update the main branch of the repo. Once it finishes all my leaflets can be found as up to date markdown files in the repo.

The following is the github actions code that runs on my `homepage` repo:


```yaml
name: Sync Leaflets

on:
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      - uses: DeterminateSystems/nix-installer-action@main
      - uses: DeterminateSystems/magic-nix-cache-action@main

      - name: Run leaflet-hugo-sync
        run: nix run github:mariuskimmina/leaflet-hugo-sync

      - name: Commit and push changes
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add content/ static/
          if git diff --staged --quiet; then
            echo "No changes to commit"
          else
            git commit -m "sync: update leaflet posts"
            git push
          fi

      - name: Trigger nix-hetzner-lab deploy
        if: success()
        env:
          GH_TOKEN: ${{ secrets.NIX_LAB_PAT }}
        run: gh workflow run deploy.yml --repo mariuskimmina/nix-hetzner-lab
```

This is the only thing I need to trigger manually after publishing a leaflet. This steps takes ~1 Minute to complete.

![](/images/leaflet/bafkreiay73bogacnzg32xdtrmb32zfbgfc7casbvuqu7f6sx77xpe3sqg4.png)

Once the main branch is updated it will trigger another github action that runs in my `nix-hetzner-lab` repository, which will essentially do a `nixos-rebuild` causing the updated version of the blog to be deployed.


```yaml
name: Deploy

on:
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      - uses: DeterminateSystems/nix-installer-action@main
      - uses: DeterminateSystems/magic-nix-cache-action@main

      - name: Update flake
        run: |
          nix flake update homepage
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add flake.lock
          if git diff --staged --quiet; then
            echo "No changes to flake.lock"
          else
            git commit -m "flake: update homepage"
            git push
          fi

      - name: Deploy
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.DEPLOY_SSH_KEY }}" > ~/.ssh/id_ed25519
          chmod 600 ~/.ssh/id_ed25519
          ssh-keyscan ${{ secrets.SERVER_IP }} >> ~/.ssh/known_hosts
          nix run nixpkgs#nixos-rebuild -- switch \
            --flake .#hetzner-lab \
            --target-host root@${{ secrets.SERVER_IP }}
```

Now this deploy jobs takes around ~12 minutes. If anyone sees a way to make this faster please let me know.

![](/images/leaflet/bafkreick5jylm7c56amlqkwd7jp4xzenaq6ualykl3etke6zm76pmzwzzm.png)

But that's it, now the new updated version of the blog is running and my leaflet can be read on my hugo based homepage as well.



Find all my repos here:

[https://github.com/mariuskimmina/homepage](https://github.com/mariuskimmina/homepage)

[https://github.com/mariuskimmina/nix-hetzner-lab](https://github.com/mariuskimmina/nix-hetzner-lab)

[https://github.com/mariuskimmina/leaflet-hugo-sync](https://github.com/mariuskimmina/leaflet-hugo-sync)



You can also find them on tangled

[https://tangled.org/mariuskimmina.com/homepage](https://tangled.org/mariuskimmina.com/homepage)

[https://tangled.org/mariuskimmina.com/nix-hetzner-lab](https://tangled.org/mariuskimmina.com/nix-hetzner-lab)

[https://tangled.org/mariuskimmina.com/leaflet-hugo-sync](https://tangled.org/mariuskimmina.com/leaflet-hugo-sync)



I currently use github as the primary development hub because of github actions being available and free but I also plan to host a CI runner for tangled on my lab soon and then things might change.

Hope you enjoyed this read and feel free to reach out to me with any feedback <3.



---
*Originally published at [Marius Toolbox](https://toolbox.leaflet.pub/3mbyw54q7gc22)*
