# Git-Based AI Development Token and API-Equivalent Cost Ceiling

**Date:** 2026-11-15  
**Status:** Research result; proposed analytical method, not adopted collection behavior  
**Subject:** Estimate a deliberately high, reproducible API-equivalent token and USD envelope for AI-assisted development from canonical Git activity without pretending that Git records actual model usage.

## Main conclusions and decision

1. **Git history is usable as an output-activity proxy, not a token meter.** An AI-created commit does not disclose the number of model calls, prompt tokens, reasoning tokens, discarded attempts, file reads, subagents, or retries that produced it.
2. **There is no finite, empirically defensible absolute upper bound on token consumption from a commit count alone.** Arbitrarily many unsuccessful calls may precede one commit, and work may consume tokens without producing a commit. A useful ceiling is therefore **conditional on explicit limits assigned by the analyst**, never a claimed measurement or a mathematical upper bound on actual ChatGPT activity.
3. **For a single conservative planning headline, use the declared high-envelope scenario described below:** four equivalent model calls per canonical commit; 300,000 uncached input tokens and 80,000 output tokens per call; the published long-context API rates for the Sol model family. As of 2026-11-15 this is **1.52 million hypothetical tokens and USD 9.60 per commit**. These inputs are intentionally aggressive scenario controls, not observed averages and not a claim that every commit actually crosses the long-context threshold.
4. **Maximum reasoning effort affects the number of reasoning tokens, not the model's quoted per-token tariff.** Reasoning is part of billed output. Chat GPT-6 Sol at High and Work GPT-6.1 Sol at Max should be mapped to their respective API model IDs for counterfactual valuation, not to a nonexistent special “Max price.” [S1][S2][S3]
5. **One USD figure may be presented only with its exact envelope definition:** “Sol-family API-equivalent stress ceiling under declared assumptions,” not “actual API bill,” “OpenAI cost,” “ChatGPT tokens spent,” or “proven maximum.”
6. **Keep the evidence collector unchanged.** Compute this estimate in a separate derived-analysis layer using existing daily commit observations. Do not add inferred token or dollar fields to canonical observational CSVs. The collector remains an evidence collector, not a billing simulator.

## 1. Question, working assumptions, and exclusion boundary

The desired use case is an owner whose software changes are overwhelmingly performed by AI agents in interactive ChatGPT and ChatGPT Work. Each canonical Git commit is treated as an AI-development output event, even when the visible commit was made by an automated tool. Conventional human-only commits are assumed negligible for this owner's intended estimate.

The model configuration to value is:

| Interaction surface | User-selected reasoning | API pricing proxy |
| --- | --- | --- |
| Ordinary ChatGPT chat | Sol, High | gpt-6-sol at Standard token rates |
| ChatGPT Work | Sol 6.1, Max | gpt-6.1-sol at Standard token rates |
| Codex | Not material to this use case | Excluded |
| Astra | Rarely selected; explicitly excluded from headline | Excluded |

This mapping is **counterfactual**, not a statement that the ChatGPT subscription routes each internal model call identically to the public API. Agent orchestration, model routing, tools, credits, cache treatment, and included usage may differ. GPT-6.1 Sol has a default 500,000-token context window in Work; subscription-included Work usage has no separate long-context surcharge, whereas API-equivalent usage can have one. [S2][S4]

Planning conversations, unattached research and draft Markdown work that never reaches Git are deliberately excluded. The resulting metric estimates **Git-visible AI development activity**, not all account activity.

Study scope: reproducible daily, weekly, monthly, hourly, per-repository, portfolio, and group aggregation; explicit upper-scenario token and USD conversion; tests and failure conditions. Implementing a new collector or billing feature is outside this research result.

## 2. Separate what Git proves from what the model assumes

### 2.1 Observable facts

From canonical reachable Git history, the system can establish:

- N(d,r): count of distinct reachable commits with committed timestamp in UTC day d in repository r.
- F(d,r): sum of changed-file occurrences reported for those commits, when available; this is not unique-file count and must preserve unknowns.
- Historical dates, active hours and commit bursts, if individual commit timestamps are available for transient analysis.
- Other high-level repository observations already defined in the evidence contract.

