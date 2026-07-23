#!/usr/bin/env python3
import json, csv, subprocess
from pathlib import Path

ROOT = Path("/Users/tonypham/MEGA/WebApp/content-gen/knowledge-tree")

def build_proj(proj: str, items: list):
    pdir = ROOT / "projects" / proj
    out_dir = pdir / "output"
    work_dir = pdir / ".work"
    out_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    slug = proj.replace("roadmap_sh_", "")
    json_path = pdir / "context" / f"{slug}.json"
    topics_list, subtopics_list = [], []
    if json_path.exists():
        with open(json_path, encoding="utf-8") as f:
            d = json.load(f)
        nodes = d.get("nodes", [])
        topics_list = [n.get("data", {}).get("label") for n in nodes if n.get("type") == "topic" and n.get("data", {}).get("label")]
        subtopics_list = [n.get("data", {}).get("label") for n in nodes if n.get("type") == "subtopic" and n.get("data", {}).get("label")]

    with open(work_dir / "context-audit.md", "w", encoding="utf-8") as f:
        f.write(f"# Context Syllabus Audit for {proj}\n\n## Core Topics\n")
        for t in topics_list:
            f.write(f"- {t}\n")
        f.write("\n## Subtopics & Detailed Skills\n")
        for st in subtopics_list:
            f.write(f"- {st}\n")

    fields = [["COMPUTING_AND_IT", "Computing & Information Technology", "Lĩnh vực công nghệ thông tin và khoa học máy tính."]]
    subjects = [["SOFTWARE_ENGINEERING_SE", "Software Engineering", "Môn học kỹ thuật phần mềm và hệ thống ứng dụng.", "COMPUTING_AND_IT"]]
    categories = [["SOFTWARE_SYSTEMS_ENGINEERING", "Software Systems Engineering", "Phân loại chuyên môn phát triển hệ thống phần mềm.", "SOFTWARE_ENGINEERING_SE"]]

    topic_rows, concept_rows, lo_rows = [], [], []

    for item in items:
        t_code, t_name, c_code, c_name, c_desc, keywords, ulo_code, ulo_name, ulo_desc, cio_code, cio_name, cio_desc, sios = item

        topic_rows.append([t_code, t_name, f"Chủ đề trọng tâm: {t_name}", "SOFTWARE_SYSTEMS_ENGINEERING"])
        concept_rows.append([c_code, c_name, c_desc, t_code, keywords, "", '{"icon": "code"}'])

        lo_rows.append([ulo_code, ulo_name, f"Người học có khả năng {ulo_desc}", "UNIVERSAL", "", c_code])
        lo_rows.append([cio_code, cio_name, f"Người học có khả năng {cio_desc}", "CONCEPTUAL_IMPL", ulo_code, c_code])

        for sio_code, sio_name, sio_desc in sios:
            lo_rows.append([sio_code, sio_name, f"Người học có khả năng {sio_desc}", "SPECIFIC_IMPL", cio_code, c_code])

    def write_tsv(fname, headers, data):
        with open(out_dir / fname, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t")
            w.writerow(headers)
            w.writerows(data)

    write_tsv("fields.tsv", ["code", "name", "description"], fields)
    write_tsv("subjects.tsv", ["code", "name", "description", "field_codes"], subjects)
    write_tsv("categories.tsv", ["code", "name", "description", "subject_codes"], categories)
    write_tsv("topics.tsv", ["code", "name", "description", "category_codes"], topic_rows)
    write_tsv("concepts.tsv", ["code", "name", "description", "topic_codes", "keywords", "cs2023_ka_mapping", "metadata"], concept_rows)
    write_tsv("learning-objectives.tsv", ["code", "name", "description", "lo_type", "parent_lo_code", "concept_codes"], lo_rows)

    val_res = subprocess.run(["python3", ".agents/skills/tree-validator/scripts/validate_tree.py", "--project", proj], capture_output=True, text=True)
    aud_res = subprocess.run(["python3", ".agents/skills/tree-validator/scripts/audit_coverage.py", "--project", proj], capture_output=True, text=True)
    
    val_last = val_res.stdout.strip().splitlines()[-1] if val_res.stdout else "N/A"
    aud_lines = [l for l in aud_res.stdout.splitlines() if "Coverage Score" in l or "Status" in l]
    
    print(f"✅ {proj:<24} | Concepts: {len(concept_rows):<2} | LOs: {len(lo_rows):<3} | Val: {val_last.split('—')[0].strip()} | Audit: {' | '.join(aud_lines)}")

# DEVOPS (22 Concepts, 110 LOs)
devops_items = [
    ("PROGRAMMING_LANGUAGE_DEVOPS", "Programming & Automation Languages", "AUTOMATION_PROGRAMMING_LANGUAGES", "Automation Scripting & System Languages", "Sử dụng Python, Go, Node.js hoặc Bash để viết script tự động hóa hạ tầng.", "Python, Go, Node.js, Bash, PowerShell, automation, scripting", "ULO-AUTOMATION-LANGUAGES", "Master Automation Scripting and System Languages", "viết các script tự động hóa công việc hạ tầng.", "CIO-SYSTEM-SCRIPTING-AUTOMATION", "Automate Operating System Tasks via Scripting", "tự động hóa quản trị hệ thống bằng script.", [
        ("SIO-DEVOPS-PYTHON-AUTOMATION-SCRIPT", "Write System Automation Scripts in Python", "viết script tự động hóa hệ thống bằng Python."),
        ("SIO-DEVOPS-BASH-SHELL-AUTOMATION", "Automate Server Administration via Bash Shell Scripts", "viết kịch bản tự động hóa quản trị máy chủ bằng Bash Shell."),
        ("SIO-DEVOPS-GO-HIGH-PERF-CLI", "Build High-Performance Infrastructure CLI Tools in Go", "xây dựng công cụ CLI hạ tầng siêu tốc bằng ngôn ngữ Go.")
    ]),
    ("OPERATING_SYSTEM_ADMINISTRATION", "Operating System Concepts & Administration", "OPERATING_SYSTEM_ADMINISTRATION_CONCEPT", "OS Kernel & System Administration Engine", "Quản trị hệ điều hành Linux (Ubuntu/Debian, CentOS/RHEL), POSIX, systemd và tài nguyên OS.", "Linux, Ubuntu, Debian, CentOS, RHEL, POSIX, systemd, kernel, OS Administration", "ULO-OS-ADMINISTRATION", "Master OS Kernel and System Administration Engines", "quản trị hệ điều hành Linux và quản lý dịch vụ systemd.", "CIO-LINUX-KERNEL-PROCESS-SUPERVISION", "Supervise Kernel Processes and System Services", "quản lý các tiến trình và dịch vụ hệ thống Linux.", [
        ("SIO-DEVOPS-LINUX-UBUNTU-CENTOS-ADMIN", "Administer Linux Servers on Ubuntu and CentOS", "quản trị máy chủ Linux trên các bản phân phối Ubuntu và CentOS."),
        ("SIO-DEVOPS-SYSTEMD-SERVICE-DAEMON", "Configure Systemd Daemon Services", "tạo file cấu hình systemd service tự động khởi động dịch vụ."),
        ("SIO-DEVOPS-POSIX-SHELL-STANDARDS", "Enforce POSIX Compliance in Shell Scripts", "viết shell script tuân thủ quy chuẩn POSIX.")
    ]),
    ("NETWORKING_PROTOCOLS_SECURITY", "Networking Protocols, Security & DNS", "NETWORKING_PROTOCOLS_SECURITY_CONCEPT", "Network Layer Protocols & Security Controls", "Các giao thức mạng TCP/IP, UDP, HTTP/HTTPS, DNS resolution, TLS/SSL và Firewalls.", "TCP/IP, UDP, HTTP, HTTPS, DNS, TLS, SSL, SSH, Firewall, iptables, ufw", "ULO-NETWORKING-SECURITY", "Master Network Layer Protocols and Security Controls", "làm chủ các giao thức mạng và mô hình bảo mật hạ tầng.", "CIO-NETWORK-TRAFFIC-FIREWALLING", "Filter Network Traffic and Configure SSL/TLS Security", "cấu hình tường lửa và mã hóa truyền tải qua SSL/TLS.", [
        ("SIO-DEVOPS-TCPIP-UDP-HTTP-NETWORKS", "Analyze Network Traffic over TCP/IP, UDP and HTTP", "phân tích luồng dữ liệu mạng qua TCP/IP, UDP và HTTP/HTTPS."),
        ("SIO-DEVOPS-DNS-RECORD-RESOLUTION", "Configure DNS Domain Records (A, CNAME, MX, TXT)", "cấu hình bản ghi tên miền DNS và kiểm tra phân giải IP."),
        ("SIO-DEVOPS-UFW-IPTABLES-FIREWALL", "Secure Host Traffic via UFW and iptables Firewalls", "thiết lập tường lửa lọc lưu lượng mạng bằng UFW và iptables.")
    ]),
    ("INFRASTRUCTURE_PROVISIONING_TERRAFORM", "Infrastructure as Code (Terraform/OpenTofu)", "IAC_INFRASTRUCTURE_PROVISIONING", "Declarative Infrastructure & State Provisioning", "Khởi tạo hạ tầng bằng mã Infrastructure as Code (IaC) với Terraform hoặc OpenTofu.", "Terraform, OpenTofu, IaC, HCL, provider, state file, plan, apply, modules", "ULO-TERRAFORM-IAC", "Master Declarative Infrastructure and State Provisioning", "tự động hóa khởi tạo hạ tầng đám mây bằng Terraform.", "CIO-STATE-PLAN-APPLY-WORKFLOW", "Manage Terraform State and Provision Resources", "quản lý tệp Terraform state và thực thi plan/apply.", [
        ("SIO-DEVOPS-TERRAFORM-HCL-DECLARATION", "Declare Cloud Resources in Terraform HCL", "khai báo tài nguyên máy chủ bằng ngôn ngữ HCL trong Terraform."),
        ("SIO-DEVOPS-TERRAFORM-REMOTE-STATE", "Manage Remote State Lock via S3 and DynamoDB", "lưu trữ tệp Terraform remote state an toàn có cơ chế khóa khóa lock."),
        ("SIO-DEVOPS-TERRAFORM-MODULES-REUSE", "Build Reusable Infrastructure Modules", "đóng gói các cụm tài nguyên hạ tầng thành Terraform Modules.")
    ]),
    ("CONFIGURATION_MANAGEMENT_ANSIBLE", "Configuration Management (Ansible)", "CONFIGURATION_MANAGEMENT_ANSIBLE_CONCEPT", "Agentless Configuration & Idempotent Automation", "Quản lý cấu hình tự động với Ansible Playbooks, Roles, Inventory và Idempotency.", "Ansible, Playbook, Inventory, Roles, YAML, agentless, SSH, Idempotency", "ULO-ANSIBLE-CONFIG-MANAGEMENT", "Master Agentless Configuration and Idempotent Automation", "quản lý cấu hình tự động hóa hàng loạt máy chủ bằng Ansible.", "CIO-PLAYBOOK-AUTOMATION-ROLES", "Execute Idempotent Ansible Playbooks across Inventories", "viết Ansible Playbooks cài đặt phần mềm tự động.", [
        ("SIO-DEVOPS-ANSIBLE-INVENTORY-SSH", "Define Server Inventories and SSH Connections", "khai báo danh sách máy chủ trong Ansible Inventory."),
        ("SIO-DEVOPS-ANSIBLE-PLAYBOOK-TASKS", "Write Idempotent Ansible Playbooks", "viết các kịch bản Ansible Playbook cài đặt phần mềm tự động."),
        ("SIO-DEVOPS-ANSIBLE-ROLES-REUSABLE", "Structure Reusable Configuration Roles", "tổ chức các quy trình cấu hình thành Ansible Roles dùng chung.")
    ]),
    ("CI_CD_PIPELINE_ORCHESTRATION", "Continuous Integration & Continuous Delivery (CI/CD)", "CONTINUOUS_INTEGRATION_DELIVERY", "Automated Build Pipelines & Continuous Delivery", "Tự động hóa tích hợp và triển khai liên tục CI/CD bằng GitHub Actions, GitLab CI, Jenkins.", "CI/CD, GitHub Actions, GitLab CI, Jenkins, pipelines, build, test, deploy, artifacts", "ULO-CICD-PIPELINE-ORCHESTRATION", "Master Automated Build Pipelines and Continuous Delivery", "xây dựng đường ống tích hợp và triển khai tự động CI/CD.", "CIO-PIPELINE-BUILD-TEST-DEPLOY", "Orchestrate Build, Test and Deployment Stages", "kết nối các giai đoạn build, test và deploy tự động.", [
        ("SIO-DEVOPS-GITHUB-ACTIONS-WORKFLOWS", "Build CI/CD Pipelines in GitHub Actions Workflows", "viết tệp workflow tự động hóa kiểm thử và deploy bằng GitHub Actions."),
        ("SIO-DEVOPS-GITLAB-CI-YAML", "Configure Multi-Stage Pipelines in .gitlab-ci.yml", "cấu hình đường ống CI/CD đa giai đoạn trong GitLab CI."),
        ("SIO-DEVOPS-JENKINS-PIPELINE-GROOVY", "Orchestrate Enterprise Pipelines via Jenkinsfiles", "xây dựng đường ống CI/CD doanh nghiệp bằng Jenkinsfile Groovy script.")
    ]),
    ("CONTAINERIZATION_ENGINE_DOCKER", "Containerization Runtimes & Image Building", "CONTAINER_RUNTIME_PACKAGING", "Container Packaging & Runtime Isolation Engine", "Đóng gói ứng dụng container bằng Docker, Containerd, Dockerfiles và Multi-Stage Builds.", "Docker, Containerd, Dockerfile, Containerization, OCI, multi-stage", "ULO-CONTAINERIZATION-DOCKER", "Master Container Packaging and Runtime Isolation Engines", "đóng gói và cách ly ứng dụng trong các container.", "CIO-CONTAINER-IMAGE-PACKAGING", "Build and Package Production Container Images", "tạo hình ảnh container sản xuất tối ưu dung lượng.", [
        ("SIO-DEVOPS-DOCKER-MULTI-STAGE-BUILD", "Build Production Images with Multi-Stage Dockerfiles", "đóng gói ảnh ứng dụng bằng kỹ thuật Multi-Stage Dockerfile."),
        ("SIO-DEVOPS-CONTAINERD-RUNTIME-RUN", "Manage Low-Level Container Runtimes via containerd", "quản lý trình thực thi container cấp thấp bằng containerd."),
        ("SIO-DEVOPS-DOCKER-COMPOSE-SERVICES", "Orchestrate Local Microservices with Docker Compose", "chạy cụm dịch vụ phát triển local bằng Docker Compose.")
    ]),
    ("CONTAINER_ORCHESTRATION_KUBERNETES", "Container Orchestration & Cluster Management", "CLUSTER_ORCHESTRATION_KUBERNETES", "Cluster Container Orchestration & Resource Management", "Quản lý và điều phối cụm máy chủ container bằng Kubernetes (k8s), Pods, Deployments, Services, Ingress.", "Kubernetes, k8s, Pods, Deployments, Services, Ingress, kubectl, Helm, HPA", "ULO-KUBERNETES-CLUSTER", "Master Cluster Container Orchestration and Resource Management", "vận hành cụm container máy chủ bằng Kubernetes.", "CIO-KUBERNETES-MANIFEST-DEPLOYMENT", "Deploy Declarative Kubernetes Resource Manifests", "triển khai các tài nguyên ứng dụng lên cụm Kubernetes.", [
        ("SIO-DEVOPS-KUBERNETES-DEPLOYMENT-YAML", "Declare Kubernetes Deployments and Services", "viết tệp YAML khai báo Deployment và Service trong Kubernetes."),
        ("SIO-DEVOPS-KUBERNETES-INGRESS-CONTROLLER", "Expose HTTP Services with Ingress Controllers", "phân tuyến đường dẫn domain vào cụm bằng Ingress Controller."),
        ("SIO-DEVOPS-HELM-CHARTS-DEPLOY", "Package and Deploy Kubernetes Applications via Helm", "quản lý phiên bản ứng dụng Kubernetes bằng Helm Charts.")
    ]),
    ("LOG_AGGREGATION_OBSERVABILITY", "Log Aggregation & Centralized Observability", "CENTRALIZED_LOG_OBSERVABILITY", "Log Collection Pipelines & Centralized Search Engines", "Thu thập và phân tích nhật ký ghi log bằng ELK Stack (Elasticsearch, Logstash, Kibana) hoặc Grafana Loki.", "ELK Stack, Elasticsearch, Logstash, Kibana, Grafana Loki, Fluentd, Promtail, log aggregation", "ULO-LOG-AGGREGATION-OBSERVABILITY", "Master Log Collection Pipelines and Centralized Search Engines", "thu thập và phân tích log tập trung toàn hệ thống.", "CIO-LOG-PIPELINE-INDEXING-SEARCH", "Index and Search Log Data across Distributed Nodes", "lưu trữ chỉ mục và truy vấn log tập trung.", [
        ("SIO-DEVOPS-ELK-STACK-LOGGING", "Collect and Search Logs via ELK Stack", "thu thập và tìm kiếm nhật ký log bằng Elasticsearch, Logstash, Kibana."),
        ("SIO-DEVOPS-GRAFANA-LOKI-PROMTAIL", "Stream Logs with Grafana Loki and Promtail", "đẩy và truy vấn log siêu nhẹ bằng Grafana Loki và Promtail."),
        ("SIO-DEVOPS-FLUENTD-LOG-COLLECTOR", "Forward Container Logs via Fluentd", "điều hướng luồng log container qua Fluentd log collector.")
    ]),
    ("METRICS_MONITORING_ALERTING", "Metrics Monitoring & Alert Management", "METRICS_MONITORING_ALERTING_CONCEPT", "Time-Series Metrics Collection & Alerting Engines", "Giám sát chỉ số tài nguyên hệ thống bằng Prometheus và hiển thị bảng điều khiển Grafana.", "Prometheus, Grafana, PromQL, Alertmanager, time-series metrics, dashboards", "ULO-METRICS-MONITORING", "Master Time-Series Metrics Collection and Alerting Engines", "giám sát chỉ số hiệu năng hệ thống theo thời gian thực.", "CIO-TIME-SERIES-PROMETHEUS-GRAFANA", "Collect Metrics and Build Grafana Dashboards", "thu thập chỉ số bằng Prometheus và dựng dashboard Grafana.", [
        ("SIO-DEVOPS-PROMETHEUS-METRICS-COLLECT", "Scrape Application Metrics with Prometheus", "cấu hình Prometheus thu thập các chỉ số tài nguyên time-series."),
        ("SIO-DEVOPS-GRAFANA-DASHBOARDS-VISUALIZE", "Visualize System Health on Grafana Dashboards", "dựng bảng điều khiển trực quan hóa thông số hệ thống trên Grafana."),
        ("SIO-DEVOPS-ALERTMANAGER-NOTIFICATIONS", "Configure Alert Rules in Prometheus Alertmanager", "gửi thông báo cảnh báo sự cố qua Prometheus Alertmanager.")
    ]),
    ("DISTRIBUTED_TRACING_TELEMETRY", "Distributed Tracing & OpenTelemetry", "DISTRIBUTED_TRACING_TELEMETRY_CONCEPT", "Distributed Request Tracing & OpenTelemetry Telemetry", "Truy vết giao dịch phân tán giữa các microservices bằng OpenTelemetry, Jaeger hoặc Zipkin.", "OpenTelemetry, Jaeger, Zipkin, distributed tracing, trace ID, span, APM", "ULO-DISTRIBUTED-TRACING", "Master Distributed Request Tracing and OpenTelemetry Telemetry", "truy vết luồng gọi API qua các dịch vụ microservices.", "CIO-TRACE-SPAN-CONTEXT-PROPAGATION", "Propagate Trace Context and Analyze Service Latency", "truy vết độ trễ giữa các dịch vụ bằng Trace ID và Span ID.", [
        ("SIO-DEVOPS-OPENTELEMETRY-INSTRUMENTATION", "Instrument Microservices with OpenTelemetry SDKs", "tích hợp SDK OpenTelemetry đo đạc độ trễ request trong mã nguồn."),
        ("SIO-DEVOPS-JAEGER-TRACE-VISUALIZATION", "Visualize Request Spans in Jaeger UI", "phân tích vết gọi API rẽ nhánh trên giao diện Jaeger UI."),
        ("SIO-DEVOPS-APM-LATENCY-PROFILING", "Profile Bottlenecks with APM Telemetry Agents", "phát hiện điểm nghẽn hiệu năng ứng dụng bằng công cụ APM.")
    ]),
    ("CLOUD_INFRASTRUCTURE_AWS", "Cloud Infrastructure & Services (AWS)", "CLOUD_INFRASTRUCTURE_AWS_CONCEPT", "Cloud Virtualization & Managed Cloud Infrastructure", "Vận hành điện toán đám mây Amazon Web Services (AWS): EC2, S3, RDS, VPC, IAM, EKS.", "AWS, EC2, S3, RDS, VPC, IAM, EKS, Cloud Architecture, Serverless", "ULO-CLOUD-AWS", "Master Cloud Virtualization and Managed Cloud Infrastructure", "làm chủ vận hành hạ tầng điện toán đám mây AWS.", "CIO-VIRTUAL-CLOUD-ARCHITECTURE", "Architect Secure VPC Networks and Managed Services", "thiết kế hạ tầng mạng ảo VPC và dịch vụ điện toán đám mây.", [
        ("SIO-DEVOPS-AWS-EC2-VPC-NETWORKING", "Provision Compute Nodes inside AWS VPC Networks", "khởi tạo máy chủ EC2 nằm trong mạng bảo mật AWS VPC."),
        ("SIO-DEVOPS-AWS-S3-STORAGE-BUCKET", "Store Object Assets in AWS S3 Buckets", "lưu trữ đối tượng tĩnh trên ổ đĩa đám mây AWS S3 Bucket."),
        ("SIO-DEVOPS-AWS-IAM-ROLES-POLICIES", "Manage Access Control via AWS IAM Roles and Policies", "quản lý phân quyền truy cập hạ tầng bằng AWS IAM Roles.")
    ]),
    ("CLOUD_INFRASTRUCTURE_GCP", "Google Cloud Platform Infrastructure (GCP)", "CLOUD_INFRASTRUCTURE_GCP_CONCEPT", "Managed Cloud Computing & Kubernetes Engines (GCP)", "Vận hành hạ tầng Google Cloud Platform (GCP): GCOMPUTE, GCS, GKE, IAM.", "GCP, Compute Engine, GCS, GKE, Cloud Run, IAM, Google Cloud", "ULO-CLOUD-GCP", "Master Managed Cloud Computing and Kubernetes Engines", "quản trị hạ tầng máy chủ trên nền tảng Google Cloud Platform.", "CIO-MANAGED-KUBERNETES-GKE", "Deploy Workloads to Managed Google Kubernetes Engine", "triển khai ứng dụng lên cụm Google Kubernetes Engine (GKE).", [
        ("SIO-DEVOPS-GCP-COMPUTE-ENGINE-VM", "Spin Up Virtual Machines on GCP Compute Engine", "khởi tạo máy chủ ảo VM trên Google Cloud Compute Engine."),
        ("SIO-DEVOPS-GCP-GKE-KUBERNETES-CLUSTER", "Deploy Containers to Google Kubernetes Engine (GKE)", "vận hành cụm k8s bằng dịch vụ Google Kubernetes Engine."),
        ("SIO-DEVOPS-GCP-CLOUD-RUN-SERVERLESS", "Deploy Serverless Containers on GCP Cloud Run", "triển khai ứng dụng container dạng Serverless với GCP Cloud Run.")
    ]),
    ("CLOUD_NATIVE_SERVERLESS_LAMBDA", "Serverless Computing & Cloud Functions", "SERVERLESS_CLOUD_COMPUTING", "Event-Driven Serverless & Cloud Function Execution", "Lập trình ứng dụng hướng sự kiện Serverless không máy chủ: AWS Lambda, Cloud Functions, Serverless Framework.", "Serverless, AWS Lambda, Cloud Functions, Event-Driven, SAM, Serverless Framework", "ULO-SERVERLESS-COMPUTING", "Master Event-Driven Serverless and Cloud Function Execution", "xây dựng ứng dụng không máy chủ Serverless.", "CIO-EVENT-DRIVEN-FUNCTION-TRIGGERS", "Trigger Cloud Functions on S3/HTTP Events", "kích hoạt hàm Lambda khi có sự kiện đẩy file hoặc HTTP request.", [
        ("SIO-DEVOPS-AWS-LAMBDA-FUNCTION-SETUP", "Deploy Event-Driven Functions to AWS Lambda", "viết và triển khai hàm xử lý sự kiện trên AWS Lambda."),
        ("SIO-DEVOPS-SERVERLESS-FRAMEWORK-YAML", "Declare Serverless Services with Serverless Framework", "khai báo ứng dụng Serverless bằng tệp serverless.yml."),
        ("SIO-DEVOPS-API-GATEWAY-LAMBDA-HTTP", "Connect HTTP Triggers via AWS API Gateway", "kết nối các endpoint HTTP từ API Gateway sang AWS Lambda.")
    ]),
    ("SITE_RELIABILITY_ENGINEERING_SRE", "Site Reliability Engineering (SRE) & Service Level Objectives", "SITE_RELIABILITY_ENGINEERING", "Service Reliability Metrics & Error Budget Management", "Phương pháp luận SRE, chỉ số SLI, SLO, SLA, Error Budget và Chaos Engineering.", "SRE, SLI, SLO, SLA, Error Budget, Chaos Engineering, Incident Response, Postmortem", "ULO-SRE-RELIABILITY", "Master Service Reliability Metrics and Error Budget Management", "áp dụng phương pháp luận SRE đảm bảo độ tin cậy hệ thống.", "CIO-RELIABILITY-TARGETS-BUDGETS", "Define Service Level Objectives and Manage Error Budgets", "định nghĩa các chỉ số cam kết chất lượng SLO và ngân sách lỗi Error Budget.", [
        ("SIO-DEVOPS-SRE-SLI-SLO-METRICS", "Define Service Level Indicators (SLI) and Objectives (SLO)", "định nghĩa các chỉ số đo đạc SLI và mục tiêu cam kết SLO."),
        ("SIO-DEVOPS-SRE-ERROR-BUDGET-CALC", "Calculate Error Budgets to Balance Release Velocity", "tính toán ngân sách lỗi Error Budget để cân đối tốc độ ra bản mới."),
        ("SIO-DEVOPS-CHAOS-ENGINEERING-LITMUS", "Simulate Infrastructure Failures via Chaos Engineering", "giả lập sự cố ngẫu nhiên bằng công cụ Chaos Engineering (LitmusChaos).")
    ]),
    ("SERVICE_MESH_ISTIO", "Service Mesh Architecture (Istio)", "SERVICE_MESH_ARCHITECTURE", "Service Mesh Control Planes & Sidecar Proxy Networks", "Quản lý mạng giao tiếp microservices với Service Mesh (Istio, Linkerd), Sidecar Proxy (Envoy) và Traffic Management.", "Service Mesh, Istio, Linkerd, Envoy Proxy, Sidecar, Traffic Splitting, mTLS", "ULO-SERVICE-MESH-ISTIO", "Master Service Mesh Control Planes and Sidecar Proxy Networks", "làm chủ quản lý giao tiếp giữa các microservices qua Service Mesh.", "CIO-SIDECAR-PROXY-TRAFFIC-MANAGEMENT", "Inject Sidecar Proxies and Control Mutual TLS Traffic", "tiêm Envoy Sidecar Proxy và quản lý lưu lượng mã hóa mTLS.", [
        ("SIO-DEVOPS-ISTIO-SIDECAR-INJECTION", "Inject Envoy Sidecar Proxies into Kubernetes Pods", "tự động tiêm Envoy Sidecar Proxy vào các Pods trong Istio."),
        ("SIO-DEVOPS-ISTIO-TRAFFIC-SPLITTING-CANARY", "Configure Canary Traffic Splitting with VirtualServices", "cấu hình chia tỷ lệ lưu lượng mạng Canary deployment bằng VirtualService."),
        ("SIO-DEVOPS-ISTIO-MUTUAL-TLS-ENCRYPT", "Enforce Mutual TLS (mTLS) Encryption across Pods", "kích hoạt mã hóa đường truyền 2 chiều mTLS giữa các microservices.")
    ]),
    ("SECRET_MANAGEMENT_VAULT", "Secrets Management & Vault Security", "SECRETS_MANAGEMENT_VAULT_CONCEPT", "Centralized Secret Vaults & Encryption Engines", "Quản lý mật khẩu, khóa mã hóa và token an toàn bằng HashiCorp Vault, AWS Secrets Manager.", "HashiCorp Vault, Secrets Manager, encryption, dynamic secrets, key rotation", "ULO-SECRETS-MANAGEMENT", "Master Centralized Secret Vaults and Encryption Engines", "quản lý các bí mật hệ thống và token mã hóa tập trung.", "CIO-DYNAMIC-SECRET-ROTATION", "Rotate Database Credentials Dynamically via Vault", "tự động luân chuyển mật khẩu CSDL bằng HashiCorp Vault.", [
        ("SIO-DEVOPS-HASHICORP-VAULT-SECRET-STORE", "Store Encrypted Secrets in HashiCorp Vault", "lưu trữ mật khẩu và khóa mã hóa trong HashiCorp Vault."),
        ("SIO-DEVOPS-VAULT-DYNAMIC-DB-CREDS", "Generate Dynamic Database Credentials on Demand", "sinh tự động mật khẩu CSDL dùng 1 lần bằng Vault Dynamic Secrets."),
        ("SIO-DEVOPS-KUBERNETES-SECRETS-INJECT", "Inject Vault Secrets into Kubernetes Pod Environments", "tiêm các mật khẩu từ Vault vào môi trường Pods trong Kubernetes.")
    ]),
    ("GITOPS_ARGO_CD", "GitOps & Continuous Deployment (ArgoCD)", "GITOPS_CONTINUOUS_DEPLOYMENT", "GitOps Declarative State & Automated Synchronization Engines", "Quản lý hạ tầng chuẩn GitOps, tự động đồng bộ trạng thái cluster từ Git bằng ArgoCD hoặc Flux.", "GitOps, ArgoCD, Flux, Git repository, declarative state, sync, drift detection", "ULO-GITOPS-ARGOCD", "Master GitOps Declarative State and Automated Synchronization Engines", "triển khai phần mềm chuẩn GitOps với ArgoCD.", "CIO-DECLARATION-STATE-SYNCHRONIZATION", "Synchronize Kubernetes Clusters with Git Source Declarations", "tự động đồng bộ trạng thái cụm Kubernetes với tệp khai báo trên Git.", [
        ("SIO-DEVOPS-ARGOCD-APPLICATION-MANIFEST", "Declare ArgoCD Applications for Git-to-Cluster Sync", "khai báo đối tượng ArgoCD Application để đồng bộ tệp YAML trên Git."),
        ("SIO-DEVOPS-ARGOCD-DRIFT-DETECTION", "Detect and Remediate Out-of-Sync Infrastructure Drift", "tự động phát hiện và sửa đổi sự lệch lệch trạng thái (drift detection)."),
        ("SIO-DEVOPS-FLUX-GITOPS-OPERATOR", "Automate Continuous Deployments with Flux CD Operator", "tự động hóa triển khai hạ tầng chuẩn GitOps bằng Flux CD Operator.")
    ]),
    ("ARTIFACT_REPOSITORY_MANAGEMENT", "Artifact Repositories & Package Registries", "ARTIFACT_PACKAGE_REGISTRIES", "Artifact Storage Repositories & Binary Package Registries", "Lưu trữ và phân phối gói phần mềm binary bằng Sonatype Nexus, JFrog Artifactory.", "Nexus, Artifactory, npm registry, Maven, PyPI, Docker registry, artifact management", "ULO-ARTIFACT-REPOSITORIES", "Master Artifact Storage Repositories and Binary Package Registries", "quản lý kho lưu trữ gói phần mềm thành phẩm tập trung.", "CIO-PACKAGE-BINARY-DISTRIBUTION", "Distribute Software Packages across Enterprise Registries", "phát hành và lưu trữ các bản đóng gói binary trong doanh nghiệp.", [
        ("SIO-DEVOPS-NEXUS-ARTIFACTORY-SETUP", "Configure Enterprise Registries in Nexus / Artifactory", "cấu hình kho lưu trữ gói thành phẩm Nexus / Artifactory."),
        ("SIO-DEVOPS-PUBLISH-PRIVATE-NPM-MAVEN", "Publish Private Packages to Internal Package Registries", "đẩy các gói thư viện private (npm, Maven, PyPI) vào kho lưu trữ nội bộ."),
        ("SIO-DEVOPS-ARTIFACT-CLEANUP-POLICY", "Enforce Storage Cleanup Policies on Old Builds", "tự động dọn dẹp các bản đóng gói cũ quá hạn sử dụng.")
    ]),
    ("BACKUP_DISASTER_RECOVERY", "Backup, Disaster Recovery & High Availability", "BACKUP_DISASTER_RECOVERY_CONCEPT", "Disaster Recovery Systems & High Availability Replication", "Chiến lược sao lưu dự phòng (Backup), khôi phục thảm họa (Disaster Recovery) và sẵn sàng cao (High Availability).", "Backup, RPO, RTO, Disaster Recovery, High Availability, Velero, failover", "ULO-DISASTER-RECOVERY", "Master Disaster Recovery Systems and High Availability Replication", "đảm bảo an toàn dữ liệu và khôi phục hệ thống khi gặp thảm họa.", "CIO-RPO-RTO-FAILOVER-STRATEGY", "Implement Automated Database Backups and Failover Verification", "cấu hình sao lưu CSDL tự động và đo đạc chỉ số RPO/RTO.", [
        ("SIO-DEVOPS-VELERO-KUBERNETES-BACKUP", "Backup Kubernetes Clusters with Velero", "sao lưu toàn bộ trạng thái cụm Kubernetes bằng công cụ Velero."),
        ("SIO-DEVOPS-DATABASE-SNAPSHOT-SCHEDULE", "Schedule Automated Database Snapshots and Point-In-Time Recovery", "lên lịch sao lưu CSDL tự động và phục hồi về thời điểm cụ thể (PITR)."),
        ("SIO-DEVOPS-DISASTER-RECOVERY-FAILOVER", "Execute Multi-Region Disaster Recovery Failover Drills", "thực tập kịch bản chuyển đổi vùng khẩn cấp (Disaster Recovery Failover).")
    ]),
    ("COST_OPTIMIZATION_FINOPS", "Cloud Cost Optimization & FinOps", "CLOUD_COST_OPTIMIZATION_FINOPS", "Cloud FinOps Management & Cost Allocation Engines", "Tối ưu hóa chi phí điện toán đám mây FinOps, Spot Instances, Savings Plans và Kubecost.", "FinOps, AWS Cost Explorer, Kubecost, Spot Instances, Savings Plans, Reserved Instances", "ULO-CLOUD-FINOPS", "Master Cloud FinOps Management and Cost Allocation Engines", "tối ưu hóa chi phí vận hành đám mây cho doanh nghiệp.", "CIO-COST-ALLOCATION-REDUCTION", "Allocate Cloud Costs and Reduce Unused Compute Resources", "phân tích chỉ số tiêu thụ và cắt giảm tài nguyên lãng phí.", [
        ("SIO-DEVOPS-AWS-SPOT-INSTANCES-COST", "Leverage AWS Spot Instances for Non-Critical Workloads", "sử dụng máy chủ AWS Spot Instances tiết kiệm tới 90% chi phí."),
        ("SIO-DEVOPS-KUBECOST-POD-COST-ALLOCATION", "Track Container Costs with Kubecost", "đo đạc chi phí tiêu thụ tài nguyên của từng Pod bằng Kubecost."),
        ("SIO-DEVOPS-SAVINGS-PLANS-RESERVED", "Purchase Savings Plans and Reserved Instances", "tối ưu hóa ngân sách dài hạn bằng giải pháp Savings Plans.")
    ]),
    ("HIGH_PERFORMANCE_LOAD_BALANCING", "Reverse Proxies & High-Performance Load Balancing", "REVERSE_PROXY_LOAD_BALANCING", "High-Performance Load Balancing & Reverse Proxy Engines", "Phân tải hệ thống nâng cao bằng Nginx, HAProxy, Traefik, ALB/NLB.", "Nginx, HAProxy, Traefik, Load Balancing, Reverse Proxy, Layer 4, Layer 7, ALB", "ULO-LOAD-BALANCING", "Master High-Performance Load Balancing and Reverse Proxy Engines", "làm chủ điều hướng phân tải hệ thống tốc độ cao.", "CIO-LAYER4-LAYER7-LOAD-BALANCING", "Balance Network Traffic at Layer 4 and Layer 7", "phân tải lưu lượng mạng ở tầng giao vận L4 và tầng ứng dụng L7.", [
        ("SIO-DEVOPS-NGINX-REVERSE-PROXY-CONFIG", "Configure Nginx as High-Performance Reverse Proxy", "cấu hình Nginx làm điều hướng Reverse Proxy và cache tĩnh."),
        ("SIO-DEVOPS-HAPROXY-LAYER4-BALANCER", "Balance TCP Traffic via HAProxy Layer 4 Load Balancers", "phân tải lưu lượng TCP cấp thấp bằng HAProxy."),
        ("SIO-DEVOPS-TRAEFIK-DYNAMIC-ROUTER", "Route Dynamic Microservice Traffic with Traefik", "tự động điều hướng lưu lượng container bằng Traefik Proxy.")
    ])
]

def main():
    print("🚀 Rebuilding roadmap_sh_devops with 22 Neutral Concepts & 110 LOs...")
    build_proj("roadmap_sh_devops", devops_items)

if __name__ == "__main__":
    main()
