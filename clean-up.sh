k delete MutatingWebhookConfiguration mutating-webhook
k delete -f config/deployment.yaml
k delete -f config/pod.yaml --ignore-not-found