None of these fields directly counts AI interactions. One agent may publish many commits; many agents may produce one commit; an agent can explore and fail without any commit; mass mechanical transformations can create large files with limited direct language-model output. A merge can introduce commits created at earlier dates, and a history rewrite can remove previously visible commits.

### 2.2 Hidden variables

For the actual AI execution, let j index every model request across chat, root agents, subagents and retries.

- I_j: uncached input tokens.
- IC_j: cached input tokens.
- O_j: output tokens including visible text, tool-call arguments and hidden reasoning.
- W_j: any cache-write tokens charged separately by the relevant API tier.
- M_j: model identifier and reasoning-effort configuration.
- L_j: short- or long-context pricing regime.
- X_j: separately billable tools, search, compute, third-party requests and service-tier adjustments.

True billed API-equivalent cost would require summing those quantities **for every actual request**. No function of commit count alone uniquely reconstructs them. OpenAI states that reasoning tokens are included in output tokens and that agents may make multiple model calls, including calls by subagents and retries. [S3]

### 2.3 What “ceiling” can and cannot mean

Three distinct meanings must not be conflated:

- **Physical absolute maximum:** maximum real expenditure compatible with a known Git history. It is unbounded without restrictions on calls, retries or time, so the maximum cannot be calculated.
- **Declared scenario ceiling:** maximum expenditure **inside a researcher-specified workload envelope**, such as at most four model-call equivalents per commit with fixed per-call token caps. This is finite and reproducible but remains assumption-conditional.
- **Estimated upper quantile:** e.g. a calibrated 95th or 99th percentile from actual usage traces. Such a statistical bound is unavailable without a representative sample of observed token logs.

This study adopts the second meaning. Calling it a guaranteed upper bound on the real workload is prohibited.

## 3. Model pricing baseline as of 2026-11-15

Published API prices per one million text tokens, Standard processing:

| API model | Short input | Short cached input | Short output | Long input | Long cached input | Long output |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt-6-sol | $2.00 | $0.20 | $10.00 | $4.00 | $0.40 | $15.00 |
| gpt-6.1-sol | $2.00 | $0.10 | $10.00 | $4.00 | $0.20 | $15.00 |

For these model pages, a request with **more than 272,000 input tokens** is priced at double the applicable input/cache rates and 1.5 times the short-context output rate **for the entire request**, not only the portion above the threshold. [S1][S2]

Important distinctions:

- High and Max are reasoning-effort configurations; the pricing pages do not set a separate surcharge per token merely because reasoning effort is higher. A harder setting can generate more output/reasoning tokens.
- Cached input is not free, but assuming **zero cache hits** intentionally increases the counterfactual estimate.
- Separately priced cache writes are possible in the API; the chosen scenario assumes **no explicit cache-write operation**, not that all possible API architectures lack cache-write charges.
- Fast and Ultrafast are separate **processing-service choices**, not synonyms for “High” or “Max” thinking. They are excluded from the headline as there is no evidence the interactive subscription purchased those API tiers.
- API token valuation is not ChatGPT Plus subscription billing, the provider's internal cost, a Work credit estimate, or a refund entitlement.
- API model prices, model availability, long-context thresholds and pricing rules are time-sensitive; the estimator must version its tariff snapshot.

A useful generic per-request equation is:

    C_j = (I_j * p_in + IC_j * p_cached + O_j * p_out
           + W_j * p_write) / 1,000,000 + X_j

Use request-specific rates p based on model, context threshold and service tier. Never add reasoning tokens again when they are already included in O_j; never add cached tokens to input if I_j already includes them. In a conventional usage structure, input total includes cached tokens, so uncached input equals input_total minus cached_input. [S3]

## 4. Default maximum-effort Sol-family stress envelope

This section defines **one** numerical upper-scenario calculation; lower, median and probabilistic estimates are outside the preferred headline.

### 4.1 Declared parameters

