{
  description = "dev shells!";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11";

  outputs = {
    self,
    nixpkgs,
  }: let
    systems = [
      "x86_64-darwin"
      "x86_64-linux"
      "aarch64-darwin"
      "aarch64-linux"
    ];

    forAllSystems = nixpkgs.lib.genAttrs systems;
    formatter = forAllSystems (system: nixpkgsFor.${system}.alejandra);
    nixpkgsFor = forAllSystems (system: nixpkgs.legacyPackages.${system});
  in {
    devShells = forAllSystems (system: let
      pkgs = nixpkgsFor.${system};
    in {
      default = import shells/all.nix pkgs;
      dev = import shells/dev.nix pkgs;
      lint = import shells/lint.nix pkgs;
      render = import shells/render.nix pkgs;
      test = import shells/test.nix pkgs;
      update = import shells/update.nix pkgs;
    });
  };
}
