# immune-crystal Whitepaper

## Abstract

immune-crystal is a general-purpose enterprise AI memory middleware that joins two mechanisms: dynamic domain isolation and periodic memory self-repair. Enterprise knowledge is stored as B-Cells, organized by a Domain Registry, inspected by T-Cells, scored by purity, and periodically reweighted by a time-crystal oscillator.

## Memory Oscillation

Each memory cell has a crystal state:

`w_i(t) = w0_i * (1 + alpha * cos(omega_i * t + phi_i)) * exp(-lambda * age)`

Retrieval score:

`score_i = cosine(query, memory_i) * w_i(t) * trust_i`

Stable compliance knowledge receives higher amplitude. Temporary or noisy memory receives stronger decay.

## Immune Layer

B-Cells store enterprise knowledge by arbitrary domain. The Domain Registry learns domain profiles from injected knowledge, compliance tags, and sensitive terms. T-Cells inspect queries for prompt injection, cross-domain leakage, and repeated pollution patterns. Antibodies are generated from repeated blocked inputs.

## Phase Transition

When contradiction is detected, the cell enters quarantine. Its frequency is split, trust is reduced, and the transition is written to audit lineage.

## Purity

Purity is a weighted trust score over contributing cells, penalized by quarantine state. Each answer returns:

- purity score
- B-Cell lineage
- crystal phase
- compliance path
- audit id

## Enterprise Fit

The system is designed for regulated AI use cases where answer correctness is not enough. Enterprises also need provenance, isolation, repair, and replayable audit evidence.
