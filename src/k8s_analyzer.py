from kubernetes import client, config
from kubernetes.client.rest import ApiException

class K8sSecurityAnalyzer:
    def __init__(self):
        try:
            config.load_kube_config()
            self.core_v1 = client.CoreV1Api()
            self.rbac_v1 = client.RbacAuthorizationV1Api()
        except Exception:
            pass # Silent fail for environment without active K8s context

    def check_privileged_pods(self):
        risky_pods = []
        try:
            pods = self.core_v1.list_pod_for_all_namespaces()
            for pod in pods.items:
                for container in pod.spec.containers:
                    if container.security_context and container.security_context.privileged:
                        risky_pods.append({
                            "namespace": pod.metadata.namespace,
                            "pod_name": pod.metadata.name,
                            "container": container.name
                        })
        except ApiException:
            return [{"error": "Unable to connect to K8s API"}]
        return risky_pods

    def check_cluster_admins(self):
        admins = []
        try:
            bindings = self.rbac_v1.list_cluster_role_binding()
            for binding in bindings.items:
                if binding.role_ref.name == "cluster-admin" and binding.subjects:
                    for subject in binding.subjects:
                        admins.append({"kind": subject.kind, "name": subject.name})
        except ApiException:
            return [{"error": "Unable to connect to K8s API"}]
        return admins