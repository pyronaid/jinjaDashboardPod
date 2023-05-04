### build the repository

### check the presence of mongo-secret and mongo-config
if [[ $(kubectl get configMap | grep -E "^mongo-config[ ]+" | wc -l) != 1 ]]; then
  echo "The mongo-config configMap is missing from k8. Launch it before"
  exit 1
fi
if [[ $(kubectl get secret | grep -E "^mongo-secret[ ]+" | wc -l) != 1 ]]; then
  echo "The mongo-secret secret is missing from k8. Launch it before"
  exit 1
fi

### build the docker images on minikube
versionApp=$(cat version.txt)
docker build -t pyronaid/jinja_dashboard_app:${versionApp} .
cat password.txt | docker login --username pyronaid --password-stdin
docker push pyronaid/jinja_dashboard_app:${versionApp}
docker rmi pyronaid/jinja_dashboard_app:${versionApp}

cat gunicorn-cfg.py

#refresh installation
echo "command delete -f jinja-config.yaml"
kubectl delete -f jinja-config.yaml
echo "###############################################"
echo "###############################################"
echo "command delete -f jinja.yaml"
kubectl delete -f jinja.yaml
echo "###############################################"
echo "###############################################"
echo "command apply -f jinja-config.yaml"
kubectl apply -f jinja-config.yaml
echo "###############################################"
echo "###############################################"
echo "command apply -f jinja.yaml"
kubectl apply -f jinja.yaml
echo "###############################################"
echo "###############################################"