| Parameter | Value | Interpretation |
| --- | ---: | --- |
| K | 4 | Maximum *equivalent model calls* charged to each counted Git commit within this scenario |
| I | 300,000 | Input tokens per call |
| O | 80,000 | Output tokens per call, **including** hidden reasoning |
| Cached input | 0 | No prompt-caching discount |
| Context regime | Long on every call | I > 272,000, invoking long-context API prices |
| API input price | $4.00 / million | Both selected Sol models, long-context Standard |
| API output price | $15.00 / million | Both selected Sol models, long-context Standard |
| Extra tool costs | Not assigned | Unknown and excluded from this **token-only** proxy |
| Commit attribution | 100% AI | User-supplied use-case assumption |
| Countable commits | Canonical reachable unique commits | Not workflow runs, changed files, author events or temporary branch copies |

Per equivalent call:

    T_call = I + O
           = 300,000 + 80,000
           = 380,000 tokens

    C_call = 300,000 / 1,000,000 * $4
           +  80,000 / 1,000,000 * $15
           = $1.20 + $1.20
           = $2.40

Per commit:

    T_commit = K * T_call = 4 * 380,000 = 1,520,000 tokens
    I_commit = K * I = 1,200,000 input tokens
    O_commit = K * O = 320,000 output tokens
    C_commit = K * C_call = 4 * $2.40 = $9.60

The 80,000-token output assumption is below the model's published 128,000-token maximum output per call. The long-context price selection is intentional and conservative for this scenario; the scenario **does not assert** that actual interactive requests had input lengths above 272K. [S1][S2]

K = 4 is not a provider-supplied bound or verified agent-call count. It makes the stress budget concrete; if an actual commit was preceded by more than four such call equivalents, the declared envelope is exceeded. Equally, a single very large context assembly, failed research branch or multiple subagents could exceed its assumptions.

### 4.2 Calculation for any day, repository or portfolio

Let N_d be the number of canonical commits assigned to a UTC day, summed across the desired repository set after applying the repository ownership and deduplication rules below.

    Input_stress(d)  = N_d * 1,200,000
    Output_stress(d) = N_d *   320,000
    Total_stress(d)  = N_d * 1,520,000
    USD_stress(d)    = N_d * $9.60

For N = 1,000 commits:

- 1.2 billion hypothetical input tokens;
- 320 million hypothetical output tokens, including reasoning;
- 1.52 billion hypothetical tokens in total;
- **$9,600** API-equivalent token cost.

These figures are a high-assumption **budget ceiling**, not a claim that an actual 1,000-commit period spent 1.52 billion tokens. Their purpose is comparability across portfolio sizes when the user explicitly wants to stress-test maximum-effort Sol usage.

### 4.3 Why raw artifact size must not become billed output

A large generated JSON, source file, diagram, CSV or Markdown result is not necessarily model-output text. It might have been created by a deterministic script, copied or transformed from prior data, compressed, templated, or committed as a binary. Conversely, extensive hidden analysis and tool-output reading can happen with a tiny final patch.

Thus:

- Bytes added, diff lines and repository size are **complexity and QA signals**, not chargeable tokens.
- Do not assume all text in a final repository was directly emitted by the language model.
- Do not add estimated artifact tokens to the K × O allowance unless a separate model-output trace confirms they are distinct; otherwise double counting is likely.
- Do not infer reasoning volume by multiplying visible output tokens by a fixed official ratio: no such general conversion is published.

## 5. Daily, hourly and portfolio aggregation

### 5.1 Authoritative daily calculation

The existing Observatory evidence model provides fully closed UTC days and canonical reachable commit counts. An external estimator should read daily N(d,r), apply the fixed declared coefficient, and aggregate additively:

    portfolio_tokens(d) = SUM_over_repositories N(d,r) * 1,520,000
    portfolio_usd(d)    = SUM_over_repositories N(d,r) * 9.60

Weekly, monthly, year-to-date, annual and grouped summaries are sums of these **derived** daily values, not separate inference passes and not sums of repository snapshots. The UTC day definition must match the canonical activity data.

