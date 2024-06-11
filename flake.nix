{
  description = "MLOps Zoompcamp - project environment";

  inputs.flake-compat.url = "github:edolstra/flake-compat";
  inputs.flake-compat.flake = false;
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

  outputs = {
    self,
    flake-compat,
    flake-utils,
    nixpkgs,
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
      in {
        devShells.default = pkgs.mkShell {
          venvDir = "venv";
          packages = with pkgs; [ python311 awscli2 ] ++
            (with pkgs.python311Packages; [ 
              pip
              pipenv
              setuptools
              venvShellHook

              # data science
              pyarrow
              hyperopt
              jupyter
              numpy
              pandas
              seaborn
              scikit-learn
              scipy
              xgboost

              # mlops
	            boto3
              flask
              gunicorn
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
