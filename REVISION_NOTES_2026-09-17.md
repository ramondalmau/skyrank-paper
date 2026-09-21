# Clarity revision of both Skyrank manuscripts

Base commit: `9739cb26be8d637c2952892911b4467195b7dd16`.

The revision strengthens the explanation of the scientific contribution: learning route-choice predictions from recorded replacements, constructing inputs without direct filing-time clues, and evaluating the reliability of those predictions. The conference paper presents the method and its main evidence; the journal retains the detailed baselines, ablations, policy analysis and validity discussion.

## Main changes

- Explain revision pairs and stay pairs separately. A revision records two routes filed for the same flight; a stay pair uses a comparison route from another flight and its preference label is inferred.
- Define chosen/abandoned routes before using those labels. Distinguish the training label from the model's predicted choice.
- Explain context alignment and within-pair normalisation as different operations. Add an explicitly hypothetical encoding example to the conference paper and the normalisation equation to the journal.
- Explain tree scores, the pairwise loss, score gaps, probability calibration and threshold selection in order. Explain why a 0.600 threshold can target 80% precision.
- Distinguish ranking accuracy, prediction coverage, proposal precision and proposal coverage. State that the observations and denominators are route pairs, not necessarily distinct flights.
- Explain the policy's actual retrospective construction: it knows the two historically filed alternatives, withholds their order, and may select either the replacement or the abandoned route.
- Preserve the main quantitative results, while distinguishing planned-fuel differences on matching revisions from additional savings caused by proposals. Annualisations are scaling assumptions, not confidence intervals.
- Replace unsupported interpretations: calibration does not guarantee later precision; 10% stay-pair error is not a confident-rejection rate; three similar test months do not rule out model ageing; attribution does not establish causal airline preferences; a planned-fuel total is not a proven upper bound on savings.
- Preserve both titles, author blocks, all citation keys and the EUROCONTROL disclaimers. Remove named waypoint examples from the conference discussion and retain the existing neutral framing of the single-indicator baseline.
- Remove the journal's McNemar/p-value claims and report effect sizes directly. Existing uncertainty intervals remain.
- Restore the original conference workflow artwork unchanged at the author's request. Clarify its probability and confirmation labels in the caption and text. Keep all other included figures and the existing section structure.
- Update journal highlights to match this manuscript, removing the obsolete model-ageing claim. Record ChatGPT assistance in the journal's existing writing declaration.

## Second clarity pass

The author requested fuller explanations using the available conference space and restoration of the original workflow diagram. This pass expands the two-row training example, distinguishes zero-encoded indicators from zero physical quantities, explains why shared context can affect a comparison through interactions, and explains calibration fitting and freezing. It separates the subsets behind 94.9% selective ranking accuracy and 79.2% proposal precision, spells out the matched-only planned-fuel sum, and adds an illustrative attribution calculation. Parallel explanations are aligned in the journal. Table labels now distinguish regulation status from delay; a regulation can be attributed with zero delay. The original workflow image is byte-identical to the base commit. The replacement vector and its generator have been removed.

## Verification

Both sources compile with pdfLaTeX/BibTeX through latexmk: **8 conference pages and 33 journal pages**, with no overfull horizontal boxes, undefined references or unresolved `??` markers. The conference reports a 0.60-point vertical-box warning from balancing its final columns; visual inspection confirms that the content remains within the margins without overlap. The abstract counts are 217 and 177 words under the project's strict whitespace convention. Every citation key is preserved (12 conference, 25 journal), and both titles and disclaimers match the base commit exactly. The comment-trap scan reports no suspect sites. Rendered pages were inspected, and short paragraph endings were rephrased where practical without reducing font size or margins.

The reported numerical results were compared with the base manuscripts and repository review records. Removed numerical occurrences were repetitions, illustrative values or the deliberately removed significance tests. The conference encoding example and the 0.85/0.40 probability examples are explicitly hypothetical. This is an editorial and interpretation revision, **not a rerun or independent reproduction of the experiments**.

## Evidence limits and remaining author checks

The referenced study code, result JSONs, source tables and raw data are not present in this paper-only repository. Several historical runbook statements imply that they are available in a larger parent project; they cannot be used as evidence of availability here. The empirical results, precise calibration implementation and training-selection history therefore remain dependent on the original study artefacts and earlier audit records.

Two details merit checking against those artefacts before submission: the exact definition of the archived planned-fuel indicator (for example, trip versus block fuel), and whether policy totals are deduplicated across repeated revisions of the same flight. This revision consistently describes pair-based planned-fuel differences and does not supply an unverified definition or new aggregate.

The conference still uses the repository's IEEEtran drafting scaffold. Its eight-page count does not certify the official SID template. Transfer and check against that template before submission, as already required by `sid2026/COMPLIANCE.md`. Journal submission declarations and the companion conference paper's final publication status remain author checks. No paper has been submitted or merged by this revision.

## Build

With IEEEtran, elsarticle and their bibliography styles installed:

```bash
(cd sid2026 && latexmk -pdf -interaction=nonstopmode -halt-on-error sid2026.tex)
(cd trc-extension && latexmk -pdf -interaction=nonstopmode -halt-on-error trc2026.tex)
```

The existing historical review files are retained as records of earlier versions. Where their page counts, figure descriptions or disclosure wording conflict with this dated note and the current manuscripts, this revision note describes the delivered version.