Date joins must be explicit; unavailable collection is not a day of zero activity. A missing row, inaccessible repository or unknown change count must remain unknown under the evidence contract.

### 5.2 Hourly aggregation is a different evidence surface

The normal Observatory dataset contains daily canonical activity, not a durable per-commit time ledger. It is **incorrect** to split daily tokens evenly over 24 hours or to invent an hourly series from daily rows.

To make an hourly analysis:

1. Temporarily fetch canonical commits and their committed timestamps for the target historical window.
2. Deduplicate by repository identity and commit SHA.
3. Assign every commit to a UTC hour from its Git committed timestamp.
4. Multiply count(hour) by the same configured stress coefficient.
5. Clearly label this as **hour-of-publication attribution**, not hour-of-computation measurement.
6. Do not persist commit SHA, messages, authors, paths, timestamps, diffs or per-commit traces in the canonical Observatory dataset. If durable hourly estimates are separately authorized, persist aggregate hourly counts/derived estimates only in a distinct derived layer with complete provenance and no accidental claim that they are collector observations.

An agent may consume tokens for hours before its commit, with multiple concurrent agents publishing in a burst. Consequently, commit-hour peaks reflect Git event concentration more directly than the true per-hour inference workload.

### 5.3 Repository grouping, completeness and history semantics

- Use discovered repository identities, not a manually maintained collection allow-list.
- Deduplicate repeated observations of the same commit within the same repository.
- Count a commit once in a selected canonical reachable history; avoid counting it again merely because it was seen on a different branch.
- If a commit appears in distinct repositories, portfolio aggregation can count its role in each repository under a **per-repository output** metric; a cross-repository global-unique-work metric is separate and would require its own identity policy.
- Preserve deleted, renamed, transferred or archived repository identity rather than silently losing earlier observed output; avoid double counting when names change.
- Git history may be rewritten; a refreshed canonical activity series can change past dates. Historical ceiling estimates should be recomputed from the versioned activity evidence, not assumed immutable.
- Exclude current-day partial data from the canonical daily pipeline in accordance with the existing closed-day contract.
- If the portfolio includes automated non-AI commits, a configurable owner-specific attribution fraction may later be justified; the present commissioned case sets this to 1.0.

### 5.4 The changed-file-occurrence field

F(d,r) is valuable as an audit covariate but should **not** secretly multiply the headline ceiling. Large changed-file counts can reflect mechanical formatting, bulk data, merges or automated generation. Counting each changed file as an additional full model session would inflate the model without evidence.

Useful secondary descriptive checks are F/N when both fields are known, percent unknown changed-file counts, distributions of commits over dates, and structural discontinuities in activity. These metrics can direct future calibration but do not change the declared USD 9.60 per commit coefficient.

## 6. Worked aggregation and exact reproducibility

For illustration, suppose a three-day activity observation contains 48, 363 and 424 canonical commits. The total is 835 commits.

| UTC day | Commits | Stress input | Stress output | Total stress tokens | API-equivalent USD |
| --- | ---: | ---: | ---: | ---: | ---: |
| Day A | 48 | 57.6M | 15.36M | 72.96M | $460.80 |
| Day B | 363 | 435.6M | 116.16M | 551.76M | $3,484.80 |
| Day C | 424 | 508.8M | 135.68M | 644.48M | $4,070.40 |
| **Total** | **835** | **1,002.0M** | **267.20M** | **1,269.20M** | **$8,016.00** |

The arithmetic is correct **conditional on the chosen per-commit assumptions**. It is not evidence that the corresponding real executions consumed those numbers. If an empirical audit produces materially smaller or larger numbers, report them as observed and retain this scenario as an explicitly different counterfactual calculation.

Reference pseudocode for daily derived calculation:

~~~python
from decimal import Decimal

CALLS_PER_COMMIT = 4
INPUT_PER_CALL = 300_000
OUTPUT_PER_CALL = 80_000
USD_PER_M_INPUT = Decimal("4")
USD_PER_M_OUTPUT = Decimal("15")

