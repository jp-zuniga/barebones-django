{
  description = "dev shells!";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11";

  outputs = {
    self,
    nixpkgs,
  }: let
    systems = ["x86_64-linux"];
    forAllSystems = nixpkgs.lib.genAttrs systems;
    nixpkgsFor = forAllSystems (system: nixpkgs.legacyPackages.${system});
  in {
    devShells = forAllSystems (system: let
      pkgs = nixpkgsFor.${system};
    in {
      default = pkgs.mkShell {
        buildInputs = [
          pkgs.bash
          pkgs.jq
          pkgs.just
          pkgs.mermaid-cli
          pkgs.postgresql_18
          pkgs.railway
          pkgs.ruff
          pkgs.ty
          pkgs.uv
        ];
      };

      dev = pkgs.mkShell {
        buildInputs = [
          pkgs.bash
          pkgs.jq
          pkgs.just
          pkgs.railway
          pkgs.ruff
          pkgs.ty
          pkgs.uv
        ];
      };

      lint = pkgs.mkShell {
        buildInputs = [
          pkgs.bash
          pkgs.just
          pkgs.ruff
        ];
      };

      render = pkgs.mkShell {
        buildInputs = [
          pkgs.bash
          pkgs.just
          pkgs.mermaid-cli
        ];
      };

      test = pkgs.mkShell {
        buildInputs = [
          pkgs.bash
          pkgs.just
          pkgs.postgresql_18
          pkgs.uv
        ];
      };

      update = pkgs.mkShell {
        buildInputs = [
          pkgs.bash
          pkgs.uv
        ];
      };
    });
  };
}
