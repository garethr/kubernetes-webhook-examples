# Feature Namespace Webhook (Kubernetes Admission Controller) 

This repository contains an implementation of a webhook for feature namespaces. This webhook does the following things

* Act on feature namespaces (with a specific label)
* Mutate DNS config of pods to include services from the origin namespace

This will remove the need to copy all services to a feature namespace, and therefore reduce the efficiency of the feature namespaces.

