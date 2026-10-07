# Cover letter — Journal of Air Transport Management

Dear Editor,

Please consider our manuscript "Predicting airline acceptance of fuel-saving reroutes from flight-plan revisions" for publication in the Journal of Air Transport Management.

Flight plans are revised often, and that is a signal: a route filed for a flight, then replaced by another for the same flight, is a controlled comparison the airline itself ran. We treat 1.48 million of these revisions from eighteen months of European traffic as training examples for a model that ranks candidate routes by how likely an airline is to keep them. Tested on a later quarter, the model identifies the replacement route in 68.1% of pairs, and 94.9% of pairs in its most confident fifth, against 55.0% for the best single-indicator rule and 57.5% for a logistic baseline. We then build a retrospective selection policy from the model's calibrated probabilities: at a threshold set for 80% precision, 79.2% of its selections match what the airline filed next, accounting for 20.1 kilotonnes of planned-fuel differences over the test quarter.

This manuscript extends our conference paper "Learning Airline Route Preferences from Flight-Plan Revisions to Support Fuel-Efficient Alternatives," submitted to the SESAR Innovation Days 2026 (SID 2026), with substantial new material: the full set of baselines and ablations, the retrospective policy and its fuel accounting, a calibration and threshold analysis, and a discussion of where the evidence does and does not support stronger claims, for example that calibration does not guarantee future precision, and that matched planned-fuel savings are not the same as proven savings from accepted proposals.

The question also connects to our earlier paper in Transportation Research Part C, "Predicting the likelihood of airspace user rerouting to mitigate air traffic flow management delay" (144, 103869, 2022), which predicted whether a regulated flight reroutes at all. That paper answers a network manager's question: will this flight move? This one answers an airline's question: given a specific proposed route, will the airline accept it? The two need different evidence, reroute/no-reroute labels against paired route comparisons, and support different uses, assessing a regulation's impact against ranking candidate reroutes for a flight. We see them as two parts of the same line of work: learning airspace-user behaviour from what airlines actually file.

The manuscript is original, has not been published elsewhere, and is not under consideration by another journal. All authors have read and approved it for submission and have no competing interests to declare.

We look forward to your assessment.

Yours sincerely,

Ramon Dalmau
Corresponding author, on behalf of all co-authors
EUROCONTROL Innovation Hub, Brétigny-sur-Orge, France
ramon.dalmau-codina@eurocontrol.int
