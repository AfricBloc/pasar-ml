# 🏗 Pasar Infrastructure

This folder contains **all infrastructure and deployment configs** for the Pasar ML project.

---

## 📂 Structure

- **docker/** → Docker Swarm or production `docker-compose` files.
- **k8s/** → Kubernetes manifests for deploying Pasar agents.
- **terraform/** → Infrastructure-as-Code for cloud setup (AWS, GCP, Azure).
- **ansible/** → Server automation & configuration playbooks.

---

## ✅ Guidelines

- Keep environment-specific secrets in **`.env`** (never commit `.env` here!).
- Add **sample YAML/Terraform files** in each subfolder for reference.
- Use GitHub Actions to trigger deployments from this folder (future step).

---
