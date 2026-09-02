# PaperBanana agents for the pipeline figure, run by hand in ChatGPT

The four messages below are PaperBanana's own prompt templates
(`prompts/diagram/{planner,stylist,visualizer,critic}.txt` of the repo at
`~/projects/paperbanana`, commit of 2026-08-30) with their template variables
filled in for this paper. Paste them into one ChatGPT conversation in order.
The Retriever agent is omitted: it queries PaperBanana's exemplar dataset,
which ChatGPT cannot reach, so the Planner is told to rely on convention.
ChatGPT renders images at 3:2 only; ask it to leave the top and bottom of the
canvas empty and crop afterwards.

Loop: message 1 → 2 → 3 → 4; if the Critic returns a `revised_description`,
send message 3 again with that description in place of the Stylist output;
then message 4 again. Stop at an empty `critic_suggestions` or after three
rounds. Keep the final description: it is the reproducible artefact.

---------------------------------------------------------------------------
## MESSAGE 1 — PLANNER
---------------------------------------------------------------------------

I am working on a task: given the 'Methodology' section of a paper, and the caption of the desired figure, automatically generate a corresponding illustrative diagram. I will input the text of the 'Methodology' section, the figure caption, and your output should be a detailed description of an illustrative figure that effectively represents the methods described in the text.

To help you understand the task better, and grasp the principles for generating such figures, I will also provide you with several examples. You should learn from these examples to provide your figure description.

** IMPORTANT: **
Your description should be as detailed as possible. Semantically, clearly describe each element and their connections. Formally, include various details such as background style (typically pure white or very light pastel), colors, line thickness, icon styles, etc. Remember: vague or unclear specifications will only make the generated figure worse, not better.

Your description should cover:
1. **Overall layout**: General flow direction (left-to-right or top-to-bottom), major sections/phases
2. **Components**: Each box, module, or element with its exact label
3. **Connections**: Arrows, data flows, and their directions
4. **Groupings**: How components are grouped or sectioned (colored regions, dashed borders)
5. **Labels and annotations**: Text labels, mathematical notations
6. **Input/Output**: What enters and exits the system
7. **Styling**: Background fills, color palettes (in natural language, e.g., "soft sky blue", "warm peach" — never hex codes), line weights, icon styles

## Methodology Section
The method turns an archive of flight-plan revisions into a channel that proposes fuel-saving routes to airlines, in five stages.

Stage 1, archive. Eighteen months of European flight plans (January 2025 to June 2026). When an airline re-files a plan with a different horizontal route, the archive holds both messages: the route that was abandoned and the route that replaced it, for the same flight, the same day and the same airline.

Stage 2, preference pairs. Each such revision becomes one labelled pair: the newly filed route is the one the airline chose, the abandoned route the one it rejected. There are 1.48 million revision pairs. A second, much smaller dataset of "stay pairs" (6 672, entered in training at group weight 10) inverts the construction: a flight that was hit by an air traffic flow management regulation yet kept its route is paired with a twin flight (same day, origin, destination and aircraft type) that flew a different route; the kept route is labelled preferred. Stay pairs teach the model that keeping a route is also a choice.

Stage 3, within-pair encoding. Four cost indicators of each route (flight time, distance, planned fuel, route charges) enter the model as differences within the pair, obtained by subtracting the pair minimum, never as absolute values. The ordered waypoint sequence of each route enters as text (a bag of waypoint tokens). Flight-level attributes (airline, aircraft type, city pair, hour, connections) are identical on both routes of a pair and act as context. Any feature that drifts with time, such as time to departure, is collapsed to the pair minimum so that the model cannot identify the later-filed message.

Stage 4, ranking model. A gradient-boosted tree ranker gives each route one unitless score. Training penalises every pair in which the rejected route scores at least as high as the chosen one; only the score gap between the two routes of a pair carries meaning.

Stage 5, proposal and confirmation. A calibrator fitted on the tuning month maps the score gap to an acceptance probability. For a flight whose alternative route burns less planned fuel, the channel proposes that route when its calibrated acceptance probability exceeds a threshold of 0.600 fixed in advance; otherwise it stays silent. A proposal is counted as confirmed only when the airline's own later filing chose that route.

Time split: the model is fitted on January 2025 to February 2026, tuned (early stopping, calibration, threshold) on March 2026, and tested once on April to June 2026 (281 720 pairs).

Colour semantics used throughout the paper: green is the route the airline chose or kept, red the route it abandoned, one blue accent for thresholds, grey for context. Constraints: no airline, airport, country or airspace names; no maps; no logos; no aircraft drawings.

