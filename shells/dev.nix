pkgs:
pkgs.mkShell {
  buildInputs = [
    pkgs.bash
    pkgs.jq
    pkgs.just
    pkgs.railway
    pkgs.ruff
    pkgs.ty
    pkgs.uv
  ];
}
