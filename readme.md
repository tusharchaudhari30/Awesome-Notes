# Awesome Notes

A comprehensive collection of software engineering notes, interview preparation materials, and technical cheat sheets for backend development, focusing on Java ecosystem, databases, and modern development tools.

[![GitHub stars](https://img.shields.io/github/stars/tusharchaudhari30/Awesome-Notes?style=social)](https://github.com/tusharchaudhari30/Awesome-Notes)
[![GitHub forks](https://img.shields.io/github/forks/tusharchaudhari30/Awesome-Notes?style=social)](https://github.com/tusharchaudhari30/Awesome-Notes)

---

## 📚 Table of Contents

- [Quickbites Cheat Sheets](#-quickbites-cheat-sheets)
- [Java](#-java)
- [Kafka](#-kafka)
- [Database](#-database)
  - [SQL](#sql)
  - [Redis](#redis)
- [How to Use](#-how-to-use)
- [Contributing](#-contributing)
- [About](#-about)

---

## ⚡ Quickbites Cheat Sheets

Concise, interview-focused cheat sheets for rapid revision. Perfect for last-minute preparation and quick reference.

### Backend & Java Stack

- **[Spring Boot Core](./Quickbites/springbootcore.md)** - IoC, DI, Annotations, Configuration, Profiles
- **[Spring Data JPA](./Quickbites/SpringJPA.md)** - Repository patterns, Query methods, Relationships
- **[Spring REST](./Quickbites/SpringRest.md)** - REST APIs, Exception handling, Validation
- **[Hibernate](./Quickbites/Hibernate.md)** - ORM fundamentals, Entity lifecycle, Caching strategies
- **[Spring Boot Unit Testing](./Quickbites/Spring-boot-unit-test.md)** - JUnit, Mockito, Integration testing

### Database

- **[SQL Cheat Sheet](./Quickbites/SQL.md)** - Queries, Joins, Aggregations, Window functions
- **[Oracle](./Quickbites/Oracle.md)** - Oracle-specific features

### Frontend

- **[React JSX](./Quickbites/reactjsx.md)** - Components, Hooks, State management
- **[React + TypeScript](./Quickbites/reactts.md)** - Type-safe React development
- **[TypeScript](./Quickbites/Typescript.md)** - Types, Interfaces, Generics, Advanced patterns

### DevOps & Tools

- **[Docker](./Quickbites/Docker.md)** - Containers, Images, Docker Compose, Best practices
- **[Git](./Quickbites/git.md)** - Commands, Workflows, Branching strategies

### Design & Architecture

- **[Low-Level Design (LLD)](./Quickbites/LLD.md)** - Design patterns, SOLID principles, Code examples
- **[High-Level Design (HLD)](./Quickbites/HLD.md)** - System design concepts

---

## ☕ Java

### Java Definitive Guide

Comprehensive Java fundamentals and advanced concepts:

- **[Fundamental Programming Structure](./Java/Java%20Definative/1.%20Fundamental%20Programming%20Structure.md)**

  - Data types, Variables, Operators
  - Control flow, Loops, Arrays
  - Methods and Parameter passing

- **[Java Keywords](./Java/Java%20Definative/Java%20Keywords.md)**
  - Complete keyword reference
  - Usage examples and best practices

### Core Java Brain Map

- **[Brain Map](./Java/Brain%20Map.md)** - Visual learning guide covering Java ecosystem

---

## 📨 Kafka

End-to-end Apache Kafka notes covering fundamentals to advanced topics:

### Core Concepts

- **[Kafka Fundamentals](./kafka/Kafka%20Fundamentals.md)** - Introduction to Kafka, Core concepts
- **[Kafka Producers](./kafka/Kafka%20Producers.md)** - Producers and message sending
- **[Kafka Consumers](./kafka/Kafka%20Consumers.md)** - Consumers and consumer groups
- **[Kafka Architecture](./kafka/Kafka%20Architecture.md)** - Kafka internals
- **[Kafka Reliability](./kafka/Kafka%20Reliability.md)** - Replication and reliability

### Advanced Topics

- **[Data Pipelines](./kafka/Data%20Pipelines.md)** - Building data pipelines
- **[Cross-Cluster Replication](./kafka/Cross-Cluster%20Replication.md)** - Cross-cluster data mirroring
- **[Kafka Streams](./kafka/Kafka%20Streams.md)** - Stream processing
- **[Kafka Security](./kafka/Kafka%20Security.md)** - Security configurations
- **[Kafka Monitoring](./kafka/Kafka%20Monitoring.md)** - Monitoring and management

### Spring Boot Integration

- **[Dead Letter Queue with Spring](./kafka/DLQSpring.md)** - Error handling, Retry mechanisms, DLQ patterns

### Quick Reference

- **[Index](./kafka/Index.md)** - Complete Kafka topics index

---

## 🗄️ Database

### SQL

Comprehensive SQL notes from basics to advanced database concepts:

#### Fundamentals

1. **[Relational Model & Architecture](./Database/SQL/1.%20Relational%20Model%20%26%20Architecture.md)**
2. **[SQL DDL (Data Definition Language)](<./Database/SQL/2.%20SQL%20Data%20Definition%20Language%20(%20DDL%20).md>)**
3. **[Keys & Integrity Constraints](./Database/SQL/3.%20Keys%20%26%20Integrity%20Constraints.md)**
4. **[SQL DML (Data Manipulation Language)](<./Database/SQL/4.%20SQL%20Data%20Monipulation%20Language%20(DML).md>)**

#### Query Techniques

5. **[Joins and Set Operations](./Database/SQL/5.%20Joins%20and%20Set%20Operations.md)**
6. **[Aggregations & Grouping](./Database/SQL/6.%20Aggregations%20%26%20Grouping.md)**
7. **[Subqueries & Common Table Expressions (CTEs)](<./Database/SQL/7.%20Subqueries%20%26%20Common%20Table%20Expressions%20(CTEs).md>)**
8. **[Window Functions & Analytics](./Database/SQL/8.%20Windo%20Functions%20%26%20Analytics.md)**

#### Advanced Concepts

9. **[Normalization & Schema Design](./Database/SQL/9.%20Normalization%20%26%20Schema%20design.md)**
10. **[Transactions & ACID Properties](./Database/SQL/10.%20Transactions%20%26%20ACID%20Properties.md)**
11. **[Concurrency Control & Locking](./Database/SQL/11.%20Concurrency%20Control%20%26%20Locking.md)**
12. **[Indexing Strategies & Performance Tuning](./Database/SQL/12.%20Indexing%20Strategies%20%26%20Performance%20Tuning.md)**
13. **[Query Execution & Optimization](./Database/SQL/13.%20Query%20Execution%20%26%20Optimization.md)**

#### Database Objects

14. **[Views, Materialized Views & Stored Procedures](./Database/SQL/14.%20Views%20Materialized%20Views%20Stored%20procedures.md)**
15. **[Triggers & User-defined Functions](./Database/SQL/15.%20Triggers%20%26%20User-defined%20Functions.md)**

**[SQL Notes Index](./Database/SQL/Readme.md)**

---

### Redis

Complete Redis and Spring Data Redis integration guide:

#### Core Redis

1. **[Redis Fundamentals and Core Concepts](./Database/Redis/1.%20Redis%20Fundamentals%20and%20Core%20Concepts.md)**
   - Data structures, Commands, Use cases
2. **[Redis Data Persistence and High Availability](./Database/Redis/2.%20Redis%20Data%20persistence%20and%20High%20Availability.md)**
   - RDB, AOF, Replication, Sentinel
3. **[Advanced Redis Concepts](./Database/Redis/3.%20Advanced%20Redis%20Concepts.md)**
   - Transactions, Pipelining, Pub/Sub, Lua scripting

#### Spring Integration

4. **[Spring Data Redis Integration](./Database/Redis/4.%20Spring%20Data%20Redis%20Integration.md)**
   - Configuration, RedisTemplate, Repository support
5. **[Spring Boot Caching with Redis](./Database/Redis/5.%20Spring%20Boot%20Caching%20with%20Redis.md)**
   - Cache abstraction, Annotations, Configuration

#### Quick References

- **[Redis Spring for Data](./Database/Redis/Redis%20Spring%20for%20Data.md)**
- **[Redis & Spring Data Redis - Interview Cheat Sheet](./Database/Redis/Redis%20%26%20Spring%20Data%20Redis%20-%20Interview%20Cheat%20Sheet.md)**

**[Redis Notes Index](./Database/Redis/README.md)**

---

## 🚀 How to Use

1. **For Interview Preparation**

   - Start with [Quickbites](#-quickbites-cheat-sheets) for rapid revision
   - Deep dive into specific topics using detailed notes

2. **For Learning**

   - Follow the structured learning path in each section
   - Use the index files for navigation

3. **For Reference**
   - Use cheat sheets for quick lookups
   - Bookmark frequently used sections

---

## 🤝 Contributing

Contributions are welcome! If you'd like to:

- Add new notes or cheat sheets
- Fix errors or improve existing content
- Suggest new topics

Please feel free to open an issue or submit a pull request.

---

## 📝 About

This repository serves as a personal knowledge base and interview preparation guide, focusing on:

- **Backend Engineering** - Java, Spring Boot, Microservices
- **Databases** - SQL, Redis, Data modeling
- **Message Queues** - Apache Kafka, Event-driven architecture
- **DevOps** - Docker, Git, CI/CD
- **System Design** - LLD, HLD, Design patterns

### Tech Stack Coverage

**Backend**: Java 8/11+, Spring Boot, Spring Data JPA, Hibernate, REST APIs  
**Databases**: SQL (PostgreSQL, MySQL, Oracle), Redis  
**Messaging**: Apache Kafka, Kafka Streams  
**DevOps**: Docker, Git  
**Frontend**: React, TypeScript  
**Design**: SOLID, Design Patterns, System Design

---

**⭐ Star this repository if you find it helpful!**

---

## 📄 License

This project is open source and available for personal and educational use.

---

**Last Updated**: November 2025
