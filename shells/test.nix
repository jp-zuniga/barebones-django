pkgs:
pkgs.mkShell {
  buildInputs = [
    pkgs.bash
    pkgs.just
    pkgs.postgresql_18
    pkgs.uv
  ];
}
