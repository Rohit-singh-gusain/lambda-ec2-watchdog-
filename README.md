# lambda-ec2-watchdog-


> A serverless AWS solution that automatically monitors running EC2 instances and sends email alerts — preventing unexpected cloud bills caused by forgotten instances.

---

## 📌 Problem Statement

While working on AWS, it's easy to forget to stop or terminate EC2 instances after use. These forgotten instances keep running 24/7 and silently accumulate charges on your AWS bill.

**This project solves that problem** by automatically checking for running EC2 instances every day and sending an email alert directly to your Gmail — so you can take action before costs pile up.

---

## 🏗️ Architecture

```
EventBridge (Cron)  →  Lambda (Python/boto3)  →  EC2 API
                                ↓
                           SNS Topic
                                ↓
                         Gmail Inbox ✉️
```

| Service | Role |
|---|---|
| **EventBridge** | Cron scheduler — triggers Lambda on a schedule |
| **Lambda** | Core engine — queries EC2 and publishes alert |
| **EC2 API** | Source — lists all running instances |
| **SNS** | Notification service — delivers email alert |
| **IAM** | Security — grants Lambda least privilege permissions |
| **Terraform** | IaC — provisions entire infrastructure as code |

---

## ✨ Features

- ✅ Fully serverless — no EC2, no server to manage
- ✅ Automated daily alerts for running instances
- ✅ Email shows instance ID, type, name and how long it has been running
- ✅ Sends "All Clear" email when no instances are running
- ✅ Entire infrastructure provisioned via Terraform (IaC)
- ✅ Modular Terraform structure — clean and reusable
- ✅ Zero hardcoded credentials — uses IAM roles and environment variables

---

## 🗂️ Project Structure

```
aws-lambda-ec2-cost-guardian/
│
├── main.tf                        # Root module — calls all child modules
├── variables.tf                   # Input variable declarations
├── output.tf                      # Root outputs
├── providers.tf                   # AWS provider configuration
├── version.tf                     # Terraform version constraints
├── terraform.tfvars.example       # Example variables file (copy to terraform.tfvars)
│
├── python_lambda_code/
│   └── lambda_function.py         # Lambda function (Python/boto3)
│
├── IAM_ROLE/
│   ├── main.tf                    # IAM role and policy
│   ├── output.tf                  # Outputs role ARN
│   └── variable.tf
│
├── lambda_module/
│   ├── main.tf                    # Lambda function resource
│   ├── output.tf                  # Outputs function ARN and name
│   └── variables.tf
│
├── SNS_topic_module/
│   ├── main.tf                    # SNS topic and email subscription
│   ├── output.tf                  # Outputs topic ARN
│   └── variable.tf
│
└── event_bridge/
    ├── main.tf                    # EventBridge rule, target, Lambda permission
    └── variable.tf
```

---

## ⚙️ Prerequisites

Before you begin make sure you have the following installed and configured:

- [Terraform](https://developer.hashicorp.com/terraform/install) >= 1.0
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) configured with your credentials
- Python 3.12 (only to edit the Lambda code locally)
- An AWS account with permissions to create Lambda, SNS, EventBridge, and IAM resources

---

## 🚀 How to Deploy

**Step 1 — Clone the repository**
```bash
git clone https://github.com/Rohit-singh-gusain/lambda-ec2-watchdog-.git
cd lambda-ec2-watchdog-
```

**Step 2 — Create your variables file**
```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` and fill in your values:
```hcl
aws_region  = "ap-south-1"
environment = "dev"
sns_endpoint       = "your-email@gmail.com"
```

**Step 3 — Initialize Terraform**
```bash
terraform init
```

**Step 4 — Preview what will be created**
```bash
terraform plan
```

**Step 5 — Deploy the infrastructure**
```bash
terraform apply
```

Terraform will create **5 resources:**
```
✅ aws_iam_role
✅ aws_iam_role_policy
✅ aws_lambda_function
✅ aws_sns_topic + subscription
✅ aws_cloudwatch_event_rule (EventBridge)
```

**Step 6 — Confirm your email subscription**

After `terraform apply` completes, check your Gmail for:
```
Subject: AWS Notification - Subscription Confirmation
```
Click **"Confirm subscription"** — this is a one time step. Until confirmed, SNS will not deliver alerts.

---

## 🧪 Testing

**Option 1 — Test Lambda manually (instant)**

Go to AWS Console → Lambda → `ec2_inspector` → Test tab → use this payload:
```json
{}
```
Click **Test** — you will receive the alert email within seconds.

**Option 2 — Wait for scheduled trigger**

EventBridge fires automatically at the scheduled cron time. Check CloudWatch logs at:
```
CloudWatch → Log Groups → /aws/lambda/ec2_inspector
```

---

## 📧 Sample Alert Email

```
=======================================================
  EC2 COST GUARDIAN — RUNNING INSTANCES DETECTED
=======================================================
  Region    : ap-south-1
  Checked at: 2025-08-10 09:00 UTC
  Total     : 2 instance(s) running

  Instance #1
  ID          : i-0abc123ef
  Name        : my-test-server
  Type        : t2.micro
  Running for : 14h 32m
  Public IP   : 13.233.xx.xx
=======================================================
  ACTION: Go to EC2 Console → stop unwanted instances
=======================================================
```

---

## 🔐 Security

- **No hardcoded credentials** — Lambda uses IAM execution role
- **Least privilege IAM policy** — only `ec2:DescribeInstances` and `sns:Publish`
- **Environment variables** — SNS ARN passed via Terraform, not hardcoded in Python
- **`.gitignore`** — state files, tfvars, and provider binaries excluded from version control

---

## 🧹 Destroy Infrastructure

To tear down all created resources:
```bash
terraform destroy
```

---

## 🛠️ Tech Stack

![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat&logo=terraform&logoColor=white)
![AWS Lambda](https://img.shields.io/badge/AWS_Lambda-FF9900?style=flat&logo=awslambda&logoColor=white)
![Amazon SNS](https://img.shields.io/badge/Amazon_SNS-FF4F8B?style=flat&logo=amazonaws&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=flat&logo=python&logoColor=white)
![Amazon EC2](https://img.shields.io/badge/Amazon_EC2-FF9900?style=flat&logo=amazonec2&logoColor=white)

---

## 👤 Author

**Rohit Singh Gusain**  
[![GitHub](https://img.shields.io/badge/GitHub-Rohit--singh--gusain-black?style=flat&logo=github)](https://github.com/Rohit-singh-gusain)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).