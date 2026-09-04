# Status of this deck

**This deck lags the manuscript as of 2026-09-04 and should not be presented
without a pass over the four items below.**

It was built against the paper as it stood on 2026-09-02. Its headline numbers
(68.1 % accuracy, 94.9 % on the most confident fifth, 77 to 79 % proposal
precision six months out) are unchanged and remain correct. What it does not
yet carry is the 2026-09-04 revision, and two of those changes affect what a
slide would claim:

1. **The channel's baseline.** The deck presents the channel without its
   no-model comparator. Proposing the cheaper route on every eligible flight
   is right only 44.9 % of the time; the model lifts that to 79.2 %. That lift
   is the strongest single number available and belongs on the channel slide.
2. **The best simple rule is 55.0 %, not 53.2 %,** because a rule scoring
   45.0 % scores 55.0 % inverted. Any slide claiming a fifteen-point margin
   over the best single-feature rule is wrong; it is thirteen.
3. **Model ageing** is three months of extra staleness confounded with four
   fewer months of training data, not "a year". The annual retraining
   recommendation has been withdrawn from the paper.
4. **Feature direction** is now reported: the model penalises attributed delay
   sharply and rewards planned fuel weakly. The second half is
   counter-intuitive and would need saying out loud rather than being left in
   a chart.

See `../README.md` for the full list of corrections and their evidence.
