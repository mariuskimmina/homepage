---
title: "Making sense of NixOS with nixos-anywhere - toolbox #2"
date: 2026-01-02T17:22:48.455Z
original_url: "https://toolbox.leaflet.pub/3mbhfupgzu22l"
author: "mariuskimmina.com"
---

*Originally published at [Marius Toolbox](https://toolbox.leaflet.pub/3mbhfupgzu22l)*

Now, this might just be me, but I was trying to love nix & nixos for a while already but whenever I tired to use for my personal projects or as a operating system for my personal computer but then I always felt like it got in the way at times.

On a personal computer I might spontaneously have to install proprietary software, like zoom, to get my work done and NixOS makes that a pain. I always went back to arch after a while but the thought of it's declarative beauty was still lingering in my mind.

I recently heard more and more people using NixOS for their servers and production workloads and, thinking about it, that makes perfect sense. I will never ever need to install zoom or the like on a server. But I do care a lot about being in control of exactly what is installed on it, especially when running production workloads. Being able to define everything in a declarative configuration and check it into version control.

The problem with that at first seemed to be that most cloud providers simply don't offer NixOS (yet) but that also appears to be a very solvable problem since there is [nixos-anywhere](https://github.com/nix-community/nixos-anywhere). This tool turns any cloud VM into a NixOS machine using `kexec`. I tried it today and I am blown away by how well it works.

I have followed the setup of [nixos-anywhere-examples](https://github.com/nix-community/nixos-anywhere-examples) and turned a Hetzner Ubuntu machine into NixOS in just a few minutes and a single command


```shellscript
nix run nixpkgs#nixos-anywhere -- --flake .generic --generate-hardware-config nixos-generate-config ./hardware-configuration.nix root@<your-ip>
```

And now all configuration files for this machine are on my local computer, I can edit them and check them into version control. And when I want to apply a change it's again just one command


```shellscript
nix run nixpkgs#nixos-rebuild -- switch --flake .#generic --target-host root@<your-ip>
```



You can find the config here: 
[https://tangled.org/mariuskimmina.com/nix-hetzner-lab](https://tangled.org/mariuskimmina.com/nix-hetzner-lab)

For now it's just a minimal edit of the example repo but I have some plans for a project I want to host this way and to see how nix as IaC tool will hold up.



... maybe someday I will also get back to it for my personal computer once again ...



---
*Originally published at [Marius Toolbox](https://toolbox.leaflet.pub/3mbhfupgzu22l)*
