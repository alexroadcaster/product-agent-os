# Product-Agent OS Lifecycle States

Use this reference when a lifecycle skill needs state order, routing, or stop conditions.

State order:

1. `uninitialized`
2. `infrastructure_planned`
3. `requirements_ready`
4. `plan_ready`
5. `team_ready`
6. `build_active`
7. `quality_gate`
8. `review_ready`
9. `release_ready`
10. `learning_ready`
11. `maintenance`

Rules:

- Do not skip lifecycle states. Move in the listed order unless a stop condition is returned.
- Do not skip from `uninitialized` to `build_active`.
- Do not enter `requirements_ready` without a requirements packet.
- Do not enter `plan_ready` without acceptance criteria and verification strategy.
- Do not enter `team_ready` without ownership boundaries when work is parallel.
- Do not enter `release_ready` without verification evidence or documented failures.
- Do not enter `learning_ready` until delivery is complete or explicitly stopped.
- Treat `maintenance` as a routing state, not permission to create active automation.
