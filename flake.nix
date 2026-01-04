 {
  description = "Hugo blog with PaperMod theme";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        
        # Fetch PaperMod theme
        papermod-theme = pkgs.fetchFromGitHub {
          owner = "adityatelange";
          repo = "hugo-PaperMod";
          rev = "master";
          sha256 = "sha256-+OyrkV+9TELJOoz1qL63Ad95jobRQfv6RpoHKhemDfM=";
        };
        
        # Hugo site build
        site = pkgs.stdenv.mkDerivation {
          name = "hugo-blog";
          src = ./.;
          buildInputs = [ pkgs.hugo ];
          
          buildPhase = ''
            # Copy theme to themes directory
            mkdir -p themes
            cp -r ${papermod-theme} themes/PaperMod
            chmod -R u+w themes/PaperMod
            
            # Build the site
            hugo --destination $out --minify
          '';
          
          installPhase = "true"; # output already in $out
        };
        
      in {
        packages = {
          default = site;
          blog = site;
        };

        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            hugo
            git
          ];
          
          shellHook = ''
            # Set up theme symlink for development
            if [ ! -d "themes/PaperMod" ]; then
              mkdir -p themes
              ln -sf ${papermod-theme} themes/PaperMod
            fi
            
            echo "Hugo PaperMod development environment"
            echo "Theme: PaperMod"
            echo "Run 'hugo server' to start development server"
          '';
        };
      });
}
