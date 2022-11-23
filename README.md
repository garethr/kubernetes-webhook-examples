# Kubernetes Admission Controller Demo in Python
Fork of https://github.com/garethr/kubernetes-webhook-examples

## Usage
```
kubectl create namespace webhook
bash deploy.sh
```

```
kubectl --namespace=webhook create secret tls webhook-certs --cert=keys/server.crt --key=keys/server.key
```

Note that pre-generated (insecure!) keys are available in the `keys` directory.


## Seeing the examples

First lets look at the mutating example. This adds a label to any pods it comes across. You can check the
`config/pod.yaml` file and see it doesn't contain the label `example.com/new-label`. The admission controller
adds the label with a random number as the value.

```console
$ kubectl apply -f config/pod.yaml
pod/nginx created
$ kubectl get -Lexample.com/new-label pod/nginx
NAME    READY   STATUS              RESTARTS   AGE   NEW-LABEL
nginx   0/1     ContainerCreating   0          0s    589
```

## Cleaning up
bash ./clean-up.sh

### Building image 
Log in to dockerhub
```
docker login
```
Build and push to dockerhub
```
docker build ./ -t aopopov/hook:latest
docker push aopopov/hook:latest
```