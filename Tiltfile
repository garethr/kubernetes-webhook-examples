allow_k8s_contexts("kubernetes-admin@webhook")

k8s_yaml("config/deployment.yaml")
k8s_yaml(["config/mutate.yaml", "config/validate.yaml"])

docker_build("garethr/hook", ".")
