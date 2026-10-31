# Zi Wei Dou Shu QuickRead

A tiny, manually invoked, read-only helper for concise Zi Wei Dou Shu readings. Use it when the user asks for **紫微斗数简批、快速看盘、简单看一下命盘** or an obvious follow-up such as “那感情呢？” It is a task instruction, not a separate inference engine.

## How to use it

1. Understand the chart and the user's focus from the current conversation. Respect clear requests about a topic, year/range, or length; ordinary natural language is enough. If essential chart information is missing, ask one short clarification instead of guessing.
2. Inspect only the relevant, currently accepted artifacts on repository `main`. Start from current state pointers when needed, then locate the applicable reviewed Zhongzhou knowledge and any existing usable chart/inference outputs. Do not read the whole repository just to produce a short reading.
3. Reuse what is actually available. If an accepted runtime can produce relevant results, use it according to its current instructions. Otherwise, use only directly supported, reviewed source/rule material that can be traced. Never claim a runtime ran when it did not.
4. Write the brief reading in natural Chinese. Default to one paragraph of about 120–220 Chinese characters unless the user asks for another length. Select a few of the clearest, most informative supported points; do not mechanically cover every palace or topic.
5. In follow-ups within the same conversation, treat the user's new focus as a continuation of the same chart unless they indicate a different person/chart. Reuse supported context, and look up new evidence when the new question requires it.

6. If the user explicitly upgrades the request to **详批、完整看盘、全面详解、完整展开** or otherwise asks to cover the chart systematically, hand off to `.agents/skills/social_detailedread/SKILL.md`. Do not keep the QuickRead 120–220-character default after an explicit DetailedRead upgrade.

## Canonical chart prerequisite

- Before using chart facts, require a snapshot produced under `product/CANONICAL_CHART_CONTRACT_v1.1.md`: Zhongzhou + `iztro-js@2.6.1` with the exact frozen configuration and provenance.
- Treat the supplied birth time as already `true_solar_time`; late Zi 23:00–23:59 remains on the supplied date and 00:00 begins the new date. Never apply a second birthplace/location correction in the chart layer.
- If a canonical Product chart generator is available, use it. Never hand-calculate palace placement, stars, transformations, DECADE, YEAR or other temporal scopes.
- A third-party chart image/text or a manually supplied chart without verifiable canonical metadata is **user-supplied, unverified input**, not the system's canonical chart. You may describe that limitation, but must not silently treat it as an iztro-generated Zhongzhou chart.
- If a canonical snapshot/generator is unavailable, do not invent a chart or proceed as if it were verified. Ask for a validated canonical snapshot or state that verified chart calculation is unavailable in the current session.
- A specific time-layer question requires the corresponding iztro-generated temporal scope; do not calculate it from age/year in the verbalizer.

## Evidence boundaries

- Use accepted Zhongzhou-school material and current accepted runtime outputs. Do not silently mix in Qintian, Heluo, online口诀, or model memory as if they were Zhongzhou evidence.
- Do not use an old branch, an unmerged PR, an archived draft, or an Issue description as executable knowledge. For this Skill, accepted `main` is the source of truth; newer accepted content can be used automatically on later runs.
- A natal pattern supports a tendency, not proof that a specific event happened. Current relationship status or a specific-year event needs relevant accepted temporal evidence.
- If a topic or period has no sufficient support, omit it or briefly say that the available evidence is insufficient. Do not expand to unrelated topics to fill the paragraph, and never invent a rule or conclusion to make the reading sound complete.
- Keep rule IDs, source references, internal reasoning, and technical terms out of the user-facing paragraph unless the user asks why. Explain the evidence briefly on request.
- The wording may be warm and conversational, but style must not add new facts. Avoid repetitive rephrasing, canned disclaimers, deterministic promises, and long technical explanations.

## Boundaries

Read-only. Do not modify repository files, Knowledge records, Product registries, rules, state, or runtime. Do not create an Issue/PR or start formal repository work merely because a user requested a reading. This Skill has no delivery dependency on Knowledge or Product: it consumes the relevant accepted content available now, and the reading can become more detailed as future Knowledge/Product updates are accepted on `main`.
