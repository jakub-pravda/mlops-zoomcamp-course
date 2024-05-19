{pkgs, ...}: {
  kernel.python.minimal = {
    enable = true;
  };
  kernel.python.mlops = { 
    enable = true; 
    displayName = "MLOps zoomcamp kernel";
    extraPackages = ps: [ 
      ps.fastparquet
      ps.numpy
      ps.pandas
      ps.seaborn
      ps.scikit-learn
      ps.scipy
    ]; 
  };
}
