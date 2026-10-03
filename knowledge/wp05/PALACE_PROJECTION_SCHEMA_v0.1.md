# PALACE_PROJECTION_SCHEMA v0.1

Status: **ACTIVE — WP05 P00**

## 1. Purpose

WP05 models the twelve palaces as **observation / projection contexts** applied to an already constructed natal/system state. It does not rebuild a new star essence for each palace.

Source-grounded principle from the Zhongzhou lower-volume `宫垣论`:

1. first establish the basic nature of each natal palace from the stars in that palace together with its triad and opposite palace;
2. when decade/year palaces move, interpret the moved configuration as a **reaction to an existing natal palace nature**, not as an isolated replacement;
3. avoid mechanical inference that reads only the current `三方四正` and ignores the natal palace state.

Project formalization:

```text
E                = immutable natal essence / natal system state
U_t              = temporal input at t
R_t              = React(E, U_t, Z_t, G_t, C_t)

C_p              = palace projection context
C_p = {
  palace_id,
  scene,
  own_palace_state,
  opposite_palace_state,
  triad_states,
  time_layer,
  active_temporal_overlays
}

Y_(p,t) = Project_p(R_t, C_p)
```

`Project_p` is a symbolic mapping interface. It is **not** a learned scalar score and does not imply linearity.

## 2. Hard layer boundary

WP05 must preserve the existing separation:

```text
L0  structure / topology
L1  latent or local state
L2  relational / interaction response
L3  palace/event-language projection
```

A source sentence such as “某星在夫妻宫主某婚姻事件” does not automatically create a new L1 latent state. Unless the source independently defines a reusable underlying state, the event wording stays at L3.

## 3. Palace topology

Canonical palace order:

```text
命 -> 兄弟 -> 夫妻 -> 子女 -> 财帛 -> 疾厄
   -> 迁移 -> 交友 -> 事业 -> 田宅 -> 福德 -> 父母
```

Opposition and triad relations are stored explicitly in `palace_ontology_v0.1.csv`.

The topology is discrete. WP05 does **not** assign numeric weights such as “本宫 0.5 / 对宫 0.3 / 三合 0.2”. The source supplies structural relations, not metric weights.

## 4. Palace identity versus scene

A palace may support more than one source-defined or source-expanded scene. Therefore:

```text
palace_id != scene_id
```

Examples:

- 父母宫: `parents` and `superiors_or_supervising_institution`
- 子女宫: `children` and `proteges_or_trusted_juniors`
- 田宅宫: `property_or_home` and `work_or_service_institution`
- 兄弟宫: `siblings` and `same_generation_peers`
- 交友宫: `subordinates_or_lower_generation_contacts`, but **not** all peer friends

This prevents a single star combination from being projected simultaneously into incompatible real-world roles.

## 5. Temporal semantics

Allowed `time_layer` values:

- `NATAL`
- `DECADE`
- `YEAR`
- `MONTH`
- `DAY`
- `HOUR`

The source distinction is represented as:

```text
natal palace state = baseline palace nature
moved/time-layer palace = environmental / temporal reaction input
```

A temporal palace does not rewrite natal essence.

If a source explicitly states that one period changes a later period, the record must route through the approved A2-R1 history schema. WP05 itself must not invent recurrence.

## 6. Projection record schema

Canonical WP05 projection records use the following fields.

### Identity / provenance

- `projection_rule_id`
- `source_id`
- `source_location`
- `source_span`
- `source_epistemic`
- `normalization_epistemic`
- `review_status`
- `reviewer_type`
- `reviewer_id`
- `reviewed_at`

### Structural context

- `palace_id`
- `scene_id`
- `time_layer`
- `base_subject`
- `base_state_ref`
- `modifier_refs`
- `condition`
- `opposite_palace_dependency`
- `triad_dependency`
- `cross_palace_dependency`

### Projection semantics

- `projection_domain`
- `projection_target`
- `projection_mode`
- `direction_or_state`
- `literal_claim`
- `normalized_claim`
- `event_specificity`
- `case_support_only`

### Audit / execution

