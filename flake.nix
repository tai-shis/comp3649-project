{
  description = "comp3649 nix development shell dependencies";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.systems.url = "github:nix-systems/default";
  inputs.nixpkgs-python.url = "github:cachix/nixpkgs-python";
  inputs.flake-utils = {
    url = "github:numtide/flake-utils";
    inputs.systems.follows = "systems";
  };

  outputs =
    { nixpkgs, nixpkgs-python, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
        # pythonVersion = "3.13";
        # python = nixpkgs-python.packages.${system}.${pythonVersion};
        # pythonWithPackages = python.withPackages (ps: with ps; [
        #   pip
        # ]);
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            (pkgs.python3.withPackages (python-pkgs: [

            ]))
            pkgs.python3Packages.venvShellHook
          ];

          venvDir = "./.venv";

          #  set up auto package adding
          postShellHook = ''
            echo "To enter python virtual environment, run source .venv/bin/activate"
            echo "To install dependencies, run pip install -r requirements.txt"
          '';
        };
      }
    );
}
