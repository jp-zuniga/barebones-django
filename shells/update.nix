pkgs:
pkgs.mkShell {
  buildInputs = [
    pkgs.bash
    pkgs.uv
  ];
}
