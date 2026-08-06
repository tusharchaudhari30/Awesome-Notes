# Rust Awesome Notes

> A complete, very detailed guide to the Rust programming language — from toolchain setup and ownership fundamentals to async, unsafe, macros, and production idioms. Written for working engineers and interview preparation.

## Table of Contents

- [Index](#index)
- [How to Read These Notes](#how-to-read-these-notes)

## Index

1. [Getting Started and Toolchain](1.%20Getting%20Started%20and%20Toolchain.md) — rustup, cargo, crates.io, editions, project anatomy, release profiles
2. [Language Fundamentals](2.%20Language%20Fundamentals.md) — variables, shadowing, scalar & compound types, functions, expressions, control flow
3. [Ownership and Borrowing](3.%20Ownership%20and%20Borrowing.md) — the memory model, moves, Copy vs Clone, references, borrow checker rules, slices
4. [Structs Enums and Pattern Matching](4.%20Structs%20Enums%20and%20Pattern%20Matching.md) — structs, methods, enums, Option, match, if let, patterns in depth
5. [Collections and Strings](5.%20Collections%20and%20Strings.md) — Vec, String vs &str, HashMap, BTreeMap, HashSet, VecDeque, choosing the right collection
6. [Error Handling](6.%20Error%20Handling.md) — panic vs Result, the ? operator, custom error types, thiserror, anyhow, error design guidelines
7. [Generics Traits and Lifetimes](7.%20Generics%20Traits%20and%20Lifetimes.md) — generic functions & types, trait bounds, trait objects, standard traits, lifetime annotations & elision
8. [Modules Crates and Workspaces](8.%20Modules%20Crates%20and%20Workspaces.md) — module tree, visibility, use paths, workspaces, feature flags, semantic versioning
9. [Closures and Iterators](9.%20Closures%20and%20Iterators.md) — Fn/FnMut/FnOnce, capture rules, iterator adapters, laziness, zero-cost abstraction
10. [Smart Pointers and Interior Mutability](10.%20Smart%20Pointers%20and%20Interior%20Mutability.md) — Box, Rc, Arc, RefCell, Cell, Weak, Deref, Drop, Cow
11. [Concurrency and Parallelism](11.%20Concurrency%20and%20Parallelism.md) — threads, channels, Mutex, RwLock, atomics, Send/Sync, scoped threads, rayon
12. [Async Programming](12.%20Async%20Programming.md) — futures, async/await, Tokio, pinning, select, streams, cancellation, common pitfalls
13. [Testing and Tooling](13.%20Testing%20and%20Tooling.md) — unit/integration/doc tests, clippy, rustfmt, benchmarking, debugging, CI setup
14. [Unsafe Rust Macros and FFI](14.%20Unsafe%20Rust%20Macros%20and%20FFI.md) — unsafe superpowers, raw pointers, FFI with C, declarative & procedural macros
15. [Idioms Patterns and Performance](15.%20Idioms%20Patterns%20and%20Performance.md) — newtype, builder, typestate, API design, performance checklist
16. [Interview Quick Fire QA](16.%20Interview%20Quick%20Fire%20QA.md) — rapid revision Q&A covering the whole book
17. [Glossary](17.%20Glossary.md) — every term in one table

## How to Read These Notes

- **New to Rust?** Read chapters 1–6 in order. Ownership (chapter 3) is the hill to climb — everything after it gets easier.
- **Coming from Java/C++/Go?** Skim 1–2, read 3 carefully (it is the part your current language does differently), then 7, 9, and 10.
- **Interview tomorrow?** Chapter 16 (Quick Fire QA) plus the tables at the top of chapters 3, 7, and 11.
- **Code samples** are self-contained and compile on stable Rust unless marked otherwise. Try them in the [Rust Playground](https://play.rust-lang.org/).
