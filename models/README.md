# Deploy the model

We created this pickle model in section #1, now we would like to deploy these model as web service

## Before model deploying

* Use exactly same version of scikit-learn, which was used to train the model (there should ne some errors during unpickle in case of using different version of scikit-learn)
  * To check installed version use `pip freeze | grep scikit-learn`