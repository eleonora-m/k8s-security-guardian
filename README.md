# 🔐 K8s Security Guardian (Bare-Metal Edition)

This project demonstrates a production-grade, security-first approach to Kubernetes infrastructure and observability. It is specifically designed for **on-premise / bare-metal** environments, bypassing managed cloud services to maintain strict data residency and air-gapped compatibility.

## 🏗 Architecture & Stack
* **Infrastructure as Code (IaC):** Ansible (Node bootstrapping, OS hardening)
* **Container Orchestration:** Kubernetes (Strict RBAC, Network Policies, Pod Security)
* **Security Dashboard API:** Python / FastAPI / Kubernetes python-client
* **Observability:** Audit log parsing & Privileged container detection

## 🚀 Key Features
1. **Automated Bare-Metal Prep:** Ansible playbooks to disable swap, configure `sysctl`, and install container runtimes.
2. **Zero-Trust Networking:** Default-deny Network Policies applied at the namespace level.
3. **Automated Security Auditing:** A custom Python API that interacts directly with the K8s API Server to detect:
   - Pods running in `privileged` mode (Root access risk).
   - Over-permissive RBAC bindings (Cluster-admin sprawl).

## 📂 Project Structure
* `/ansible` - Infrastructure bootstrapping and OS-level compliance.
* `/manifests` - K8s YAMLs for strict RBAC, Namespaces, and Network Policies.
* `/src` - Custom Python (FastAPI) security dashboard connecting to K8s API.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Kubernetes cluster access (kubeconfig configured)
- Ansible (for infrastructure provisioning)

### Installation
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the API Server
```bash
uvicorn src.main:app --reload
```

### Automated Deployment & Testing
Use the provided `deploy.sh` script for automated deployment and verification:

```bash
# Make script executable and run
chmod +x deploy.sh
./deploy.sh
```

The script will:
1. Apply all Kubernetes manifests
2. Validate resource creation
3. Start the security API server
4. Run smoke tests on all endpoints

### API Endpoints
- `GET /` - Health check
- `GET /api/v1/security/privileged-pods` - List privileged pods
- `GET /api/v1/security/cluster-admins` - List cluster-admin subjects

### Testing
```bash
python3 tests/test_security.py
```

## 🔍 Security Analysis Demo

### 1. Deploy Security Manifests
```bash
kubectl apply -f manifests/
```

### 2. Create a Vulnerable Pod (For Testing)
```bash
kubectl apply -f manifests/bad-pod.yaml
```

### 3. Run Security Analysis
```bash
# Start API server
uvicorn src.main:app --host 0.0.0.0 --port 8000

# Check for privileged pods (in another terminal)
curl http://localhost:8000/api/v1/security/privileged-pods
```

**Expected Output:**
```json
{
  "alert_level": "HIGH",
  "findings": [
    {
      "namespace": "default",
      "pod_name": "hacker-pod",
      "container": "evil-container"
    }
  ]
}
```

### 4. Check RBAC Analysis
```bash
curl http://localhost:8000/api/v1/security/cluster-admins
```

**Expected Output:**
```json
{
  "alert_level": "CRITICAL", 
  "findings": [
    {
      "kind": "Group",
      "name": "system:masters"
    }
  ]
}
```

## 🛠 Development

For testing without a real cluster, you can use Minikube or Kind.

### Running with Minikube
```bash
minikube start
# Configure kubeconfig to point to minikube
uvicorn src.main:app --reload
```

## 🔧 Troubleshooting

### PodSecurity Violations
If you encounter PodSecurity admission errors:
```bash
kubectl describe pod <pod-name> -n security-guardian
```
Common fixes:
- Add `seccompProfile: { type: RuntimeDefault }` to securityContext
- Ensure `runAsNonRoot: true` and `runAsUser` is set
- Drop unnecessary capabilities

### API Connection Issues
- Verify kubeconfig: `kubectl cluster-info`
- Check service account permissions: `kubectl auth can-i list pods --as=system:serviceaccount:security-guardian:security-analyzer`

### Port Already in Use
If port 8000 is busy:
```bash
lsof -i :8000
uvicorn src.main:app --host 0.0.0.0 --port 8080
```

---
**👩‍💻 Author:** Eleonora Musaeva | DevOps & Cloud Engineer