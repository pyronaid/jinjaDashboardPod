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
if [[ $(kubectl get configMap | grep -E "^springboot-config[ ]+" | wc -l) != 1 ]]; then
  echo "The springboot-config configMap is missing from k8. Launch it before"
  exit 1
fi

### build the docker images on minikube
versionApp=$(cat version.txt)
docker build --no-cache -t pyronaid/jinja_dashboard_app:${versionApp} --force-rm --no-cache .
cat password.txt | docker login --username pyronaid --password-stdin
docker push pyronaid/jinja_dashboard_app:${versionApp}
docker rmi --force pyronaid/jinja_dashboard_app:${versionApp}

cat gunicorn-cfg.py

# kustomization command
sed "s/#VERSIONAPP#/${versionApp}/g" jinja.yaml > jinja-toexecute.yaml

#refresh installation
echo "command delete -f jinja-toexecute.yaml"
kubectl delete -f jinja-toexecute.yaml
echo "###############################################"
echo "###############################################"
echo "command delete -f jinja-ingress.yaml"
kubectl delete -f jinja-ingress.yaml
echo "###############################################"
echo "###############################################"
echo "command apply -f jinja-toexecute.yaml"
kubectl apply -f jinja-toexecute.yaml
echo "###############################################"
echo "###############################################"
echo "command apply -f jinja-ingress.yaml"
kubectl apply -f jinja-ingress.yaml
echo "###############################################"
echo "###############################################"