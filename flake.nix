{
  description = "Your jupyenv project";

  nixConfig.extra-substituters = [
    "https://tweag-jupyter.cachix.org"
  ];
  nixConfig.extra-trusted-public-keys = [
    "tweag-jupyter.cachix.org-1:UtNH4Zs6hVUFpFBTLaA4ejYavPo5EFFqgd7G7FxGW9g="
  ];

  inputs.flake-compat.url = "github:edolstra/flake-compat";
  inputs.flake-compat.flake = false;
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  inputs.jupyenv.url = "github:tweag/jupyenv";

  outputs = {
    self,
    flake-compat,
    flake-utils,
    nixpkgs,
    jupyenv,
    ...
  } @ inputs:
    flake-utils.lib.eachSystem
    [
      flake-utils.lib.system.x86_64-linux
    ]
    (
      system: let
        pkgs = import nixpkgs {
          inherit system;
        };
        inherit (jupyenv.lib.${system}) mkJupyterlabNew;
        jupyterlab = mkJupyterlabNew ({...}: {
          nixpkgs = inputs.nixpkgs;
          imports = [(import ./kernels.nix)];
        });
      in rec {
        packages = {inherit jupyterlab;};
        packages.default = jupyterlab;
        apps.default.program = "${jupyterlab}/bin/jupyter-lab";
        apps.default.type = "app";

        devShells.default = pkgs.mkShell {
          venvDir = "venv";
          packages = with pkgs; [ python311 ] ++
            (with pkgs.python311Packages; [ 
              pip
              setuptools
              venvShellHook

              # data science
              fastparquet
              hyperopt
              jupyter
              numpy
              pandas
              seaborn
              scikit-learn
              scipy
              xgboost

              # mlops
              mlflow
            ]);
          shellHook = ''            
            if ! pgrep -f "jupyter-lab" > /dev/null
            then
              echo "Starting Jupyter"
              nohup jupyter-lab &
            fi
            PID_JUPYTER=$(pgrep -f "jupyter-lab" | head -n 1)
            
            if ! pgrep -f "mlflow" > /dev/null
            then
              echo "Starting MLflow"
              nohup mlflow server &
            fi
            PID_MLFLOW=$(pgrep -f "mlflow" | head -n 1)

            echo "Jupyter is running PID: $PID_JUPYTER"
            echo "MLflow is running PID: $PID_MLFLOW"

            function kill_all() {
              echo "Killing $1,,,"
              for i in $(pgrep -f "$1"); do kill "$i"; done
              echo "$1 killed"
            }

            function cleanup() {
              echo "Exiting..."
              kill_all "mlflow"
              kill_all "jupyter-lab"
            }
            trap cleanup EXIT
          ''; 
        };
      }
    );
}
