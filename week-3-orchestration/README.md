# Orchestration

The orchestration part mainly involves orchestrating data pipelines in the [Mage data platform](https://www.mage.ai/). For Mage deployment, I'm using a Dockerfile instead of Nix flakes, as I did in previous homework assignments. The simple reason is that the Mage platform is not currently in nixpkgs, and honestly, I'm a bit too lazy to unify the deployment right now.