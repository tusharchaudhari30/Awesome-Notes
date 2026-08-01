# AWS Cloud Practitioner (CLF-C02) — Awesome Notes

> Complete study notes for the AWS Certified Cloud Practitioner exam — covering all four domains, the key services, and the exam-trap distinctions.

## Exam Overview

| Item | Detail |
|---|---|
| Exam code | CLF-C02 |
| Questions | 65 (50 scored + 15 unscored), multiple choice & multiple response |
| Duration | 90 minutes |
| Passing score | 700 / 1000 (scaled) |
| Level | Foundational — no hands-on prerequisite |

**Domain weights:**

| Domain | Weight |
|---|---|
| 1. Cloud Concepts | 24% |
| 2. Security & Compliance | 30% |
| 3. Cloud Technology & Services | 34% |
| 4. Billing, Pricing & Support | 12% |

## Table of Contents

- [Domain 1 — Cloud Concepts](#domain-1--cloud-concepts)
  - [What is Cloud Computing?](#what-is-cloud-computing)
  - [Benefits of the Cloud](#benefits-of-the-cloud)
  - [Cloud Service Models (IaaS / PaaS / SaaS)](#cloud-service-models-iaas--paas--saas)
  - [Cloud Deployment Models](#cloud-deployment-models)
  - [AWS Global Infrastructure](#aws-global-infrastructure)
  - [Well-Architected Framework](#well-architected-framework)
  - [Cloud Adoption Framework (CAF) & Migration](#cloud-adoption-framework-caf--migration)
- [Domain 2 — Security & Compliance](#domain-2--security--compliance)
  - [Shared Responsibility Model](#shared-responsibility-model)
  - [IAM — Identity and Access Management](#iam--identity-and-access-management)
  - [Security Services](#security-services)
  - [Encryption & Key Management](#encryption--key-management)
  - [Compliance & Governance](#compliance--governance)
- [Domain 3 — Cloud Technology & Services](#domain-3--cloud-technology--services)
  - [Compute](#compute)
  - [Storage](#storage)
  - [Databases](#databases)
  - [Networking & Content Delivery](#networking--content-delivery)
  - [Application Integration](#application-integration)
  - [Analytics](#analytics)
  - [Machine Learning & AI Services](#machine-learning--ai-services)
  - [Developer Tools & IaC](#developer-tools--iac)
  - [Management & Monitoring](#management--monitoring)
  - [Migration & Transfer](#migration--transfer)
- [Domain 4 — Billing, Pricing & Support](#domain-4--billing-pricing--support)
  - [Pricing Fundamentals](#pricing-fundamentals)
  - [EC2 Purchasing Options](#ec2-purchasing-options)
  - [Cost Management Tools](#cost-management-tools)
  - [AWS Organizations & Consolidated Billing](#aws-organizations--consolidated-billing)
  - [Support Plans](#support-plans)
- [Exam Traps & Service One-Liners](#exam-traps--service-one-liners)
- [Final Exam Tips](#final-exam-tips)

---

# Domain 1 — Cloud Concepts

## What is Cloud Computing?

**Cloud computing** = on-demand delivery of IT resources (compute, storage, databases, networking) over the internet with **pay-as-you-go** pricing — instead of buying and maintaining your own data centers.

**Five essential characteristics:**

1. **On-demand self-service** — provision resources yourself, no human intermediary.
2. **Broad network access** — available over the network from anywhere.
3. **Resource pooling** — multi-tenant, shared infrastructure.
4. **Rapid elasticity** — scale up/down quickly, appears unlimited.
5. **Measured service** — usage metered; pay only for what you use.

**Key vocabulary:**

- **Scalability** — ability to handle growth by adding resources.
  - *Vertical scaling (scale up)* — bigger instance.
  - *Horizontal scaling (scale out)* — more instances (preferred in cloud).
- **Elasticity** — automatically acquire/release resources to match demand (Auto Scaling).
- **Agility** — speed to provision resources (minutes, not weeks) and experiment.
- **High availability (HA)** — system stays operational despite failures (multi-AZ).
- **Fault tolerance** — system keeps working even when components fail.
- **Disaster recovery (DR)** — recovering from catastrophic events (multi-Region). Strategies from cheap/slow to costly/fast: **Backup & Restore → Pilot Light → Warm Standby → Multi-site Active/Active**.
- **CapEx → OpEx** — cloud replaces upfront capital expense with variable operational expense.

## Benefits of the Cloud

The classic **six advantages of cloud computing** (know these!):

1. **Trade fixed expense for variable expense** — pay only when you consume.
2. **Benefit from massive economies of scale** — AWS's scale = lower prices.
3. **Stop guessing capacity** — scale with actual demand; no over/under-provisioning.
4. **Increase speed and agility** — resources in minutes; faster experimentation.
5. **Stop spending money running and maintaining data centers** — focus on customers, not racking servers.
6. **Go global in minutes** — deploy to Regions worldwide with a few clicks.

## Cloud Service Models (IaaS / PaaS / SaaS)

| Model | You manage | AWS manages | Example |
|---|---|---|---|
| **IaaS** | OS, runtime, apps, data | Hardware, virtualization, networking | EC2, EBS, VPC |
| **PaaS** | Apps, data | Everything below (OS, runtime, scaling) | Elastic Beanstalk, RDS, Lambda* |
| **SaaS** | Just your usage/config | The entire application | Amazon Chime, Gmail, Salesforce |

*Lambda is often called FaaS/serverless — an extreme of PaaS.

Mnemonic: pizza analogy — IaaS = kitchen provided, you cook; PaaS = pizza delivered, you serve; SaaS = dining out.

## Cloud Deployment Models

| Model | Description | When |
|---|---|---|
| **Public cloud** | All on AWS | Default; full cloud benefits |
| **Private cloud (on-premises)** | Own data center, cloud-like tooling | Regulatory / legacy needs |
| **Hybrid** | On-prem + cloud connected (Direct Connect, VPN, Outposts, Storage Gateway) | Gradual migration, data residency |
| **Multi-cloud** | Multiple providers | Vendor risk diversification |

## AWS Global Infrastructure

```
Region  ⊃  Availability Zones (AZs)  ⊃  Data centers
   +  Edge Locations (CloudFront)  +  Local Zones  +  Wavelength  +  Outposts
```

- **Region** — a physical geographic area (e.g., `ap-south-1` Mumbai). Contains **≥ 3 AZs** (minimum 2, new regions 3+). Choose a region by: **compliance/data residency, latency to users, service availability, price**.
- **Availability Zone (AZ)** — one or more discrete data centers with redundant power/network, isolated from other AZs' failures, connected by low-latency private fiber. **Deploy across ≥ 2 AZs for high availability.**
- **Edge Locations** — 400+ sites for **CloudFront (CDN)** and **Route 53** — cache content close to users. Far more numerous than Regions.
- **Local Zones** — AWS infrastructure extension near large population centers for single-digit-ms latency.
- **AWS Outposts** — AWS hardware racks physically installed **in your data center** (hybrid).
- **AWS Wavelength** — AWS compute embedded in 5G telecom networks for ultra-low latency.

**Most services are Regional** (EC2, RDS); some are **Global** (IAM, Route 53, CloudFront, WAF).

## Well-Architected Framework

**Six pillars** (mnemonic: **CROSS + P** or "Security OPS CoRe"):

| Pillar | Focus | Example practice |
|---|---|---|
| **Operational Excellence** | Run & monitor, continuously improve | IaC, small reversible changes, runbooks |
| **Security** | Protect data/systems | Least privilege, encrypt everywhere, traceability |
| **Reliability** | Recover from failure, meet demand | Multi-AZ, auto scaling, test recovery |
| **Performance Efficiency** | Use resources efficiently | Right-size, serverless, go global |
| **Cost Optimization** | Avoid unneeded cost | Right pricing model, measure, stop idle resources |
| **Sustainability** | Minimize environmental impact | Maximize utilization, managed services |

**AWS Well-Architected Tool** — free console tool to review workloads against the pillars.

## Cloud Adoption Framework (CAF) & Migration

**AWS CAF** — guidance to plan cloud transformation across **six perspectives**:
Business, People, Governance (business capabilities) + Platform, Security, Operations (technical capabilities).

**The 7 Rs of migration strategies:**

| Strategy | Meaning |
|---|---|
| **Rehost** | "Lift and shift" — move as-is (fastest) |
| **Replatform** | "Lift, tinker, and shift" — minor optimizations (e.g., DB → RDS) |
| **Repurchase** | Move to SaaS (e.g., CRM → Salesforce) |
| **Refactor / Re-architect** | Rebuild cloud-native (most effort, most benefit) |
| **Relocate** | Move VMware/containers wholesale (e.g., VMware Cloud on AWS) |
| **Retain** | Keep on-prem for now |
| **Retire** | Decommission what's unused |

---

# Domain 2 — Security & Compliance

## Shared Responsibility Model

**The most-tested concept on the exam.**

- **AWS: security *OF* the cloud** — hardware, software, networking, facilities that run AWS services; physical security; hypervisor; managed-service patching.
- **Customer: security *IN* the cloud** — your data, IAM users/permissions, OS patching (on EC2), network/firewall config (security groups, NACLs), client & server-side encryption, application security.

Responsibility shifts with the service model:

| Task | EC2 (IaaS) | RDS (managed) | Lambda/S3 (serverless) |
|---|---|---|---|
| Physical/hypervisor | AWS | AWS | AWS |
| OS patching | **Customer** | AWS | AWS |
| App/data/IAM/encryption config | Customer | Customer | Customer |

**Always customer:** data, IAM, encryption choices. **Always AWS:** physical infrastructure, global network, host hypervisor.

## IAM — Identity and Access Management

Global, free service controlling **who** (authentication) can do **what** (authorization) on which resources.

- **Root user** — created with the account; unrestricted. **Best practice:** enable MFA, don't use it daily, no root access keys; use it only for root-only tasks (closing account, changing support plan).
- **IAM User** — a person/app with long-term credentials (password / access keys).
- **IAM Group** — collection of users; attach policies to groups, not individuals.
- **IAM Role** — temporary credentials **assumed** by users, services (e.g., EC2 instance role), or external identities. **Preferred over access keys** — especially for EC2/Lambda accessing AWS APIs.
- **IAM Policy** — JSON document: `Effect` (Allow/Deny), `Action`, `Resource`, optional `Condition`. **Explicit Deny always wins.** Default is implicit deny.
- **Least privilege** — grant only permissions needed. Start minimal, expand as required.
- **MFA** — something you know + something you have. Enable for root and all users.
- **IAM Identity Center (SSO)** — single sign-on to multiple accounts/apps with a corporate directory.
- **IAM Access Analyzer / Credential Report / Access Advisor** — audit external access, credential age, unused permissions.
- **STS** — issues temporary security credentials (what roles use under the hood).

## Security Services

| Service | One-liner |
|---|---|
| **AWS WAF** | Web Application Firewall — blocks SQL injection, XSS, bad IPs at Layer 7 (on CloudFront/ALB/API Gateway) |
| **AWS Shield Standard** | Free, automatic **DDoS** protection for everyone |
| **AWS Shield Advanced** | Paid 24/7 DDoS response team + cost protection |
| **Amazon GuardDuty** | Intelligent **threat detection** — ML on CloudTrail/VPC Flow/DNS logs |
| **Amazon Inspector** | Automated **vulnerability scanning** of EC2, ECR images, Lambda |
| **Amazon Macie** | ML-based discovery of **sensitive data / PII in S3** |
| **AWS Security Hub** | Central dashboard aggregating security findings across services |
| **Amazon Detective** | Investigate/root-cause security findings |
| **AWS Firewall Manager** | Centrally manage WAF/Shield/security-group rules across accounts |
| **AWS Secrets Manager** | Store & **auto-rotate** secrets (DB passwords, API keys) |
| **AWS Systems Manager Parameter Store** | Config/secret storage (no auto-rotation on standard tier) |
| **AWS Artifact** | **On-demand download of compliance reports** (SOC, PCI, ISO) |
| **Amazon Cognito** | Authentication (sign-up/sign-in) for **your web/mobile app users** |
| **AWS Trusted Advisor** | Best-practice checks: cost, performance, **security**, fault tolerance, service limits |

**Network-level protection:**

- **Security Group** — instance-level virtual firewall; **stateful**; allow rules only.
- **Network ACL** — subnet-level; **stateless**; allow *and* deny rules; evaluated in order.

## Encryption & Key Management

- **In transit** — TLS/SSL (use **ACM** — AWS Certificate Manager, free public certs).
- **At rest** — **AWS KMS** (Key Management Service) manages encryption keys; integrates with S3, EBS, RDS, etc.
- **AWS CloudHSM** — dedicated, single-tenant **hardware security modules** you control (compliance-driven).
- S3 encrypts new objects by default (SSE-S3).

## Compliance & Governance

- **AWS Artifact** — self-service compliance reports & agreements.
- **AWS Config** — records resource **configuration history** and evaluates rules ("is every S3 bucket encrypted?"). Answers *"what changed?"*
- **AWS CloudTrail** — logs **every API call** (who did what, when, from where). Answers *"who did it?"* Enabled by default (90-day event history).
- **AWS Audit Manager** — continuously audits usage against frameworks (PCI, GDPR).
- **AWS Organizations SCPs** — Service Control Policies set **maximum permissions** for member accounts (guardrails).
- **AWS Control Tower** — automated setup of a secure, governed **multi-account landing zone** with guardrails.
- **Data residency** — data stays in the Region you choose; AWS doesn't move it.
- **Penetration testing** — allowed **without prior approval** for common services (EC2, RDS, Lambda…), but DDoS simulation requires approval.

---

# Domain 3 — Cloud Technology & Services

Ways to interact with AWS: **Management Console** (web UI), **CLI**, **SDKs** (programmatic), **Infrastructure as Code** (CloudFormation/CDK).

## Compute

### Amazon EC2 (Elastic Compute Cloud)

Resizable virtual machines (instances).

- **AMI** — Amazon Machine Image; template (OS + software) to launch instances.
- **Instance families:** General purpose (t3, m5) • Compute optimized (c5) • Memory optimized (r5, x1) • Storage optimized (i3, d2) • Accelerated/GPU (p4, g5).
- **User data** — bootstrap script at first launch.
- **Security groups** control traffic; **key pairs** for SSH.
- **Placement, tenancy:** Shared (default) • **Dedicated Instances** (hardware not shared with other accounts) • **Dedicated Hosts** (entire physical server — for BYOL licensing/compliance).

### Scaling & Load Balancing

- **Auto Scaling Group (ASG)** — automatically adds/removes instances based on demand (elasticity) and replaces unhealthy ones (self-healing). Set min/max/desired.
- **Elastic Load Balancing (ELB)** — distributes traffic across targets in multiple AZs (high availability):
  - **ALB** — Layer 7 (HTTP/HTTPS), path-based routing.
  - **NLB** — Layer 4 (TCP/UDP), extreme performance, static IP.
  - **GWLB** — for third-party network appliances.

### Serverless & Containers

| Service | One-liner |
|---|---|
| **AWS Lambda** | Run code without servers; pay per request + duration (ms); max 15-min runtime; event-driven |
| **AWS Fargate** | **Serverless compute for containers** — no EC2 to manage |
| **Amazon ECS** | AWS-native container orchestration |
| **Amazon EKS** | Managed **Kubernetes** |
| **Amazon ECR** | Container image registry |
| **Elastic Beanstalk** | PaaS — upload code, AWS handles provisioning/scaling/monitoring (you keep resource control) |
| **AWS App Runner** | Simplest way to run a containerized web app from source/image |
| **Amazon Lightsail** | Simple VPS with predictable monthly price — for beginners/simple apps |
| **AWS Batch** | Run batch computing jobs at scale |
| **AWS Wavelength / Local Zones / Outposts** | Compute at the edge / on-prem |

*Serverless* = no server management, auto scaling, pay-for-use, built-in HA: **Lambda, Fargate, S3, DynamoDB, SQS, SNS, API Gateway, Aurora Serverless**.

## Storage

### Amazon S3 (Simple Storage Service)

**Object storage** — files stored as objects in globally-unique-named **buckets** (data itself lives in a Region). Virtually unlimited; object max 5 TB. **11 nines (99.999999999%) durability.**

**Storage classes:**

| Class | Use case |
|---|---|
| S3 Standard | Frequent access, default |
| S3 Intelligent-Tiering | Unknown/changing access patterns — auto-moves tiers |
| S3 Standard-IA | Infrequent access, rapid retrieval, cheaper storage / retrieval fee |
| S3 One Zone-IA | Infrequent, non-critical, single AZ (cheaper, less resilient) |
| S3 Glacier Instant Retrieval | Archive with millisecond access |
| S3 Glacier Flexible Retrieval | Archive; minutes–hours retrieval |
| S3 Glacier Deep Archive | Cheapest; 12–48 h retrieval; long-term compliance |

**Features:** versioning, lifecycle policies (auto-transition/expire), replication (CRR/SRR), static website hosting, encryption by default, Block Public Access (on by default), S3 Transfer Acceleration (fast global uploads via edge locations), presigned URLs.

### Block & File Storage

| Service | Type | One-liner |
|---|---|---|
| **EBS** (Elastic Block Store) | Block | Network-attached disk for **one EC2 instance** (in same AZ); persists independently; snapshot to S3 |
| **Instance Store** | Block | Physically attached, **ephemeral** — data lost on stop/terminate; fastest |
| **EFS** (Elastic File System) | File (NFS, Linux) | Shared file system for **many instances across AZs**; auto-scales |
| **FSx for Windows** | File (SMB) | Managed Windows file share (Active Directory) |
| **FSx for Lustre** | File | High-performance computing file system |
| **Storage Gateway** | Hybrid | On-prem access to cloud storage (File/Volume/Tape gateway) |
| **AWS Backup** | — | Centralized, policy-based backups across services |
| **Snow Family** | Physical | **Snowcone / Snowball Edge / (Snowmobile-retired)** — physical devices to migrate TB–PB offline or compute at edge |

## Databases

| Service | Type | One-liner |
|---|---|---|
| **RDS** | Relational (SQL) | Managed MySQL, PostgreSQL, MariaDB, Oracle, SQL Server; **Multi-AZ = HA (failover)**, **Read Replicas = read scaling** |
| **Aurora** | Relational | AWS-built, MySQL/PostgreSQL-compatible, up to 5×/3× faster, 6 copies across 3 AZs; Serverless option |
| **DynamoDB** | Key-value/NoSQL | Serverless, single-digit-ms latency at any scale; **DAX** = in-memory cache for it; Global Tables = multi-region |
| **ElastiCache** | In-memory cache | Managed **Redis / Memcached** — microsecond reads, offload DBs |
| **Redshift** | Data warehouse | Petabyte-scale **OLAP / analytics** (columnar); not for transactions |
| **DocumentDB** | Document | MongoDB-compatible |
| **Neptune** | Graph | Relationships — social networks, fraud detection |
| **QLDB** | Ledger | Immutable, cryptographically verifiable transaction log |
| **Keyspaces** | Wide column | Cassandra-compatible |
| **Timestream** | Time series | IoT/operational metrics |
| **MemoryDB** | In-memory DB | Redis-compatible, durable primary database |

**OLTP (transactions) → RDS/Aurora/DynamoDB. OLAP (analytics) → Redshift.**

## Networking & Content Delivery

- **VPC (Virtual Private Cloud)** — your logically isolated network in a Region. Contains **subnets** (public = route to internet, private = not), spans AZs.
  - **Internet Gateway (IGW)** — VPC ↔ internet.
  - **NAT Gateway** — lets **private** subnets reach out to the internet (not in).
  - **Route Tables** — control traffic routing.
  - **VPC Peering** — connect two VPCs (non-transitive).
  - **Transit Gateway** — hub connecting many VPCs & on-prem (transitive).
  - **VPC Endpoints** — private connection to AWS services (S3, DynamoDB) without internet.
  - **VPC Flow Logs** — capture IP traffic metadata for troubleshooting.
- **Route 53** — managed **DNS** (global); health checks; routing policies (simple, weighted, latency, failover, geolocation).
- **CloudFront** — **CDN**; caches content at edge locations globally; DDoS protection with Shield/WAF; low latency for static & dynamic content.
- **AWS Global Accelerator** — improves global app performance by routing over AWS backbone using static anycast IPs (does **not** cache — vs CloudFront).
- **Direct Connect** — **dedicated private physical line** on-prem → AWS (consistent bandwidth, weeks to provision).
- **Site-to-Site VPN** — encrypted tunnel over the **internet** on-prem → AWS (quick to set up).
- **Client VPN** — individual laptops → AWS securely.
- **API Gateway** — create, publish, secure APIs at scale (fronts Lambda commonly); throttling, auth, versioning.
- **PrivateLink** — expose a service privately to other VPCs.

## Application Integration

| Service | One-liner |
|---|---|
| **SQS** | **Queue** — decouple producers/consumers; pull-based; messages persisted up to 14 days; Standard vs FIFO |
| **SNS** | **Pub/Sub notifications** — push one message to many subscribers (email, SMS, Lambda, SQS fan-out) |
| **EventBridge** | Serverless **event bus** — route events between AWS services & SaaS apps; scheduler |
| **Step Functions** | Visual **workflow orchestration** of Lambda/services (state machines) |
| **Amazon MQ** | Managed message broker (ActiveMQ/RabbitMQ) for lift-and-shift of existing apps |
| **AppSync** | Managed GraphQL APIs |
| **SES** | Bulk transactional **email** sending |

Decoupling with queues = fault tolerance + independent scaling (loose coupling).

## Analytics

| Service | One-liner |
|---|---|
| **Athena** | **Serverless SQL directly on S3** data; pay per query scanned |
| **QuickSight** | Serverless **BI dashboards** / visualization |
| **Kinesis** | **Real-time streaming** data ingestion & analytics |
| **AWS Glue** | Serverless **ETL** (extract-transform-load) + Data Catalog |
| **EMR** | Managed big-data clusters (Hadoop/Spark) |
| **Data Exchange** | Find & subscribe to third-party datasets |
| **OpenSearch Service** | Search & log analytics (Elasticsearch-compatible) |
| **MSK** | Managed Apache **Kafka** |
| **Lake Formation** | Build governed **data lakes** on S3 quickly |

## Machine Learning & AI Services

| Service | One-liner |
|---|---|
| **SageMaker** | Build/train/deploy **custom ML models** (for data scientists) |
| **Bedrock** | Access **foundation models / generative AI** via API |
| **Amazon Q** | GenAI assistant (business & developer) |
| **Rekognition** | Image & video analysis (faces, objects, moderation) |
| **Comprehend** | NLP — sentiment, entities from text |
| **Polly** | Text → speech |
| **Transcribe** | Speech → text |
| **Translate** | Language translation |
| **Textract** | Extract text/data **from documents/forms** (beyond OCR) |
| **Lex** | Conversational chatbots (Alexa tech) |
| **Kendra** | Intelligent enterprise **search** |
| **Personalize** | Recommendation engine |
| **Forecast** | Time-series predictions |

## Developer Tools & IaC

| Service | One-liner |
|---|---|
| **CloudFormation** | **Infrastructure as Code** — JSON/YAML templates, repeatable stacks |
| **CDK** | Define infrastructure in real programming languages (compiles to CloudFormation) |
| **CodePipeline** | CI/CD orchestration |
| **CodeBuild** | Managed build/test service |
| **CodeDeploy** | Automated deployments to EC2/Lambda/on-prem |
| **CodeArtifact** | Artifact/package repository |
| **CloudShell** | Browser-based shell with CLI pre-authenticated |
| **X-Ray** | Distributed **tracing** / debugging of microservices |
| **Amplify** | Build & host full-stack web/mobile apps quickly |
| **AppConfig / Systems Manager** | Config & operations management |

## Management & Monitoring

| Service | One-liner |
|---|---|
| **CloudWatch** | **Metrics, alarms, dashboards, logs** — monitoring backbone (billing alarms live here, us-east-1) |
| **CloudTrail** | **API call audit log** — who did what |
| **AWS Config** | Resource configuration tracking & compliance rules — what changed |
| **Systems Manager (SSM)** | Fleet operations: patching, run commands, Session Manager (SSH-less access), Parameter Store |
| **Trusted Advisor** | Automated best-practice checks (cost, performance, security, fault tolerance, limits, sustainability); full checks need Business+ support |
| **Health Dashboard** | Service health: public status + **your account-specific** events |
| **Compute Optimizer** | ML right-sizing recommendations for EC2/EBS/Lambda |
| **License Manager** | Track software licenses |
| **Service Catalog** | Curated list of approved products for org self-service |
| **Managed Grafana / Prometheus** | Managed open-source monitoring |
| **Resource Groups & Tagging** | Organize resources; tags = key/value metadata for cost allocation & automation |

## Migration & Transfer

| Service | One-liner |
|---|---|
| **Migration Hub** | Central tracking of migrations |
| **Application Migration Service (MGN)** | Automated lift-and-shift (rehost) of servers |
| **DMS** | **Database Migration Service** — migrate DBs with minimal downtime (homogeneous or heterogeneous with SCT) |
| **DataSync** | Fast online transfer of file data on-prem ↔ AWS |
| **Transfer Family** | Managed SFTP/FTPS/FTP into S3/EFS |
| **Snow Family** | Offline physical data transfer (TB–PB) |
| **Application Discovery Service** | Inventory on-prem servers for migration planning |

---

# Domain 4 — Billing, Pricing & Support

## Pricing Fundamentals

Three drivers of cost: **Compute, Storage, Data Transfer OUT**.

- **Pay-as-you-go** — no contracts; stop paying when you stop using.
- **Pay less by reserving** (commitment discounts) and **pay less with volume** (tiered pricing).
- **Data transfer IN is free**; transfer **OUT to internet costs**; inter-Region and inter-AZ transfer cost; within same AZ (private IP) free.
- **Free Tier** types: **Always free** (Lambda 1M req/mo, DynamoDB 25 GB), **12-months free** (EC2 t2/t3.micro 750 h/mo, S3 5 GB), **Trials** (short-term).

## EC2 Purchasing Options

| Option | Discount | Use case |
|---|---|---|
| **On-Demand** | 0% (baseline) | Short, unpredictable workloads; no commitment |
| **Reserved Instances (RI)** | Up to ~72% | Steady-state (e.g., DB) — 1 or 3-yr commit; Standard vs Convertible; pay all/partial/no upfront |
| **Savings Plans** | Up to ~72% | Commit to $/hour for 1/3 yrs — flexible across instance families/Regions (Compute SP) |
| **Spot Instances** | Up to ~90% | Fault-tolerant, interruptible work (batch, CI) — AWS can reclaim with 2-min warning |
| **Dedicated Hosts** | Most expensive | Entire physical server — BYOL licenses, compliance |
| **Dedicated Instances** | — | Hardware isolated to your account |
| **Capacity Reservations** | — | Reserve capacity in an AZ (no discount by itself) |

## Cost Management Tools

| Tool | Purpose |
|---|---|
| **AWS Pricing Calculator** | **Estimate cost BEFORE** building an architecture |
| **Billing & Cost Management console** | View invoices, payments |
| **Cost Explorer** | **Visualize & analyze historical** spend; 12-month **forecast**; RI/SP recommendations |
| **AWS Budgets** | Set custom cost/usage budgets with **alerts** (actual or forecasted overrun) |
| **Cost & Usage Report (CUR)** | Most **detailed/granular** raw billing data → S3 |
| **Cost Allocation Tags** | Tag resources to break down cost by team/project |
| **Cost Anomaly Detection** | ML alerts on unusual spend |
| **CloudWatch Billing Alarm** | Alarm when estimated charges exceed threshold |

## AWS Organizations & Consolidated Billing

- **AWS Organizations** — centrally manage multiple accounts: group into **OUs**, apply **SCPs** (permission guardrails), automate account creation.
- **Consolidated billing** — one bill for all accounts; **combined usage** unlocks volume-tier discounts; RI/Savings Plan discounts **shared across accounts**.
- **Control Tower** — sits on Organizations; automated landing zone + preventive/detective guardrails.
- Multi-account benefits: isolation (blast radius), per-team billing, separate environments.

## Support Plans

| Plan | Cost | Key features |
|---|---|---|
| **Basic** | Free | Docs, forums, Health Dashboard, core Trusted Advisor checks, account/billing support only |
| **Developer** | from $29/mo | **Business-hours email** access to Cloud Support Associates; general guidance < 24 h, system impaired < 12 h |
| **Business** | from $100/mo | 24/7 phone/chat; **full Trusted Advisor**; prod impaired < 4 h, **prod down < 1 h**; third-party software support |
| **Enterprise On-Ramp** | from $5,500/mo | Pool of **TAMs**; business-critical down < 30 min |
| **Enterprise** | from $15,000/mo | **Designated TAM**, Concierge billing team, Well-Architected reviews, **business-critical down < 15 min** |

**Other help:** AWS Professional Services, APN Partners, AWS Marketplace (third-party software, billed via AWS), AWS re:Post (community Q&A), AWS Quick Starts / Solutions Library.

---

# Exam Traps & Service One-Liners

Frequently-confused pairs — know the difference cold:

| A vs B | Distinction |
|---|---|
| **CloudTrail vs CloudWatch vs Config** | *Who* made API call vs *metrics/monitoring* vs *what config changed* |
| **Security Group vs NACL** | Instance-level stateful allow-only vs subnet-level stateless allow+deny |
| **RDS Multi-AZ vs Read Replica** | Availability/failover (sync) vs read scaling (async) |
| **CloudFront vs Global Accelerator** | Caches content at edge vs routes traffic over AWS backbone (no caching) |
| **SQS vs SNS** | Pull queue (1 consumer group) vs push pub/sub (fan-out to many) |
| **EBS vs EFS vs Instance Store** | One instance, one AZ vs shared multi-AZ NFS vs ephemeral physical |
| **S3 vs EBS vs EFS** | Object vs block vs file storage |
| **Direct Connect vs Site-to-Site VPN** | Private dedicated line (weeks, consistent) vs encrypted over internet (minutes, variable) |
| **IAM User vs Role** | Long-term credentials for a person vs temporary assumed credentials (prefer roles for services) |
| **KMS vs CloudHSM** | Managed multi-tenant keys vs dedicated single-tenant hardware |
| **Inspector vs GuardDuty vs Macie** | Vulnerability scan (EC2/images) vs threat detection (accounts/workloads) vs PII discovery (S3) |
| **Artifact vs Audit Manager** | Download AWS's compliance reports vs audit *your* usage continuously |
| **Pricing Calculator vs Cost Explorer** | Estimate *future/planned* vs analyze *historical* spend |
| **Budgets vs Cost Anomaly Detection** | Threshold alerts you define vs ML-detected unusual spend |
| **Trusted Advisor vs Health Dashboard** | Best-practice checks vs service outage/maintenance events |
| **Dedicated Host vs Dedicated Instance** | Physical server visibility (BYOL, socket-level licensing) vs just isolated hardware |
| **Elastic Beanstalk vs CloudFormation** | PaaS for apps (uses CFN underneath) vs raw IaC for any resource |
| **OLTP vs OLAP** | RDS/Aurora/DynamoDB vs Redshift |
| **Athena vs Redshift** | Ad-hoc serverless SQL on S3 vs full data warehouse |
| **Snowball vs DataSync** | Offline physical transfer vs online network transfer |
| **Local Zones vs Wavelength vs Outposts** | Metro-edge latency vs 5G-edge vs AWS racks in *your* DC |

---

# Final Exam Tips

1. **Read the qualifier words:** "MOST cost-effective", "LEAST operational overhead", "HIGHLY available" — they select the answer. "Least operational overhead" → serverless/managed. "Most cost-effective + interruptible" → Spot.
2. **Managed/serverless is usually the answer** when the question asks to reduce management burden.
3. **High availability → Multi-AZ. Disaster recovery / lowest latency to global users → Multi-Region / CloudFront.**
4. **Shared Responsibility questions:** data & IAM = always customer; hardware & facilities = always AWS; OS patching depends on service (EC2 = you, RDS = AWS).
5. **Security defaults:** least privilege, roles over keys, MFA on root, encrypt everything.
6. Eliminate obviously wrong options first — usually 2 are clearly off-topic.
7. Unanswered = wrong; **never leave blanks**; flag and return.
8. There is **no penalty for guessing**, and ~15 questions are unscored experiments.
9. Watch time: ~80 seconds per question; don't stall on one.
10. Hands-on the Free Tier at least once — launching an EC2 instance and creating an S3 bucket makes half the exam intuitive.

---

*Last updated: August 2026, aligned to CLF-C02.*