def stress_from_commits(commits: int):
    if commits < 0:
        raise ValueError("commit count must be nonnegative")
    inp = commits * CALLS_PER_COMMIT * INPUT_PER_CALL
    out = commits * CALLS_PER_COMMIT * OUTPUT_PER_CALL
    usd = (
        Decimal(inp) * USD_PER_M_INPUT
        + Decimal(out) * USD_PER_M_OUTPUT
    ) / Decimal(1_000_000)
    return {"input_tokens": inp, "output_tokens": out,
            "total_tokens": inp + out, "api_equivalent_usd": usd}
~~~

The function is purely analytical. Data acquisition, missing-source handling, grouping, tariff snapshots and presentation must remain separate responsibilities.

## 7. Attribution to Chat High versus Work Max

Git commits do not identify the ChatGPT interaction surface or the reasoning mode. Inferring “Work” from a long task, a commit message, edit magnitude or agent naming would be speculative.

For the requested conservative scenario, this uncertainty **does not prevent a common dollar headline**, because the selected short and long **uncached** input/output rates are equal for gpt-6-sol and gpt-6.1-sol. The two models differ in cached-input prices, which the zero-cache stress envelope intentionally ignores. [S1][S2]

Maintain an optional analytical surface label only if it is independently known from a permitted user-supplied task ledger or usage trace. Otherwise show “Sol family / interaction surface unknown,” never fabricate a 70/30 or 80/20 Chat/Work split.

A highest reasoning configuration does not imply all 80K hypothetical output tokens were reasoning tokens. For the chosen scenario, output includes reasoning as a **budget category**; visible and hidden output cannot be separated without traces.

## 8. Rigorous alternatives and model limitations

A commit-proportional stress ceiling is intentionally simple and comparable, but has predictable failure modes:

1. **One commit, many failed tries:** true consumption can exceed the declared bound.
2. **One agent, many tiny commits:** stress allocation can drastically exceed true usage.
3. **Large bulk generated artifacts:** added bytes have little relationship to billed model output.
4. **Research without commit:** omitted by the requested Git-visible scope.
5. **Tool-heavy work:** token proxy excludes separately charged search, hosted compute, external APIs and other tools.
6. **Subagents:** more model requests can occur than the assigned K call equivalents.
7. **Very long sessions:** repeated history rereads may dominate even when final diffs are small.
8. **Prompt caching:** zero-cache assumption increases proxy relative to cache-aware pricing, but does not constitute proof of an upper bound on call count.
9. **Model routing:** an interactive ChatGPT surface need not match a public API deployment exactly.
10. **Commit timestamp:** determines historical attribution, not the time inference was performed.
11. **History changes:** current canonical Git history is not an immutable activity event log.
12. **Selection bias:** the portfolio's Chat/Work distribution, task types, and human interventions cannot be inferred from Git alone.

### Explicit non-claims

Do not state: “This user spent $8,016,” “This period used 1.269B tokens,” “the actual maximum was $8,016,” “reasoning Max costs 6x more,” “all bytes committed were generated output tokens,” or “the number of commits measures prompts.”

State: “For 835 canonical commits, the **declared four-call, long-context, no-cache, 300K-input/80K-output Sol-family stress scenario** evaluates to **1.269B hypothetical tokens and $8,016 API-equivalent token cost**.”

### Calibration path when real usage becomes available

A later, separately authorized refinement should join a **permissioned, aggregated** usage dataset to time windows or task groups, without storing raw prompts, reasoning traces or repository contents. Record actual input, cached input, output (including reasoning), tool costs, model IDs, date windows, and successful versus failed agent runs where available.

Compare actual tokens/commit and cost/commit only within matched task classes, then adjust K, I and O or replace the scenario with empirically measured high quantiles. Do not secretly convert a calibrated quantile into a hard bound. The original fixed envelope should remain versioned for historical comparability.

If a reliable model-call log exists, direct aggregation of actual token counts **supersedes** proxy inference. Git data then provides output provenance, not billing evidence.

## 9. Proposed separation of responsibilities

