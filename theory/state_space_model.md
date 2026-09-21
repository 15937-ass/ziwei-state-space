# State-Space Model — Draft 0.1

## 1. Goal

Represent Zhongzhou “essence -> temporal response” reasoning as a latent-state dynamical system without imposing unsupported empirical weights.

## 2. Generic nonlinear form

```text
x_(t+1) = F_theta(x_t, u_t^astro, G_t, c_t)
y_t     = H_phi(x_t, p_t, c_t)
```

where:

- `x_t`: latent qi state,
- `u_t^astro`: exogenous temporal input (decade/year/month),
- `G_t`: structural relation context,
- `c_t`: additional context,
- `p_t`: palace/domain projection,
- `y_t`: observable/semantic output,
- `theta, phi`: symbolic/unknown parameters.

## 3. Why not assume LTI

The working hypothesis is state-dependent response:

```text
effect(u | x_a) != effect(u | x_b)
```

Thus an initial candidate decomposition is:

```text
x_(t+1) = A(x_t)x_t + B(x_t)u_t + N(x_t, u_t; theta)
```

This is a modeling hypothesis, not a claim that the Zhongzhou corpus explicitly supplies these matrices.

## 4. Palace organization candidates

### Candidate A — local palace states

```text
X_t = [q_1(t), ..., q_12(t)]
q_p(t) in Q
```

### Candidate B — global latent state + palace projections

```text
x_t in Q
y_p = P_p(x_t)
```

Decision deferred until rule/ontology extraction shows which representation is less redundant.

## 5. Modifier representation

Possible operator form:

```text
x' = T_m(x)
```

with source-derived operator class:
- strengthen,
- weaken,
- transform,
- inhibit,
- activate,
- conditional response.

Magnitude remains symbolic.

## 6. Star-system interaction

Candidate decomposition:

```text
H_ij = S_i + S_j + Delta_ij
```

where `Delta_ij` is an interaction/emergence term.

This is an analysis device. The final model may use a nonlinear operator `Phi(S_i,S_j)` instead.

## 7. Observation model

```text
y_p = P_p(x_t)
```

The same latent state may map to different domain manifestations under different palace projections.

## 8. Paper-1 control-theoretic scope

Paper 1 may discuss:
- state definition,
- inputs/outputs,
- structural coupling,
- structural observability questions,
- symbolic gains,
- nonlinear response.

Paper 1 does not require:
- fitted A/B/C/D matrices,
- numerical controllability rank,
- Kalman filtering on real cases,
- empirical parameter estimation.

Those belong to the next phase.