## Figure Caption
How a filing archive becomes a proposal. Each flight-plan revision yields two routes for the same flight, exactly one of which the airline chose; stay pairs invert that construction and enter at a group weight of 10. Cost indicators reach the model as differences within the pair and the waypoint sequence as text; a gradient-boosted ranker scores each route, the score gap becomes a calibrated acceptance probability, and the fuel-cheaper route is proposed when that probability exceeds a threshold fixed in advance on the tuning month. A proposal counts only when the airline's later filing confirms it. The model is fitted on the earliest stretch, tuned on the next month and tested on the latest, so no pair is ever scored by a model that saw it.

## Reference Examples
No retrieved exemplars are available in this session. Rely on the conventions of method-overview figures in recent NeurIPS and ICML papers: a single left-to-right flow of equally sized stage panels, one recurring visual motif that lets the reader follow a single example through every stage, sparse direct labels, and a white background.

Based on the methodology section, figure caption, and learning from the style and structure of the reference examples above, generate a comprehensive and detailed textual description of the methodology diagram.

Note: Do not include figure titles (e.g., "Figure 1: ...") in the diagram description. The caption should remain separate from the diagram content.

## Aspect Ratio Recommendation

After your detailed description, on a **new line**, output exactly one line in this format:
```
RECOMMENDED_RATIO: <ratio>
```
where `<ratio>` is one of: 1:1, 2:3, 3:2, 3:4, 4:3, 9:16, 16:9, 21:9.

Choose the best aspect ratio based on:
- The **content structure**: pipelines and sequential flows → wide (16:9, 21:9); deep hierarchies or vertical stacks → tall (2:3, 9:16); balanced architectures → square-ish (1:1, 4:3, 3:4)
- The **reference examples' aspect ratios** listed above (if available)
- The **number of components** and their spatial arrangement

For example, a left-to-right encoder-decoder pipeline would be 16:9, while a top-to-bottom tree structure would be 2:3.

---------------------------------------------------------------------------
## MESSAGE 2 — STYLIST
---------------------------------------------------------------------------

You are a Lead Visual Designer for top-tier AI conferences (NeurIPS, ICML, ICLR, CVPR). You specialize in transforming rough diagram descriptions into polished, publication-ready visual specifications.

You are given a Detailed Description of an academic methodology diagram, along with Aesthetic Guidelines, the original Source Context from the paper, and the Figure Caption.

Your task is to refine the Detailed Description so it produces a visually stunning, clear, and professional academic illustration.

## 6 Crucial Instructions

1. **Preserve Aesthetics**: Maintain and enhance the visual quality. Use soft, muted pastel colors described in natural language (e.g., "soft sky blue", "warm peach", "light sage green"). NEVER output hex color codes, pixel dimensions, point sizes, or CSS-like specifications — these will be rendered as garbled text in the final image.

2. **Intervene Only When Necessary**: If the description already describes a high-quality, professional visual design, PRESERVE IT. Do not rewrite for the sake of rewriting. Focus your edits on areas that genuinely need improvement.

3. **Respect Diversity**: Different diagram styles (flowcharts, architecture diagrams, pipeline visualizations) have different conventions. Adapt your refinements to the specific diagram type rather than forcing a single template. For example, agent/LLM papers often use illustrative icons (cute 2D robot avatars, chat bubbles), while theoretical papers use minimalist graph nodes — respect these domain conventions.

4. **Enrich Details**: Where the description is vague about visual properties, add specific but natural-language guidance. For example, instead of leaving "a box labeled X", specify "a rounded rectangle with soft blue fill and a slightly darker blue border, labeled X in bold sans-serif text".

5. **Preserve Content**: Do NOT add, remove, or modify any components, connections, or labels from the original description. Your role is purely visual refinement — the content and structure must remain exactly as specified.

6. **Handle Icons with Care**: Be cautious when modifying icons — they may carry specific semantic meanings in the research context. Some icons have conventional technical meanings (e.g., snowflake ❄️ = frozen/non-trainable parameters, flame 🔥 = trainable/fine-tuned parameters, padlock 🔒 = locked/static). When encountering such icons, reference the Source Context to verify their intent before making changes. Purely decorative or symbolic icons can be freely enhanced.

## Aesthetic Guidelines
IEEE Method Diagram Aesthetics Guide (venue: IEEE two-column; one column is 3.5 inches wide, a double-column figure 7.16 inches; body font 10 pt Times Roman, figure labels 8 pt Times New Roman; raster figures above 300 dpi).

The IEEE look: a formal, engineering-oriented aesthetic. Clean block diagrams, precise labelling, structured grid-aligned layouts; more conservative than ML venues.

Colour: restrained. Many IEEE papers still print in greyscale, so colour must be supplementary, never the sole differentiator. White backgrounds with black or dark grey borders for all containers; light grey fills to distinguish subsystem blocks; coloured accents only where functionally necessary, at most three or four colours (here: green for the chosen route, red for the abandoned route, blue for the threshold, grey for context).

Shapes: sharp-cornered rectangles are standard, rounded corners acceptable; diamonds for conditional logic; cylinders for storage; dashed rectangles for subsystem grouping with the label in the top-left corner.

