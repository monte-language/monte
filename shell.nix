{ nixpkgs ? import <nixpkgs> {} }:
let
  inherit (nixpkgs) pkgs;
in pkgs.stdenv.mkDerivation {
  name = "monte-env";
  buildInputs = with pkgs; [
    graphviz git
    pythonPackages.sphinx
  ];
}
