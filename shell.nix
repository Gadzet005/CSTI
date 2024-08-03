let
	pkgs = import <nixpkgs> {};
in pkgs.mkShell {
	packages = [
		(pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
			requests
			beautifulsoup4
<<<<<<< HEAD
			click
=======
			requests-cache
>>>>>>> origin/master
		]))
		pkgs.clang-tools
	];
}
