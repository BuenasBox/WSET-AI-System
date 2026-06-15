# Misconception Closure Implementation Plan

1. Restore the 20 node files to the pre-sprint schemas.
2. Add compatibility tests for legacy loading and non-mutation.
3. Add adapter tests for direct-ID and text evidence across SBA, OR, SAT, and
   explicit weakness-profile events.
4. Implement the adapter and route existing runtime entry points through it.
5. Add evidence history and deterministic low/medium/high labels.
6. Build recommendation and coaching views from existing node fields and WWJ
   remediation.
7. Replace Profile percentage confidence with adapted evidence labels.
8. Filter Full Simulation findings to the current simulation and show evidence,
   practice priority, and next activity.
9. Run backend unit tests, slow tests when required, frontend tests, governance
   scans, and update the closure and validation reports.
