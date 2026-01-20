pkgs:
pkgs.mkShell {
  buildInputs = [
    pkgs.bash
    pkgs.just
    pkgs.ruff
  ];
}
