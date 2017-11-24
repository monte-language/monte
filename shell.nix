{ nixpkgs ? import <nixpkgs> {} }:
let
  inherit (nixpkgs) pkgs;
in pkgs.stdenv.mkDerivation {
  name = "typhon-env";
  buildInputs = with pkgs; [
    graphviz tahoelafs git
    pythonPackages.sphinx
  ];
}
