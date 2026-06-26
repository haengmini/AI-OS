---
type: raw
title: Agent Backend / Second-Brain References
tags: [references, raw, backend, second-brain]
created: 2026-06-22
source: "web (2026-06-22)"
status: raw
---

# Agent Backend & Second-Brain — 레퍼런스 (raw, 미증류)

> 수집일 2026-06-22. 증류되면 concepts/comparisons로 승격(`[[memory-promotion-filter]]`).

## 1. Postgres 작업 큐 (SKIP LOCKED)
- PostgreSQL 공식 FOR UPDATE/SKIP LOCKED: https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE
- Neon, Queue with SKIP LOCKED: https://neon.com/guides/queue-system
- Supabase best practice: https://supaexplorer.com/best-practices/supabase-postgres/lock-skip-locked/

## 2. 즉시 깨우기 (LISTEN/NOTIFY)
- PostgreSQL 공식 NOTIFY: https://www.postgresql.org/docs/current/sql-notify.html
- 심층(tapoueh): https://tapoueh.org/blog/2018/07/postgresql-listen-notify/
- 주의: NOTIFY 단독은 큐 불가 → SKIP LOCKED 테이블과 병행.

## 3. 벡터 메모리 (pgvector)
- pgvector GitHub: https://github.com/pgvector/pgvector
- Supabase pgvector: https://supabase.com/docs/guides/database/extensions/pgvector
- Tiger Data 튜토리얼: https://www.tigerdata.com/blog/postgresql-as-a-vector-database-using-pgvector

## 4. 내구성 오케스트레이션 (Temporal)
- Temporal for AI: https://temporal.io/solutions/ai
- Temporal + AI agents: https://dev.to/akki907/temporal-workflow-orchestration-building-reliable-agentic-ai-systems-3bpm

## 5. 메시지 브로커 비교
- Kafka·RabbitMQ·NATS·Redis Streams (2026): https://dev.to/mahdi0shamlou/message-brokers-comparison-2026-kafka-rabbitmq-nats-redis-streams-which-one-should-you-3ea8

## 6. 멀티에이전트 프레임워크
- DataCamp CrewAI vs LangGraph vs AutoGen: https://www.datacamp.com/tutorial/crewai-vs-langgraph-vs-autogen
- Turing 2026 top frameworks: https://www.turing.com/resources/ai-agent-frameworks
- 현황: AutoGen 유지보수 모드(→ MS Agent Framework), LangGraph 모멘텀.

## 7. 에이전트 메모리 설계
- arXiv survey, Memory for Autonomous LLM Agents: https://arxiv.org/pdf/2603.07670
- Long-term memory architectures: https://www.gocodeo.com/post/memory-architectures-for-long-term-ai-agent-behavior
- Redis 단기/장기 메모리: https://redis.io/blog/build-smarter-ai-agents-manage-short-term-and-long-term-memory-with-redis/

## 관련
- [[postgres-vs-drive-as-agent-bus]] · [[index]]
