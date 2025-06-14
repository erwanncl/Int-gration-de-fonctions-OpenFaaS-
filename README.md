# TP2 – Chaîne de traitement de commandes OpenFaaS

## Prérequis

- Docker Desktop + Minikube  
- `kubectl`, `helm`, `faas-cli`  
- PowerShell ou bash

---

## 1. Démarrer Minikube & Kubernetes

```bash
minikube start --driver=docker --cpus=4 --memory=4096 --disk-size=20g
kubectl config use-context minikube
```

---

## 2. Installer OpenFaaS

```bash
helm repo add openfaas https://openfaas.github.io/faas-netes/
helm repo update

kubectl create namespace openfaas --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace openfaas-fn --dry-run=client -o yaml | kubectl apply -f -

helm install openfaas openfaas/openfaas \
  --namespace openfaas \
  --set functionNamespace=openfaas-fn \
  --set generateBasicAuth=true \
  --set faasnetes.imagePullPolicy=IfNotPresent \
  --set gateway.image=ghcr.io/openfaas/gateway:0.27.12
```

### 🔐 Récupérer le mot de passe admin :

```bash
kubectl -n openfaas get secret basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 -d
```

### 🔑 Se connecter à OpenFaaS :

```bash
faas-cli login --gateway http://127.0.0.1:8080 \
  --username admin --password <PASSWORD>
```

### 🚪 Ouvrir l’accès local :

```bash
kubectl -n openfaas port-forward svc/gateway 8080:8080
```

---

## 3. Créer les secrets

```bash
kubectl -n openfaas-fn create secret generic sftp-host     --from-literal=host="ftp.heab7543.odns.fr"
kubectl -n openfaas-fn create secret generic sftp-user     --from-literal=user="formation_openfaas@heab7543.odns.fr"
kubectl -n openfaas-fn create secret generic sftp-password --from-literal=pass="}{?Z]~Pxq!R9"
kubectl -n openfaas-fn create secret generic user-id       --from-literal=USER_ID="USX"
```

---

## 4. Déployer les fonctions

```bash
faas-cli up -f stack.yaml --gateway http://127.0.0.1:8080
```

---

## 5. Tests

### 🔁 CRON → NATS

```bash
curl -X POST http://127.0.0.1:8080/function/daily-fetcher
```

### 📄 Consommation & CSV

```bash
faas-cli logs file-transformer --gateway http://127.0.0.1:8080
kubectl -n openfaas-fn exec deploy/file-transformer -- head -n5 /home/app/function/output.csv
```

### 🌐 Vérification du status HTTP

```bash
curl http://127.0.0.1:8080/function/status-checker
```