- `source_span_verified`
- `normalization_verified`
- `history_feedback`
- `human_gate_required`
- `notes`

## 7. Controlled projection modes

WP05 v0.1 allows:

- `STATE_EXPRESSION` — a reusable state expressed through a palace scene
- `RELATIONAL_PROJECTION` — relationship between self and another role
- `FUNCTIONAL_PROJECTION` — career/resource/organizational or other functional expression
- `CROSS_PALACE_CONSTRAINT` — source explicitly requires another palace to constrain interpretation
- `EVENT_CANDIDATE` — concrete event-language output; normally L3
- `TIMING_TRIGGER` — source explicitly identifies a time-layer trigger
- `SCENE_TRANSLATION` — same palace structure translated to a second source-supported scene

No mode implies probability or numeric magnitude.

## 8. Event specificity

Controlled `event_specificity`:

- `ABSTRACT` — broad expression, e.g. resource retention, mobility, emotional stability
- `SCENE_LEVEL` — marriage, career, subordinate relation, property, health, etc.
- `CONCRETE_EVENT` — specific marriage, illness, accident, legal, death, childbirth, exact occupation, etc.

Default routing:

```text
ABSTRACT       -> eligible for reusable projection rule
SCENE_LEVEL    -> eligible with explicit palace scene
CONCRETE_EVENT -> usually CASE_SUPPORT_ONLY unless a reusable mechanism is independently supported
```

## 9. Cross-palace constraints

The source repeatedly requires cross-palace reading. WP05 therefore supports dependencies without collapsing them into one latent state.

Examples of structural dependency classes:

- `OWN_PLUS_OPPOSITE`
- `OWN_PLUS_TRIAD`
- `OWN_PLUS_OPPOSITE_PLUS_TRIAD`
- `OWN_PLUS_NAMED_PALACE`
- `GLOBAL_CHART_CHECK`

The dependency class records **what must be consulted**, not how strongly it is weighted.

## 10. Palace-specific decontamination rules

1. **兄弟 vs 交友**  
   Peer friendship remains primarily a 兄弟宫 scene; 交友宫 is biased toward subordinates / lower-generation contacts. Do not merge them.

2. **子女 vs 交友**  
   Ordinary employees/subordinates belong to 交友; personally cultivated, promoted, close junior assistants may project through 子女.

3. **事业 vs 财帛**  
   Career prominence and financial gain/retention are separable. A strong career projection does not imply strong financial retention.

4. **夫妻 vs 事业**  
   Mutual influence is allowed, but marriage outcome and career outcome remain separate targets.

5. **疾厄**  
   Do not infer disease from the natal 疾厄宫 alone when the source requires 命宫、福德宫 or temporal activation.

6. **迁移**  
   Separate `mobility` from `outcome_after_movement`. A movement signal is not automatically a gain signal.

7. **福德 vs 命宫**  
   Mental/subjective enjoyment and outer/material life expression remain separable.

8. **父母**  
   Parent scene and superior/institution scene must be explicitly tagged; the same star combination may translate differently.

9. **田宅**  
   Property/home and service-institution/work-environment scenes must be tagged separately.

10. **古今语义**  
    Ancient offices, occupations, family structures, gender norms and concrete social labels are not silently mapped one-to-one into modern categories. Use `CASE_SUPPORT_ONLY` or an auditable `SCENE_TRANSLATION`.

## 11. Acceptance gate for a WP05 rule

A projection rule is executable only if:

1. palace / scene is explicit or auditable;
2. source span is verified;
3. underlying state/operator is not quarantined;
4. no new primitive qi is invented from event wording;
5. no continuous weight is invented;
6. time-layer semantics do not overwrite natal essence;
7. source-explicit long-memory is routed through A2-R1 history;
8. any concrete event remains L3 unless separately justified.

## 12. P00 conclusion

P00 introduces no new Human Gate.

It formalizes the existing Zhongzhou logic as:

```text
natal/system state
    -> modifier/operator response
    -> palace semantic context
    -> cross-palace constraints
    -> temporal activation
    -> scene/event projection
```

The next work unit is P01: source-span extraction of the `命宫` corpus using this schema.
