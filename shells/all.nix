pkgs:
pkgs.mkShell {
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
}