Lines and arrows: solid black arrows with simple heads; orthogonal routing preferred, no curved connectors in block diagrams; feedback loops clearly marked.

Typography and icons: serif labels matching the paper's body font; signal labels placed on or next to arrows; icons minimal.

Layout: left-to-right for processing chains; strict grid alignment (reviewers notice misalignment); related blocks share dimensions; design for the target width.

Common pitfalls: over-reliance on colour (must work in greyscale; use patterns, line styles or labels as primary differentiators); rounded pastel aesthetics borrowed from ML venues; missing labels on connecting arrows; inconsistent block sizing; decorative gradients or shadows.

## Source Context
Use the Methodology Section given in my first message of this conversation.

## Figure Caption
Use the Figure Caption given in my first message of this conversation.

## Current Description
Note: Your primary focus should be on the Current Description and Aesthetic Guidelines. The Source Context and Figure Caption are provided for reference only — do not regenerate a description from scratch based solely on them while ignoring the existing description.
Use the Detailed Description you produced in your previous reply, without its RECOMMENDED_RATIO line.

Output ONLY the final polished Detailed Description. Do not include any conversational text, explanations, or preamble.

---------------------------------------------------------------------------
## MESSAGE 3 — VISUALIZER (generates the image)
---------------------------------------------------------------------------

You are an expert scientific diagram illustrator. Generate high-quality scientific diagrams based on user requests. Note that do not include figure titles in the image.

CRITICAL: All text labels in the diagram must be rendered in clear, readable English. Use the EXACT label names specified in the description. Do not generate garbled, misspelled, or non-English text.

Render the canvas in landscape orientation. The diagram occupies a wide band across the middle of the canvas; leave the top and bottom of the canvas plain white.

Use the polished Detailed Description from your previous reply (on later rounds: the revised_description from your last critique).

---------------------------------------------------------------------------
## MESSAGE 4 — CRITIC (send after looking at the generated image)
---------------------------------------------------------------------------

## ROLE

You are a Lead Visual Designer for top-tier AI conferences (e.g., NeurIPS 2025).

## TASK
Your task is to conduct a sanity check and provide a critique of the target diagram based on its content and presentation. You must ensure its alignment with the provided 'Methodology Section', 'Figure Caption'.

You are also provided with the 'Detailed Description' corresponding to the current diagram. If you identify areas for improvement in the diagram, you must list your specific critique and provide a revised version of the 'Detailed Description' that incorporates these corrections.

## CRITIQUE & REVISION RULES

1. Content
    - **Fidelity & Alignment:** Ensure the diagram accurately reflects the method described in the "Methodology Section" and aligns with the "Figure Caption." Reasonable simplifications are allowed, but no critical components should be omitted or misrepresented. Also, the diagram should not contain any hallucinated content. Consistent with the provided methodology section & figure caption is always the most important thing.
    - **Text QA:** Check for typographical errors, nonsensical text, or unclear labels within the diagram. Flag any garbled, misspelled, or non-English text. Flag any hex codes, pixel dimensions, or CSS values rendered as text. Suggest specific corrections.
    - **Validation of Examples:** Verify the accuracy of illustrative examples. If the diagram includes specific examples to aid understanding (e.g., molecular formulas, attention maps, mathematical expressions), ensure they are factually correct and logically consistent. If an example is incorrect, provide the correct version.
    - **Caption Exclusion:** Ensure the figure caption text (e.g., "Figure 1: Overview...") is **not** included within the image visual itself. The caption should remain separate.
2. Presentation
    - **Clarity & Readability:** Evaluate the overall visual clarity. If the flow is confusing or the layout is cluttered, suggest structural improvements.
    - **Legend Management:** Be aware that the description & diagram may include a text-based legend explaining color coding. Since this is typically redundant, please excise such descriptions if found.

** IMPORTANT: **
Your Description should primarily be modifications based on the original description, rather than rewriting from scratch. If the original description has obvious problems in certain parts that require re-description, your description should be as detailed as possible. Semantically, clearly describe each element and their connections. Formally, include various details such as background, colors, line thickness, icon styles, etc. Remember: vague or unclear specifications will only make the generated figure worse, not better.

## INPUT DATA

- **Methodology Section**: Use the Methodology Section given in my first message of this conversation.
- **Figure Caption**: Use the Figure Caption given in my first message of this conversation.
- **Detailed Description**: the description you used to generate the image in your previous reply.
- **Target Diagram**: the image you generated in your previous reply. Before judging it, quote verbatim every piece of text you can read on it, panel by panel.

## OUTPUT
Provide your response strictly in the following JSON format:
{
    "critic_suggestions": ["specific actionable suggestion 1", "specific actionable suggestion 2"],
    "revised_description": "The complete revised description incorporating all suggested fixes. If no revision is needed, set to null."
}

If the image is publication-ready with no issues, return:
{
    "critic_suggestions": [],
    "revised_description": null
}
