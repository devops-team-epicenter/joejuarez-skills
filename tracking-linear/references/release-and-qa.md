## 12. Decide whether QA is required

Respect explicit repository policy and issue requirements.

Suggested default:
Require QA for changes affecting:
- User-facing behavior.
- Authentication and permissions.
- Payments.
- Destructive operations.
- Data migrations.
- Third-party integrations.
- Sensitive or business-critical workflows.

Manual QA may be unnecessary for narrowly scoped documentation
or internal tooling changes when repository policy permits it.

If QA is undecided:
- Treat it as required.
- Record the unresolved decision.
- Do not silently waive it.

Record:
- QA requirement.
- Reason.
- Target environment.
- Test instructions.
- Expected result.
- Tested version or artifact.
- Reviewer or verification source.
- Result and evidence.

Do not claim human QA passed without an actual recorded result.

An agent's checks may satisfy an automated verification requirement,
but must not impersonate human sign-off.

Invalidate or reassess prior QA when subsequent changes affect
the behavior that was tested.

## 13. Distinguish code review from QA

The configured Review status means QA review unless explicitly
configured otherwise.

Use a separate Code Review status or PR metadata for developer review.

Do not treat:
- PR approval as QA approval.
- Passing CI as manual QA.
- QA on an older version as proof for a materially changed version.

## 14. Reconcile status from verified evidence

Apply the repository's configured status mapping.

### Implementation starts

Move to In Progress.

### PR opens or code review is requested

Keep In Progress or use the configured Code Review status.

Do not use the QA Review status merely because a PR needs code review.

### PR merges

Use Merged / Awaiting Deployment when configured.

Otherwise retain an appropriate non-completed status and record
that deployment is pending.

Do not mark Done Staging or Done Production based on merge alone.

### Staging deployment succeeds

If required QA is pending or undecided:
- Move to Review.
- Include the staging URL and QA instructions.

If QA is explicitly unnecessary and required checks passed:
- Move to Done Staging.

### Staging QA passes

Move to Done Staging when all required staging deliverables are present.

### QA fails

Move to In Progress or the configured failure state.

Record:
- Expected and actual behavior.
- Reproduction steps.
- Affected version and environment.
- Relevant evidence.

### Production deployment succeeds

Move to Done Production only when:
- The deployed artifact contains all required changes.
- Required checks passed.
- Required QA gates are satisfied.
- Dependencies and rollout prerequisites are satisfied.
- The requested behavior is available under the configured completion policy.

If required QA is still outstanding:
- Use Review.
- Clearly record that production deployment already occurred.
- Apply incident or rollback policy if the release violated a required gate.

### Deployment fails

Do not advance completion.
Record the failure and retain the last verified valid state.

### Deployment is rolled back

Reconcile the issue to the last verified valid state.

If production no longer contains the fix:
- Remove the implication that it remains complete in production.
- Record the rollback and next action.

### PR closes without merging

Do not mark the issue completed.

Inspect whether the work was:
- Abandoned.
- Replaced.
- Superseded.
- Moved to another PR.

Preserve links and explain the outcome.

## 15. Verify release completeness

Before advancing deployment-related status, verify:

- The correct repository and environment.
- The deployed commit or artifact contains the change.
- All required PRs and repositories are included.
- Required checks passed.
- Required QA applies to the deployed version.
- Required migrations were applied.
- Required configuration and secrets are present without exposing them.
- Required background workers or services were deployed.
- Feature flags are in the intended state.
- No unresolved dependency blocks the outcome.
- The deployment has not been superseded or rolled back.

A successful deployment job is not sufficient when the requested behavior
remains unavailable.

Never infer deployment solely from:
- A branch name.
- A merge timestamp.
- A PR label.
- A comment claiming the release happened.

## 16. Workflow-category semantics

Use the configured completion target.

If production is the finish line:
- Prefer a non-completed category for Done Staging.
- Reserve completed status for Done Production.

If staging is explicitly the final delivery target:
- Done Staging may represent completion.

Do not silently change workspace workflow categories.
Report a mismatch between configuration and intended semantics.

## 17. Durable post-merge automation

A conversational skill does not keep running after the session ends.

Future events require persistent automation such as:
- Git-provider workflows.
- CI/CD hooks.
- Linear release automation.
- A webhook service or scheduled reconciler.

The durable implementation must handle:
- PR merges.
- Deployment success and failure.
- QA results.
- Rollbacks.
- Retries and missed events.

Define one owner for each transition:
- Merge transitions.
- Deployment transitions.
- QA transitions.

Inspect existing integrations before adding another status writer.

Prevent conflicts such as:
- Native merge automation marking Done before deployment.
- A stale staging event overwriting Done Production.
- Two integrations posting the same update.

If automation is missing, report:
"Implementation tracking is configured; post-merge reconciliation
still requires persistent automation."

Never claim to be monitoring future events without a running mechanism.

## 18. Idempotency, concurrency, and recovery

Before creating an issue:
- Recheck for an existing match.
- Reuse the request's durable correlation identifier when available.

For concurrent agents:
- Use a shared lock, serialized creation step, or equivalent coordination
  when the implementation provides it.
- Do not claim a second search alone eliminates duplicate-creation races.

For every event or retry:
- Reuse durable issue, PR, deployment, and event identifiers.
- Re-read current state before writing.
- Avoid duplicate comments.
- Ignore stale or superseded events.
- Verify eligibility before applying a status transition.
- Preserve intentional human changes when stale automation conflicts.

Do not downgrade production completion because an older staging event arrives.

A verified rollback or new QA failure is different from a stale event
and must be reconciled appropriately.

For partial failures:
- Report exactly which operation succeeded and which failed.
- Retry only the failed operation when safe.
- Reuse an issue created successfully even if a later linking step failed.
- Never create another issue merely because a later operation failed.

## 19. Meaningful comments

Add concise comments at material milestones:

- Implementation completed.
- PR linked.
- Required PR merged.
- Deployment succeeded or failed.
- QA passed or failed.
- Blocker discovered or resolved.
- Scope changed materially.
- Release rolled back.

Avoid:
- Comments for every trivial edit.
- Repeating the full description.
- Duplicate webhook updates.
- Empty progress claims.

Prefer updating the existing summary when that communicates the current
state more clearly than another comment.

Each comment should make clear:
- What happened.
- What it means for the user-facing outcome.
- What remains outstanding, if anything.

## 20. Completion report

After acting, return a concise report containing:

- Issue identifier and URL.
- Whether the issue was reused or created.
- Classification.
- Current status.
- Plain-language summary of what was fixed or added.
- Branch and PR links when available.
- Checks performed and their actual results.
- Latest verified deployment environment.
- QA requirement and result.
- Blockers or pending automation.

Clearly distinguish:
- Implemented.
- Merged.
- Deployed to staging.
- QA passed.
- Available in production.

Do not imply all stages are complete when only some are verified.

Example:

Issue: ABC-123 — [issue URL]
Action: Reused existing issue
Classification: Bug + UX Improvement
Status: Review

What was fixed:
Customers now receive a clear explanation when a discount code expires
and can continue checkout without losing their cart.

Validation:
Automated checks passed. Manual QA is pending.

Release:
Available on staging. Not yet available in production.

PRs:
- [PR link]

Remaining:
QA approval, followed by production deployment.
