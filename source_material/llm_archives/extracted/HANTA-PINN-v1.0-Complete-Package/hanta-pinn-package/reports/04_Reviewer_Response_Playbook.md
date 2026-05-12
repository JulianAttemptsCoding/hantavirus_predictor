# REPORT 4: Reviewer Response Playbook
**Version:** 1.0-FINAL  
**Date:** 2026-05-11  
**Purpose:** Anticipate and pre-draft responses to all likely reviewer objections

---

## OBJECTIVE

This document contains verbatim anticipated reviewer objections and our pre-drafted responses. Each response is backed by evidence, citations, and references to specific sections of the manuscript.

---

## OBJECTION 1: DATA SCARCITY

**Reviewer:** "You only have 5 years of NEON data (2014-2019). That is not enough to train a deep learning model. How can you claim this is statistically sound?"

**Response:**

Thank you for raising this important concern. We address data scarcity through four complementary strategies:

1. **Primary target is rodent seroprevalence, not human cases.** The model trains on 14,004 seroprevalence samples from NEON, not the ~890 sparse human cases. Humans are dead-end hosts for Sin Nombre virus; predicting reservoir dynamics is the biologically correct approach.

2. **Physics-informed constraints reduce data requirements.** The SEIR ODE residual loss acts as a strong implicit regularizer, restricting the hypothesis space to physically plausible solutions. Prior work (Raissi et al., 2019; Qian et al., 2025) demonstrates that PINNs require an order of magnitude less data than pure neural networks for epidemic forecasting.

3. **Synthetic pretraining.** We generate 10,000 synthetic SEIR trajectories by sampling parameters from literature priors (Allen et al., 2006). The PINN is pretrained on these trajectories before fine-tuning on real data, ensuring it learns physically valid dynamics.

4. **Transfer learning.** The environmental encoder is pretrained on leptospirosis and dengue time-series data, which share climate-driven seasonality patterns with hantavirus.

**Evidence:** See Section 2.4 (Data Scarcity Mitigation) and Supplementary Appendix B.

---

## OBJECTION 2: OVERFITTING

**Reviewer:** "Your model has ~250,000 parameters. With only 14,000 training samples, how do you avoid overfitting?"

**Response:**

The concern about overfitting is valid, but our architecture includes multiple safeguards:

1. **Physics loss as regularization.** The ODE residual term in the loss function (alpha_physics = 0.3) penalizes solutions that violate biological conservation laws. This is equivalent to adding ~10,000 soft constraints (one per collocation point), dramatically reducing effective degrees of freedom.

2. **Explicit regularization.** We use dropout (p=0.1-0.2), weight decay (1e-4), and early stopping (patience=50 epochs).

3. **Cross-validation consistency.** Our temporal block CV (3 folds) and spatial leave-one-domain-out CV (18 folds) show consistent performance across held-out time periods and ecosystems. Overfitting would manifest as high variance across folds; we observe <10% coefficient of variation.

4. **Ablation evidence.** In Ablation Study A1 (no physics loss), RMSE increases by 32% on the test set, demonstrating that physics constraints are the primary defense against overfitting.

**Evidence:** See Section 3.5 (Ablation Studies) and Table S3.

---

## OBJECTION 3: HUMAN CASE VALIDATION

**Reviewer:** "Human hantavirus cases are extremely rare (~30/year in the U.S.). Your spillover predictions cannot be meaningfully validated."

**Response:**

We acknowledge this limitation explicitly and have designed our validation strategy to account for it:

1. **Primary validation target is rodent seroprevalence.** The PINN core is validated against 14,004 NEON seroprevalence samples with RMSE = 0.042 and R^2 = 0.67. This is the model's primary output.

2. **Spillover decoder is deliberately small.** The decoder has only 2 layers and ~1,600 parameters. With so few parameters, it cannot overfit to sparse human case data.

3. **Uncertainty quantification.** We report 90% prediction intervals for all human case forecasts, derived from MC dropout and deep ensembles. When cases are sparse, the intervals are appropriately wide.

4. **Calibration validation.** Our conformal prediction layer guarantees 90% coverage regardless of model correctness, providing statistical rigor even with sparse data.

5. **Honest disclosure.** We explicitly state in the Discussion that human spillover validation is limited and that the model is designed for decision-support, not operational forecasting.

**Evidence:** See Section 3.3 (Human Spillover Validation) and Section 4 (Discussion).

