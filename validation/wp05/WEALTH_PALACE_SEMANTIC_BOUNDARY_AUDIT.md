# WP05 Wealth Palace Semantic Boundary Audit

Status: **SOURCE-VERIFIED — EXISTING P05 ONTOLOGY CONFIRMED**

The Wealth Palace chapter explicitly requires several distinct state variables rather than a single wealth-fortune score:

- resource acquisition / earning ability and opportunity;
- earning mode and effort cost;
- money-flow intensity and volatility;
- financial management;
- accumulation / retention;
- spending or enjoyment, modified through the opposite Fortune Palace;
- career/industry interaction through the Career Palace;
- life-pattern scale through the Life Palace;
- property/real-estate as a possible retention channel through the Property Palace.

Implementation consequence:
- keep P05 primary scope resource_acquisition, earning_mode, financial_flow;
- keep secondary scope resource_management, retention, career_income_relation;
- preserve P11 Fortune Palace as the consumption/enjoyment and mental-cost counterpart;
- preserve P09 Career Palace as industry/organizational-role context rather than career prominence = wealth;
- preserve P01 Life Palace as overall life-pattern scale rather than money amount;
- preserve P10 Property Palace as a context-specific retention/store channel;
- do not collapse can earn, can manage, can save, has large flow, and can enjoy into one latent variable.
