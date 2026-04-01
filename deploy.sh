#!/usr/bin/env bash
set -euo pipefail

# project root
cd "$(dirname "$0")"

# 0. virtualenv activation
if [ -f venv/bin/activate ]; then
  source venv/bin/activate
else
  echo "[WARN] venv not found, using current Python env"
fi

# 1. apply manifests
echo "[1/5] Applying Kubernetes manifests..."
kubectl apply -f manifests/01-namespace.yaml
kubectl apply -f manifests/02-rbac.yaml
kubectl apply -f manifests/03-network-policies.yaml
kubectl apply -f manifests/04-pod-security.yaml
kubectl apply -f manifests/05-app.yaml

# 2. ensure resources
echo "[2/5] List resources..."
kubectl get ns security-guardian
kubectl get sa,role,rolebinding -n security-guardian
kubectl get deployment,pod -n security-guardian
kubectl get networkpolicy -n security-guardian

# 3. start uvicorn service
echo "[3/5] Starting uvicorn service (background)..."
pidfile=/tmp/k8s-security-guardian.pid
if [ -f "$pidfile" ] && kill -0 "$(cat $pidfile)" 2>/dev/null; then
  echo "Killing existing uvicorn PID $(cat $pidfile)"
  kill "$(cat $pidfile)"
  sleep 1
fi
nohup uvicorn src.main:app --host 0.0.0.0 --port 8000 > /tmp/k8s-security-guardian.log 2>&1 &
echo $! > "$pidfile"

# 4. smoke test API
echo "[4/5] Smoke test API..."
curl -sS http://localhost:8000/ && echo
curl -sS http://localhost:8000/api/v1/security/privileged-pods && echo
curl -sS http://localhost:8000/api/v1/security/cluster-admins && echo

# 5. done
echo "[5/5] Done. Logs: /tmp/k8s-security-guardian.log"