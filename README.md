# End-to-End DevOps Final Project — Flask, Jenkins & GitOps

**Project checklist · Verified lab evidence · Updated 17 November 2026**

**Objective:** Build and test a Python Flask application, package it as a Docker image, automate CI with Jenkins, publish the image to Docker Hub, and deploy it to Kubernetes using GitOps and Argo CD.

## Project status at a glance

| Area | Status | Evidence |
|---|---|---|
| Git repository | ✅ Verified | `hatif007/devops-final-exam`; local `dev` branch matches `origin/dev` |
| Flask application | ✅ Verified | `/` and `/online` responded successfully on port `8082` |
| Automated tests | ✅ Verified | Jenkins Build #5: **3 passed** |
| Jenkins CI | ✅ Verified | Build #5 finished `SUCCESS` |
| Flake8 | ✅ Executed — findings | 7 style violations |
| Bandit | ✅ Executed — findings | 1 Medium and 4 Low findings |
| Trivy | ✅ Executed — findings | 51 High, 0 Critical findings in image `:5` |
| Docker image | ✅ Verified | Built and pushed `hatif007/devops-final-exam:5` |
| GitOps update | ✅ Verified | DEV tag changed from `22` to `5`; commit `056c95f` pushed |
| Kubernetes environments | ✅ Verified | DEV `2/2`, QA `1/1`, PRD `5/5` ready |
| Argo CD | ✅ Verified | DEV, QA and PRD: `Synced` and `Healthy` |
| LoadBalancer services | ✅ Verified | Minikube tunnel assigned local external IP `127.0.0.1` |
| GitHub Actions | ⬜ To complete | Workflow implementation and testing |
| Slack alerts | ⬜ To complete | CI/CD notifications and alert testing |
| Prometheus and Grafana | ⬜ To complete | Monitoring stack and dashboards |

## Part 1 — Source code and application

- [x] Work with Git branches (`dev`, `main`, `Feature`).
- [x] Keep the application and pipeline configuration in GitHub.
- [x] Implement Flask endpoints: `/` and `/online`.
- [x] Run three automated Python tests with `pytest`.
- [x] Containerize the application with `Dockerfile` (`python:3.13-slim`, port `8082`).

**HTTP evidence:**

```text
GET /       -> Hello! The Python application is running successfully.
GET /online -> {"application":"alive","status":"online"}
```

## Part 2 — Jenkins CI and security scans

- [x] Configure Jenkins pipeline with Kubernetes-based build agents.
- [x] Install Python dependencies and execute `pytest` (**3/3 passed**).
- [x] Run **Flake8** and **Bandit** in parallel.
- [x] Build Docker image `devops-final-exam:5`.
- [x] Run **Trivy** against the built image.
- [x] Authenticate and push `hatif007/devops-final-exam:5` to Docker Hub.
- [x] Update the GitOps repository from the pipeline.

**Actual findings in Jenkins Build #5:** Flake8: **7** style violations; Bandit: **1 Medium + 4 Low**; Trivy: **51 High + 0 Critical** (46 Debian OS findings and 5 Python-package findings).

**Important:** These scanning tools were successfully integrated and executed, but their checks **did not pass cleanly**. Jenkins uses `catchError`, so findings were logged and the pipeline continued to publish and deploy the image. `Finished: SUCCESS` is **not** a security clearance.

## Part 3 — GitOps, Kubernetes and Argo CD

GitOps repository: [hatif007/devops-final-exam-gitops](https://github.com/hatif007/devops-final-exam-gitops)

- [x] Maintain separate configuration for DEV, QA and PRD.
- [x] Update DEV `environments/dev/values.yaml` automatically with `yq`.
- [x] Commit and push the updated DEV image tag (`056c95f`).
- [x] Synchronize deployments with Argo CD.
- [x] Verify all three Argo CD applications as **Synced / Healthy**.
- [x] Verify Kubernetes deployment readiness and image tags.
- [x] Start Minikube tunnel and verify local LoadBalancer IP assignment.

| Environment | Deployed image | Ready replicas | Argo CD |
|---|---|---:|---|
| DEV | `hatif007/devops-final-exam:5` | 2/2 | Synced / Healthy |
| QA | `hatif007/devops-final-exam:22` | 1/1 | Synced / Healthy |
| PRD | `hatif007/devops-final-exam:22` | 5/5 | Synced / Healthy |

**Note:** DEV was updated to `:5`; QA and PRD remained on `:22`. The tunnel provides local access (`127.0.0.1`), not a public internet address.

## End-to-end verified flow

```text
GitHub source (dev)
       |
       v
Jenkins Build #5 -> pytest + Flake8 + Bandit
       |
       v
Docker build -> Trivy scan -> Docker Hub :5
       |
       v
GitOps DEV values.yaml -> commit 056c95f
       |
       v
Argo CD (Synced / Healthy)
       |
       v
Kubernetes DEV (2/2 Ready, image :5)
       |
       v
Flask HTTP endpoints verified
```

## Remaining checklist

- [ ] **GitHub Actions** — Implement and test CI workflow(s).
- [ ] **Slack Alerts** — Configure and verify pipeline notifications.
- [ ] **Prometheus and Grafana** — Set up monitoring and dashboards.
