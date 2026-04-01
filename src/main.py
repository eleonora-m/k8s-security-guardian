from fastapi import FastAPI
from .k8s_analyzer import K8sSecurityAnalyzer

app = FastAPI(title="K8s Security Guardian API")
analyzer = K8sSecurityAnalyzer()

@app.get("/")
def read_root():
    return {"status": "Active", "system": "K8s Security Guardian", "mode": "Bare-Metal"}

@app.get("/api/v1/security/privileged-pods")
def get_privileged_pods():
    """Returns a list of pods running with root privileges"""
    return {"alert_level": "HIGH", "findings": analyzer.check_privileged_pods()}

@app.get("/api/v1/security/cluster-admins")
def get_cluster_admins():
    """Returns a list of subjects with cluster-admin rights"""
    return {"alert_level": "CRITICAL", "findings": analyzer.check_cluster_admins()}