| Layer | Responsibility | Action authorized by this research |
| --- | --- | --- |
| Canonical Observatory collector | Preserve closed-day repository evidence and its existing semantics | **No change** |
| Derived analytical computation | Apply an explicitly versioned stress-envelope formula to canonical counts | Method specified; implementation not authorized |
| Tariff registry | Maintain date/version, model ID, service tier, context threshold and rates | Concept specified; no new persistent registry authorized |
| Presentation | Display daily/hourly, grouped and portfolio hypothetical tokens and USD with caveats | Concept specified; no dashboard change authorized |
| Real usage reconciliation | Optional future usage-trace calibration with permissions | Research horizon only |

Suggested derived-output labels: **AI-attributed canonical commits**, **Hypothetical input tokens — stress scenario**, **Hypothetical output + reasoning tokens — stress scenario**, **Total hypothetical tokens**, **Sol API-equivalent USD**, **Envelope version**, **Tariff as-of date**, **Observation completeness**, and **Git committed-time attribution**.

The estimate must not be inserted into canonical repository/activity/language/Traffic datasets, because it is an analyst-derived claim rather than a GitHub observation. A research document alone is sufficient as the current durable result.

## 10. Acceptance and falsification checks

A future implementation can be checked against:

1. N = 0 on a known complete closed day produces zero *Git-visible* proxy, never a claim of zero AI activity.
2. N = 1 produces 1.52M hypothetical tokens and $9.60 with the documented envelope.
3. N = 835 produces 1,269.20M hypothetical tokens and $8,016.00 exactly.
4. Sum of daily-derived totals equals portfolio-derived totals when the same repository set, dates and envelope are used.
5. Changing context pricing, model or reasoning labeling never silently modifies historical tariff versions.
6. Cached input, reasoning output, long-context multipliers and per-call totals are not double counted.
7. Missing repository days, unknown file counts and failed collection remain unknown, not zeros.
8. Hourly figures do not appear unless an independent per-commit timestamp source has been examined.
9. Historical rebase/merge changes are handled by canonical history semantics.
10. No repository files, commit messages, author identities, paths or per-commit patches are persisted by the Observatory collector.
11. No private-repository Actions workflows are launched as part of this research.
12. The UI never calls a scenario-derived number a measured token count or a guaranteed maximum.

## 11. Outcome and open questions

**Outcome:** A reproducible **high Sol-family API-equivalent counterfactual** is specified using the Observatory's existing canonical commit counts, with a deliberately strict no-cache and long-context tariff choice. The per-commit multiplier is 1.52M hypothetical tokens and $9.60, and it scales linearly to time periods, repositories and portfolio groups.

**What remains unknown:** actual agent-call counts, actual token usage, hidden reasoning, cache hits, how much work was performed in Chat versus Work, any non-token charges, and whether real execution falls above or below the chosen envelope.

**Decision boundary:** This result establishes an analytical formula and its limitations; it does **not** authorize edits to the collector, schema, Action schedules, stored observations, documentation routes, or web presentation. Any product integration must be commissioned separately.

## External sources

- **[S1] GPT-6 Sol model pricing and long-context rule.** Supports the gpt-6-sol short/long API rate baseline, the 272K input threshold and the 128K maximum output specification. OpenAI API model documentation: https://developers.openai.com/api/docs/models/gpt-6-sol
- **[S2] GPT-6.1 Sol model pricing and Work context distinction.** Supports gpt-6.1-sol short/long API rates, 272K threshold, 128K maximum output, and the distinction between a 500K default Work context and API long-context pricing. OpenAI API model documentation: https://developers.openai.com/api/docs/models/gpt-6.1-sol
- **[S3] Agent-model token accounting.** Supports model-call, subagent and retry accounting, with reasoning included in output and cached input included in input totals. OpenAI API Agents observability documentation: https://developers.openai.com/api/docs/guides/agents-api/observability
- **[S4] Work/Codex usage model.** Supports the separation between ChatGPT subscription usage and purchased/API usage, GPT-6.1 Sol availability and 500K default Work context. OpenAI Help Center: https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
