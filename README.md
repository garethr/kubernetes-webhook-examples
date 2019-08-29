# Kubernetes Admission Controller Demo in Python

This repository contains an example validating and mutating webhook implementation written in Python. This is mainly
intended for anyone looking at how self-hosted Kubernetes webhooks function, and contains a few components that might be of interest:

1. A basic web hook application, with both a validating and mutating examples
2. Kubernetes configuration for the various moving parts
3. A [Tilt](https://tilt.dev/) configuration for trying out the demos
4. An [Invoke](https://github.com/pyinvoke/invoke) tasks file for running through the examples, including generating private keys

The intention is to show a little more than a hello-world example, but not too much so you can't see how to use this in your own applications.


## Usage

First you'll need a Kubernetes cluster. For experiments like this [Kind](https://kind.sigs.k8s.io) is perfect as you can easily throw away the cluster afterwards.

Create a Kind cluster and then export the configuration, so `kubectl` and other tools know how to access the cluster.

```
kind create cluster
export KUBECONFIG=$(kind get kubeconfig-path
```

You can build the image and deploy the Kubernetes components, including a Deployment, Service, Namespace and the admission conrtollers, using Tilt. The following will set everything up and exit, but if you'd like to experiment with Tilt then remove all the flags and be suitably impressed.

```
tilt up --hud=false --no-browser --watch=false
```

You'll also need to create a secret with the certificates used to secure the traffic for the webhook, as Kubernetes requires these to be served over HTTPS.

```
kubectl --namespace=webhook create secret tls webhook-certs --cert=keys/server.crt --key=keys/server.key
```

Note that pre-generated (insecure!) keys are available in the `keys` directory. You can see how to generate these using `openssl` in the `tasks.py` file, or simple run `invoke generate-keys` and pass in the required arguments.


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

Now try and apply a podspec which specifies an environment variable. The validating webhook will reject the creation and
return an error:

```console
$ kubectl apply -f config/invalid-pod.yam
Error from server: error when creating "config/invalid-pod.yaml": admission webhook "webhook.webhook.svc" denied the request: env keys are prohibited
```

## Cleaning up

If you're using Kind then you can simply delete the cluster.

```
kind delete cluster
```

If not, you can remove all of the releated resources using tilt like so:

```
tilt down
```

