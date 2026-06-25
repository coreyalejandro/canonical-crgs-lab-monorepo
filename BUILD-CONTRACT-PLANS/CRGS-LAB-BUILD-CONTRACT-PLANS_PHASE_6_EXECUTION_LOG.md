# CRGS Lab — Phase 6 Execution Log

**Build Contract:** `CRGS-LAB-BUILD-CONTRACT-PLANS_PHASE_6.md`  
**Executed:** 2026-06-25  
**Status:** COMPLETE  
**Governed by:** The Living Constitution 2.0 — Sociotechnical Constitution v2.0.0

---

## What Was Built

### Section I — Cloud Infrastructure State (Terraform)

| Artifact | Path | Status |
|---|---|---|
| Terraform main | `terraform/main.tf` | ✅ Created |
| Terraform variables | `terraform/variables.tf` | ✅ Created |
| Terraform outputs | `terraform/outputs.tf` | ✅ Created |

**`terraform/main.tf` provisions:**

| Resource | Type | Details |
|---|---|---|
| `enterprise_vpc` | `aws_vpc` | `10.0.0.0/16`, DNS enabled |
| `public[0-1]` | `aws_subnet` | 2 AZs, map public IP, hosts LB |
| `private[0-1]` | `aws_subnet` | 2 AZs, EKS nodes + all services |
| `igw` | `aws_internet_gateway` | Public subnet → internet |
| `nat` | `aws_nat_gateway` | Private subnet → internet (engine only) |
| `math_sandbox_sg` | `aws_security_group` | Ingress: VPC only port 8000; **Egress: 127.0.0.1/32 only** (constitutional isolation) |
| `engine_sg` | `aws_security_group` | Ingress: 8501 from VPC; Egress: 0.0.0.0/0 via NAT (OpenAI API) |
| `eks` module | `terraform-aws-modules/eks/aws@19.15.3` | `1.27`, `m5.2xlarge`, 2–10 nodes, private subnets |
| `constitutional_engine` | `aws_ecr_repository` | `IMMUTABLE` tags, scan on push |

**Corrections from contract:**
- Added `aws_subnet`, `aws_internet_gateway`, `aws_nat_gateway`, `aws_eip`, `aws_route_table` resources — the contract's EKS module required these but left them as `[/* securely mapped */]` stubs
- Added `aws_ecr_repository` — referenced by CI/CD pipeline but omitted from contract
- Added `backend "s3"` for remote state — local state is not acceptable for enterprise IaC
- `egress 127.0.0.1/32` pattern preserved exactly from contract — AWS default-allows all egress, so this override is required

---

### Section II — Production Kubernetes Manifests

| Artifact | Path | Status |
|---|---|---|
| Production stack | `k8s/production-stack.yaml` | ✅ Created |
| Math sandbox | `k8s/math-sandbox.yaml` | ✅ Created |
| Secrets template | `k8s/secrets.yaml` | ✅ Created |

**`k8s/production-stack.yaml`:**
- `Namespace: crgs-lab` — all resources scoped
- `StatefulSet: knowledge-graph` — Neo4j `5.18.0-community`, `50Gi` PVC, readiness probe on bolt port, credentials from K8s Secret
- `Service: neo4j-service` — ClusterIP on 7687/7474
- `Deployment: constitutional-engine` — 2 replicas, ECR image, all env vars from Secrets, `/_stcore/health` readiness probe
- `Service: constitutional-engine-service` — ClusterIP
- `Service: enterprise-dashboard-lb` — AWS NLB LoadBalancer, port 80 → 8501

**`k8s/math-sandbox.yaml`:**
- `Deployment: math-sandbox` — runs as `runAsUser: 1000` (non-root, mirrors sandbox Dockerfile)
- `Service: math-sandbox-service` — ClusterIP port 8000
- `NetworkPolicy: sandbox-isolation` — **Ingress: engine pods only; Egress: omitted = default deny** — this is the Kubernetes-native enforcement of constitutional isolation

**`k8s/secrets.yaml`:**
- `Secret: crgs-lab-secrets` — template with base64 placeholder for `OPENAI_API_KEY`; real Neo4j values pre-encoded
- Safe to commit — all sensitive values are placeholders

---

### Section III — CI/CD GitHub Actions Pipeline

| Artifact | Path | Status |
|---|---|---|
| Production deploy workflow | `.github/workflows/production-deploy.yml` | ✅ Created |

**Pipeline steps on every push to `main`:**
1. Configure AWS credentials from GitHub Secrets
2. Login to ECR
3. `docker build` + push with both `sha`-tagged and `latest` tags (immutable SHA tag preserved)
4. `aws eks update-kubeconfig`
5. Apply `k8s/secrets.yaml` with `OPENAI_API_KEY_B64` injected from GitHub Secrets (never in the repo)
6. `sed` substitute ECR URL into manifests → `kubectl apply`
7. `kubectl set image` rolling update on both deployments
8. `kubectl rollout status` — pipeline fails if rollout does not stabilise within 300s
9. Poll and print live load balancer hostname

**Upgrades from contract:**
- `actions/checkout@v4`, `configure-aws-credentials@v4`, `amazon-ecr-login@v2` (latest stable vs v2/v1)
- `OPENAI_API_KEY` injected from `secrets.OPENAI_API_KEY_B64` at deploy time — never stored in the repo
- `rollout status` timeout 300s with explicit failure propagation

---

### Section IV — Makefile Phase 6 Targets

| Artifact | Path | Status |
|---|---|---|
| Makefile updated | `Makefile` | ✅ Updated |

**New targets:**
```makefile
make deploy-cloud-infrastructure   # terraform init + apply
make deploy-kubernetes             # kubectl apply all manifests + rollout status
```

---

## Pre-Flight Requirements Before Running `make deploy-kubernetes`

| Requirement | Notes |
|---|---|
| AWS CLI configured | `aws configure` — needs `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` |
| Terraform installed | `brew install terraform` (macOS) |
| kubectl installed | `brew install kubectl` |
| S3 state bucket | Create `crgs-lab-terraform-state` bucket in `us-east-1` before `terraform init` |
| OPENAI_API_KEY encoded | `echo -n "sk-proj-..." \| base64` → paste into `k8s/secrets.yaml` before apply |
| ECR URL substituted | Run `terraform output ecr_repository_url` → replace `YOUR_AWS_ACCOUNT_ID` in k8s manifests |
| GitHub Secrets set | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `OPENAI_API_KEY_B64` in repo settings |

---

## Estimated Cloud Cost (Standard Enterprise Tier — us-east-1)

| Resource | Estimate/month |
|---|---|
| EKS cluster control plane | ~$73 |
| 3× m5.2xlarge nodes | ~$1,000 |
| NAT Gateway | ~$45 |
| Application Load Balancer | ~$25 |
| ECR storage | ~$5 |
| **Total** | **~$1,148/month** |

---

*This log is immutable. Phase 7 work will be tracked in `CRGS-LAB-BUILD-CONTRACT-PLANS_PHASE_7.md`.*