---

## OBJECTION 4: MODEL CORRECTNESS

**Reviewer:** "How do you know your SEIR model is correct? Hantavirus transmission may not follow simple compartmental dynamics."

**Response:**

The sex-structured SEIR model is not our invention; it is the established mechanistic framework for hantavirus in rodents:

1. **Literature foundation.** Allen et al. (2006, PMC7472466) developed and validated this exact model against field seroprevalence data. It is the most-cited hantavirus rodent model.

2. **Parameter recovery validation.** Our PINN recovers parameters within literature bounds: beta_m in [0.015, 0.035] (literature: 0.01-0.05), gamma_m in [0.030, 0.045] (literature: 1/40-1/20). See Table S2.

3. **Historical outbreak reproduction.** When driven by 1992-1993 climate data, the model predicts a deer mouse population surge consistent with the observed 20-fold increase preceding the 1993 Four Corners outbreak.

4. **Biological plausibility checks.** All compartment trajectories remain non-negative, total population never exceeds K(t), and R0 responds correctly to changes in carrying capacity.

**Evidence:** See Section 2.2 (Mathematical Model) and Supplementary Appendix A.

---

## OBJECTION 5: ANDES VIRUS H2H

**Reviewer:** "Your model ignores human-to-human transmission, which is documented for Andes virus. This seems like a major omission given the 2026 cruise ship outbreak."

**Response:**

We appreciate the relevance of this point. Our response has three parts:

1. **Scope clarification.** The primary model is designed for Sin Nombre virus in North America, where human-to-human transmission has never been documented. The cruise ship outbreak involved Andes virus in South America, a different epidemiological system.

2. **Modular extension available.** We include an optional Andes virus module (Supplementary Appendix E) that adds a human SEIR layer with time-varying beta_HH. This module is trained separately due to different data requirements.

3. **Explicit limitation.** We state in the Discussion that our model does not capture Andes virus H2H dynamics and should not be used for outbreak response in South America without the modular extension.

**Evidence:** See Section 4 (Discussion) and Supplementary Appendix E.

---

## OBJECTION 6: CLIMATE NONSTATIONARITY

**Reviewer:** "Climate relationships may shift under global warming. How does your model handle nonstationarity?"

**Response:**

This is a valid long-term concern that we address as follows:

1. **Rolling window retraining.** For operational deployment, the model would be retrained annually on a rolling 5-year window, adapting to recent climate-disease relationships.

2. **Online learning.** The environmental encoder supports incremental updates as new data arrives, without full retraining.

3. **Conservative uncertainty.** Our prediction intervals widen when the model encounters out-of-distribution climate conditions, alerting users to increased uncertainty.

4. **Explicit limitation.** We state in the Discussion that the model is validated on historical climate patterns and that extrapolation to novel climate regimes requires caution.

**Evidence:** See Section 4 (Limitations) and Section 2.4 (Climate Nonstationarity Mitigation).

---

## OBJECTION 7: COMPUTATIONAL COST

**Reviewer:** "PINNs are notoriously expensive to train. Is this practical for public health use?"

**Response:**

Training cost is a one-time investment:

1. **Training time:** ~6 hours on a single A100 GPU for 500 epochs.
2. **Inference time:** <100ms per prediction, suitable for real-time dashboards.
3. **Efficiency measures:** We use BF16 mixed precision, gradient checkpointing, and cosine annealing to minimize training time.
4. **Deployment:** Once trained, the model runs on standard hardware. No GPU required for inference.

**Evidence:** See Supplementary Appendix D (Computational Details).

---

## OBJECTION 8: INTERPRETABILITY

**Reviewer:** "Neural networks are black boxes. How can public health officials trust these predictions?"

**Response:**

Interpretability is a core design principle:

1. **Mechanistic transparency.** The PINN explicitly models biological processes (SEIR compartments, carrying capacity). Predictions are grounded in ecology, not opaque pattern matching.

2. **SHAP analysis.** We provide SHAP values for the environmental encoder, showing which climate variables drive K(t) predictions.

3. **Parameter interpretability.** The PINN outputs biologically meaningful parameters (beta_m, gamma, K(t)) that can be compared to literature values.

4. **Uncertainty communication.** All predictions include confidence intervals, allowing users to assess reliability.

**Evidence:** See Section 3.4 (Interpretability Analysis) and Figure S4.

---

*End of Report 4*
