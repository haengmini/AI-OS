# Loop Flow

## 기본 흐름 / Default Flow

```text
Production Output
→ Dashboard JSON Update
→ Hermes Review
→ Memory Update
→ Slack Report
→ Next Action
```

## Step 1. Read State

Hermes reads Dashboard JSON files.

## Step 2. Review

Hermes checks blocked agents, delayed projects, missing verification, stale memory, repeated manual tasks, resource overuse, missing reports, and unclosed tasks.

## Step 3. Update

Hermes updates Memory, Dashboard JSON, and reports.

## Step 4. Report

Hermes reports to Slack, Dashboard, and Markdown report.

## Step 5. Next Action

Hermes proposes next task, responsible agent, priority, risk, and verification.
