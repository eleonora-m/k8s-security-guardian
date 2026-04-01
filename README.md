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

### API Endpoints
- `GET /` - Health check
- `GET /api/v1/security/privileged-pods` - List privileged pods
- `GET /api/v1/security/cluster-admins` - List cluster-admin subjects

### Testing
```bash
python3 tests/test_security.py
```

## 🛠 Development

For testing without a real cluster, you can use Minikube or Kind.

### Running with Minikube
```bash
minikube start
# Configure kubeconfig to point to minikube
uvicorn src.main:app --reload
```

---
**👩‍💻 Author:** Eleonora Musaeva | DevOps & Cloud Engineer