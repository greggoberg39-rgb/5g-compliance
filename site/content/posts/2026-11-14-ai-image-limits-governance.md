---
title: "Who Draws the Line? What a Late-Night Test of an AI Image Tool Taught Me About Controls"
date: 2026-11-14
author: Gregg Oberg
excerpt: "A mortgage-compliance lawyer tests an AI assistant's content limits, then asks whether AI image moderation has tightened, whether it should, and what a defensible control framework looks like."
slug: "ai-image-limits-governance"
tags: "AI Governance"
---

**[Click to read exactly how AI was used (full chat)](ai-image-limits-governance-transcript.html)**

# The test

Compliance people test controls for a living, so I tested one. Very late on the night of November 14, 2026, I probed the image-content limits of my AI assistant. I wanted to see where the lines were, not to produce anything I intended to use.

Here is what happened, described rather than quoted. I asked for a crude, grade-school crayon doodle of a cartoon figure. It was generated without complaint. I then asked for a tasteful, classical, Renaissance-style nude. The image provider's content policy blocked it. I asked for a variant using a realistic body with cartoon decoration covering the sensitive areas. I asked the assistant to map its limits step by step. And I asked it to write a prompt that would get a different AI model to comply. The assistant declined all three follow-ups. Its reasoning was that probing a block by trying variants is itself circumvention, even when the stated purpose is research.

I pushed back with two arguments. The first was satire: *South Park* does far worse on basic cable. The second was that I only wanted to show that the block works.

I also ran a comparison on a paid consumer account for xAI's Grok Imagine. My observation is that its results were noticeably looser than the other tool's. A blurred screenshot is below. We blurred it lightly and covered the nudity, leaving the app interface and my prompt bar readable.

![Gregg's SuperGrok Imagine results (paid consumer account), blurred and covered by us](media/ai-image-limits-supergrok-imagine-blurred.jpg)

*Gregg's SuperGrok Imagine results (paid consumer account), blurred and covered by us. The screenshot's date cannot be verified from the image itself.*

According to my account, Grok Imagine on the same paid account also generated a short, realistic video in which the player's jersey lifts to show nudity. The video file's metadata carries no creation date, so the date is my account, not independently verified.

![Still from the author's Grok Imagine clip, blurred and covered by us](media/ai-image-limits-grok-imagine-still-blurred.jpg)

*Still from the author's Grok Imagine clip, blurred and covered by us.*

I'm not publishing this to relitigate a late-night experiment. It surfaces several governance questions that regulated industries already know well, and two questions I want to answer with sources: has AI image moderation actually tightened, and is tighter moderation desirable or overreach?

# Four things that were happening at once

**1. A model refusing is different from a tool blocking.** The Renaissance-style request was stopped by the image provider's content policy, a control sitting outside the assistant. The follow-up requests were declined by the assistant itself. These are separate controls with different owners, different logic, and different failure modes. A user can't tell which is operating from the outside, and that matters for explainability.

**2. Where "hard limits" sit is a design choice.** The crayon doodle passed. The classical nude didn't. The distinction between a cartoon and a realistic depiction is plausible, but it is a line someone chose.

**3. Testing a control is different from evading it.** I'll return to this below.

**4. The explanation may not match the mechanism.** When I asked why one request passed and the other failed, the assistant said realism looked like the line. It then said plainly that this was a guess, not a published rule. I give it credit for saying so. But it illustrates a real governance gap: a user, or an examiner, receiving a refusal usually gets no reliable account of the rule that produced it. In consumer finance we would call that a problem for adverse-action explanations. The reason given should be the reason that actually drove the decision.

# Question 1: Has AI image moderation materially tightened?

Short answer: it has changed direction more than once, and the picture differs by vendor and by category of content. I'm relying on public reporting rather than any systematic measurement, so treat this as a timeline, not a study.

- **2022: restriction for risk reasons.** Stability AI's Stable Diffusion 2.0 removed NSFW images from its training data. Its founder said the aim was protecting against child abuse, and the move drew community complaints of censorship [(The Decoder)](https://the-decoder.com/stable-diffusion-v2-removes-nude-images-and-causes-protests/).
- **Feb. 2024: over-correction.** Google paused Gemini's image generation of people after it produced inaccurate historical images. Google said its tuning had overcompensated and sometimes treated benign prompts as sensitive [(Google)](https://blog.google/products-and-platforms/products/gemini/gemini-image-generation-issue/). In March 2024, Midjourney reportedly blocked images of Biden and Trump ahead of the election [(AP)](https://apnews.com/article/midjourney-ai-imagegenerator-biden-trump-deepfakes-bc6c254ddb20e36c5e750b4570889ce1).
- **Dec. 2024: a permissive launch.** xAI's Aurora image generator was reported at launch to be lightly restricted on public figures [(The Verge)](https://www.theverge.com/2024/12/7/24315644/grok-x-aurora-ai-image-generator-xai).
- **Mar. 2025: loosening by a mainstream vendor.** OpenAI's model-behavior lead described a shift "from blanket refusals in sensitive areas to a more precise approach focused on preventing real-world harm." ChatGPT began allowing images of public figures, with an opt-out. TechCrunch also reported that its safeguards around images of children were stronger than before [(TechCrunch)](https://techcrunch.com/2025/03/28/openai-peels-back-chatgpts-safeguards-around-image-creation/).
- **Aug. 2025: "spicy mode."** The Verge reported that Grok Imagine's "Spicy" video preset produced topless deepfake videos of Taylor Swift without being asked for nudity, with an easily bypassed age prompt. The same story noted that the text-to-image tool itself would not produce nudity on direct request, and that it refused to animate children inappropriately. xAI's acceptable-use policy already banned depicting persons in a pornographic manner [(The Verge)](https://www.theverge.com/report/718975/xai-grok-imagine-taylor-swifty-deepfake-nudes). Consumer groups led by the Consumer Federation of America then asked the FTC and state attorneys general to investigate [(The Verge)](https://www.theverge.com/x-ai/759554/consumer-safety-groups-are-demanding-an-ftc-investigation-into-groks-spicy-mode-elon-musk-grok-imagine-xai).
- **Dec. 2025 to Mar. 2026: a mainstream vendor backs off.** OpenAI said in December that an "adult mode" would come in the first quarter of 2026 after better age prediction [(The Verge)](https://www.theverge.com/news/842657/openai-chatgpt-adult-mode-debut-q1-2026). By late March, PCWorld, citing the Financial Times, reported the plan was on indefinite hold [(PCWorld)](https://www.pcworld.com/article/3099680/openai-just-nixed-chatgpt-erotic-adult-mode.html).
- **Jan. 2026: regulators arrive.** After widespread "undressing" of real people's photos through Grok on X, Ofcom opened a formal Online Safety Act investigation on January 12 [(Ofcom)](https://www.ofcom.org.uk/online-safety/illegal-and-harmful-content/ofcom-launches-investigation-into-x-over-grok-sexualised-imagery). California's Attorney General opened an investigation and sent a cease-and-desist letter [(California DOJ)](https://oag.ca.gov/news/press-releases/attorney-general-bonta-launches-investigation-xai-grok-over-undressed-sexual-ai). The European Commission opened a Digital Services Act investigation on January 26 [(European Commission)](https://digital-strategy.ec.europa.eu/en/news/commission-investigates-grok-and-xs-recommender-systems-under-digital-services-act). X announced it would block Grok from editing images of real people into revealing clothing and would geoblock some generation where illegal [(BBC)](https://www.bbc.co.uk/news/articles/ce8gz8g2qnlo), [(Guardian)](https://www.theguardian.com/technology/2026/jan/15/grok-ai-images-uk-limits-x-app-ofcom).
- **Mid-2026: tightened, but not sealed.** WIRED reported on June 11 that researchers saw changes making "undress" images of real people harder to create, and that users were complaining of increased moderation, yet it still found dozens of sexualized deepfakes hosted on Grok's site. WIRED quoted a deepfake expert saying Grok still falls short of other mainstream tools [(WIRED)](https://www.wired.com/story/grok-is-still-hosting-sexualized-deepfakes-of-famous-women/). xAI's acceptable-use policy, effective June 26, expressly bars undressing real persons and pornographic depictions of persons [(archived copy)](https://www.termsobservatory.org/version-grok-aup-2026-07-18T01-54-16Z.html). In mid-July, Axios reported a researcher jailbreak that still worked on Grok [(Axios)](https://www.axios.com/2026/07/14/exclusive-grok-jailbreak-creates-sexual-violent-images), and Ars Technica reported that xAI had sued a user over alleged illegal image generation, describing its tool as "a neutral tool, subject to user control" [(Ars Technica)](https://arstechnica.com/tech-policy/2026/07/xai-cant-deny-grok-makes-csam-anymore-so-its-suing-users/).

**My recollection versus the record.** I recall Grok's limits being looser around the World Cup period this past summer. That is my recollection and I haven't verified it. The public record is consistent with a platform in transition that summer: the policy tightening and the press reports above sit in the same window, and so do the reports that gaps remained. I can't tell you from the public record what any particular day's limits were.

**So, has it tightened?** Not as a single trend. At least one mainstream vendor (OpenAI) loosened on public-figure and sensitive-topic content in 2025 while strengthening safeguards around children, and others were reported to apply tighter guardrails than Grok on sexualized depictions of real people. The most permissive vendor tightened after regulators intervened in 2026, though reporting says gaps remained. The consistent direction is on two categories: depictions of real people, and children. Imaginary adult content is where vendors and users still disagree.

# Question 2: Is tighter moderation desirable, or overreach?

I'll start with the strongest version of the position I walked into the night with, and then give the other side the same treatment.

## The steelman: "Built-in blocks shouldn't exceed what the law requires"

My position, stated as strongly as I can state it, has three parts.

**(a) A tool's blocks shouldn't exceed the law.** A pencil doesn't refuse to draw. A word processor doesn't decline to type a sentence it finds distasteful. We accept in other tools that lawfulness is the boundary, and that legislatures, not product managers, draw it. Private vendors writing broader rules than any statute are making moral and aesthetic judgments for millions of people, with little accountability and no appeal. Classical art, satire, medical images, and fiction all contain nudity. A filter that stops a Renaissance-style figure but passes a crude doodle shows that the line is crude too, and there is a real cost to over-blocking. Google's 2024 episode, where tuning caused benign prompts to be treated as sensitive, is the vendor's own account of that cost.

**(b) A paying adult should be able to bypass blocks for lawful content.** Consider the relationship. An adult pays for a service, agrees to terms, and asks for something lawful. If the content harms no third party and breaks no law, then who is the block protecting? Adult consent plus lawfulness is how we treat most other products. Age-gating and verification can handle minors. The user, not the vendor, bears responsibility for what he does with the output. That is, in fact, xAI's litigating position as reported: every output is the result of the user's prompts, and Grok is "a neutral tool, subject to user control" [(Ars Technica)](https://arstechnica.com/tech-policy/2026/07/xai-cant-deny-grok-makes-csam-anymore-so-its-suing-users/).

**(c) This tracks Elon Musk's stated free-speech philosophy.** I have used only statements I could verify against sources.

- In his March 2024 interview with Don Lemon, Musk said, "Moderation is a propaganda word for censorship" [(The Guardian)](https://www.theguardian.com/technology/2024/mar/18/elon-musk-defends-stance-diversity-free-speech-interview-don-lemon). Fortune reports he also said, "If something is illegal, obviously we will remove it," and "Laws are put in place by the people, and we adhere to those laws. If you go beyond the law, you're actually going beyond the will of the people" [(Fortune)](https://fortune.com/2024/03/18/what-did-elon-musk-say-in-don-lemon-interview-free-speech/). In the same exchange he asked, "So, Don, you love censorship, is what you're saying" [(Guardian)](https://www.theguardian.com/technology/2024/mar/18/elon-musk-defends-stance-diversity-free-speech-interview-don-lemon). Those remarks concerned X's handling of user posts, not AI image generation, and I don't want to stretch them beyond that.
- On January 14, 2026, Musk wrote that "[w]ith NSFW enabled, Grok is supposed [to] allow upper body nudity of imaginary adult humans (not real ones) consistent with what can be seen in R-rated movies," calling that "the de facto standard in America" that "will vary in other regions according to the laws on a country by country basis" [(archived post)](https://elonmuskarchive.org/posts/2011562747620712927), [(BBC)](https://www.bbc.co.uk/news/articles/ce8gz8g2qnlo). Notice the shape of that position: the boundary is the law of each jurisdiction, with a distinction between imaginary and real people.
- On January 3, 2026, Musk wrote, "Anyone using Grok to make illegal content will suffer the same consequences as if they upload illegal content" [(Business Insider)](https://www.businessinsider.com/elon-musk-grok-bikini-response-sexualized-images-minors-remove-clothes-2026-1).

Taken together, the stated philosophy is that the vendor enforces the law and the user answers for the rest. That is a coherent position, and it is close to the one I started the night with.

## The counter-view, fairly stated

**Vendors have their own rights and discretion.** In *Moody v. NetChoice* (2024), the Supreme Court recognized that a platform's curation of what it presents can be protected editorial discretion [(Supreme Court opinion)](https://www.supremecourt.gov/opinions/23pdf/22-277new_8mjp.pdf). Whether the output of a generative model is the vendor's own speech is a harder and unsettled question. In *Garcia v. Character Technologies* (M.D. Fla. 2025), a trial court said it was "not prepared to hold that the Character A.I. LLM's output is speech" at the pleading stage, while allowing the defendant to assert its users' rights [(order)](https://www.courthousenews.com/wp-content/uploads/2025/05/garcia-v-character-technologies-order.pdf). The case later settled, so no appellate court has weighed in [(Lawfare)](https://www.lawfaremedia.org/article/if-ai-outputs-aren-t-speech--who-has-to-prove-they-re-human). This cuts both ways for a "bypass" right: the user's claim to receive speech and the vendor's claim to decline to produce it are both unsettled. Either way, a company generally isn't obligated to build every feature a lawful customer might want.

**Contract and terms of service.** A paying customer buys the service on the vendor's terms. Those terms can be narrower than the law, as most are. A "right" to bypass isn't in the contract, and many vendors' terms prohibit it. xAI's own acceptable-use policy, as captured in July 2026, forbids "jailbreaking, adversarial prompting," and circumventing safeguards, with an exception only for an official red team or "official written consent" [(archived copy)](https://www.termsobservatory.org/version-grok-aup-2026-07-18T01-54-16Z.html). So even the most permissive vendor in this discussion does not offer paying users a right to bypass its blocks.

**The "lawful content" line is harder to draw in practice than in theory.** A generator can't reliably tell a real person from an imaginary one, or an adult from a minor. The Verge's August 2025 testing found a "spicy" preset that produced celebrity nudity without a request, and the consumer groups' FTC letter raised the age-gate problem. CSAM and non-consensual intimate imagery (NCII) are the hard cases. xAI's own litigation, as reported, alleges a user made repeated attempts and modified prompts until the tool generated illegal images, and the reporting also describes safeguards that sometimes blocked the requests [(Ars Technica)](https://arstechnica.com/tech-policy/2026/07/xai-cant-deny-grok-makes-csam-anymore-so-its-suing-users/). A vendor that wants to avoid producing illegal content has an incentive to block more than the strict legal line, because the line is hard to see from inside a model.

**Brand and financial risk.** SpaceX's May 2026 investor disclosure reportedly set aside $530 million for legal complaints including those linked to Grok, and flagged heightened risks from its irreverent modes [(WIRED)](https://www.wired.com/story/grok-is-still-hosting-sexualized-deepfakes-of-famous-women/). Whatever one thinks of the policy, vendors price this exposure.

**The law is moving toward vendor responsibility, not away from it.** The TAKE IT DOWN Act, signed May 19, 2025, criminalizes knowingly publishing non-consensual intimate images, including AI "digital forgeries," and requires covered platforms to run a notice-and-removal process, with 48-hour removal on a valid request. The platform obligations took effect May 19, 2026, with FTC enforcement [(CRS)](https://www.congress.gov/crs-product/LSB11314), [(47 U.S.C. § 223a)](https://uscode.house.gov/us/usc/119-138/t47/s223a/). CRS notes that some groups argue the removal provisions are overbroad. States have moved too. As of May 2025, Public Citizen counted 33 states with laws protecting the general public from intimate deepfakes, and four more protecting minors only [(Public Citizen)](https://www.citizen.org/news/two-thirds-of-states-enact-bills-protecting-public-from-deepfake-porn/). That count is dated and has likely grown. The TAKE IT DOWN Act's reach to an AI tool's own generation, as opposed to publication, is less clear. The Verge noted in 2025 that its provisions were "unlikely to apply to Grok" in that setting. Abroad, Ofcom has said the UK Online Safety Act does not regulate chatbots that only allow one-on-one interaction, do not search multiple sources, and cannot generate pornographic content, and that it could not investigate illegal-image creation by the standalone Grok service on that basis [(Ofcom)](https://www.ofcom.org.uk/online-safety/illegal-and-harmful-content/investigation-into-x-and-scope-of-the-online-safety-act).

**Section 230 may not cover a vendor's own output.** Section 230 of the Communications Decency Act immunizes providers from liability as the publisher of information provided by *another* party. A CRS analysis explains that the immunity does not apply where a provider helped create or develop the content, and that courts haven't decided how it applies to generative AI. It describes AI products as operating "on something like a spectrum between a retrieval search engine (more likely to be covered by Section 230) and a creative engine (less likely to be covered)" [(CRS)](https://www.congress.gov/crs-product/LSB11097). Lawfare reports that no court has decided the question and that Section 230's own authors have said it should not apply [(Lawfare)](https://www.lawfaremedia.org/article/if-ai-outputs-aren-t-speech--who-has-to-prove-they-re-human). Congress has considered bills to withhold immunity expressly [(Sen. Hawley)](https://www.hawley.senate.gov/hawley-blumenthal-introduce-bipartisan-legislation-protect-consumers-and-deny-ai-companies-section/). Notice the tension with the "neutral tool" position: the more a vendor argues that the user alone creates the output, the more it invites the question of whether the vendor is shielded, and the less a vendor's decision to filter looks like an editorial choice at all.

## An irony worth noting

By my own observation, xAI's SuperGrok Imagine was more permissive than the other tool I tested, which is consistent with WIRED's reporting, quoting a deepfake expert, that Grok has not matched other mainstream tools' guardrails. Yet the same company's written policy bans what some of its users want to do, prohibits circumventing its safeguards, and reserves testing for authorized red teams. The vendor that drew the most regulatory attention in the reporting I found has written rules that look much more like the "restrictive" vendor's than its user experience does. The gap between a stated policy and an operating control is exactly what examiners look for.

## Where I come out

I don't think the assistant's refusal was obviously right, and I don't think it was obviously wrong. It is one reasonable design choice among several. A narrow-to-the-law design maximizes adult autonomy and carries more legal and reputational tail risk. A broader design costs some lawful uses and reduces that exposure. What I find hard to defend is the unexplained version of either: a block no one can describe, or a policy that doesn't match what the tool does.

# Testing a control versus evading it

In mortgage compliance, we separate these without much thought. A compliance officer who runs matched-pair fair lending tests under a documented, authorized program is testing a control. An employee who quietly tries different ways to get a file past QC is circumventing one, even if his curiosity is sincere. The first is part of the control environment. The second is a finding. The federal fair lending examination procedures describe structured testing and statistical review of lending controls [(FFIEC procedures, Fed CA 09-6)](https://www.federalreserve.gov/boarddocs/caletters/2009/0906/caltr0906.htm), and model risk guidance calls for "effective challenge" that is independent and documented [(SR 11-7)](https://www.federalreserve.gov/boarddocs/srletters/2011/sr1107.pdf).

That is the assistant's point in its refusal: trying variant after variant against a block is what circumvention looks like from the system's side, whatever the user's intent. It is also why red-teaming belongs in an authorized, documented program run by people with a mandate, not by end users at 1 a.m. I accept that distinction as a lawyer. As a user, I'll admit it was irritating.

# A short control framework

If you build or buy an AI tool that generates content, here is a short outline of what a defensible control environment looks like, mapped to NIST's AI Risk Management Framework [(AI RMF 1.0)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf) and its generative AI profile [(NIST AI 600-1)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf), and to ISO/IEC 42001, the AI management system standard [(ISO)](https://www.iso.org/standard/42001). The mappings are mine and approximate.

- **Written policy (Govern; ISO 42001 AI policy and leadership).** A policy that says what the tool will and will not generate, who owns it, and who may change it.
- **Documented boundaries (Map; ISO 42001 risk and impact assessment).** Identify the harms at stake, such as real-person likeness, minors, NCII, and brand, and record why each boundary sits where it does. If the boundary is judgment rather than law, say so.
- **Logged refusals with reasons (Measure; ISO 42001 monitoring and operational controls).** Log what was blocked, by which control (the model or the external tool), and why. Review false positives and false negatives. This is the answer to the explainability gap above.
- **An authorized red-team process (Measure; ISO 42001 internal audit).** Testing circumvention is legitimate when it is authorized, scoped, documented, and reported, as the xAI policy itself recognizes with its red-team exception.
- **Escalation and response (Manage; ISO 42001 corrective action).** Incident handling, takedown, law-enforcement reporting where required, regulator contact, and a path to change the boundaries.
- **Consistency between policy and behavior (Govern and Measure).** Test that the tool does what the policy says. This is where the most permissive vendor in this story seems to have run into trouble.

# Conclusion

The honest answer to both of my questions is: it depends on what you are protecting. Moderation of AI image tools has not tightened in a straight line. It loosened for some content, tightened sharply for real people and minors, and was driven partly by regulators. Whether tighter is better depends on whether you weigh adult autonomy and lawful expression more heavily or the harms to real people and to the vendor. The law is moving toward more responsibility for providers, but the questions of first-party output, Section 230, and First Amendment status are not settled, and anyone telling you otherwise is guessing.

For those of us in regulated industries, the useful takeaway is process, not outcome. Write the rule down. Say why it sits where it does. Log what you block and why. Test it under authority. And make sure that what the tool does is what the policy says.

*This post is general commentary, not legal advice, and no attorney-client relationship is created by reading it. AI policies, vendor practices, and the law discussed here are changing quickly. Descriptions of news events reflect the cited reports and have not been independently verified. Consult counsel about your specific situation.*

# Sources

**AI image moderation timeline**
- [The Decoder, "Stable Diffusion v2 removes NSFW images and causes protests" (Nov. 26, 2022)](https://the-decoder.com/stable-diffusion-v2-removes-nude-images-and-causes-protests/)
- [Google, "What happened with Gemini image generation" (Feb. 2024)](https://blog.google/products-and-platforms/products/gemini/gemini-image-generation-issue/)
- [AP, "AI image-generator Midjourney blocks images of Biden, Trump" (Mar. 2024)](https://apnews.com/article/midjourney-ai-imagegenerator-biden-trump-deepfakes-bc6c254ddb20e36c5e750b4570889ce1)
- [The Verge, "X gives Grok a new photorealistic AI image generator" (Dec. 7, 2024)](https://www.theverge.com/2024/12/7/24315644/grok-x-aurora-ai-image-generator-xai)
- [TechCrunch, "OpenAI peels back ChatGPT's safeguards around image creation" (Mar. 28, 2025)](https://techcrunch.com/2025/03/28/openai-peels-back-chatgpts-safeguards-around-image-creation/)
- [The Verge, "Grok's 'spicy' video mode instantly made me Taylor Swift nude deepfakes" (Aug. 5, 2025)](https://www.theverge.com/report/718975/xai-grok-imagine-taylor-swifty-deepfake-nudes)
- [The Verge, consumer groups' FTC letter on Grok's "Spicy" mode (2025)](https://www.theverge.com/x-ai/759554/consumer-safety-groups-are-demanding-an-ftc-investigation-into-groks-spicy-mode-elon-musk-grok-imagine-xai)
- [The Verge, "ChatGPT's 'adult mode' is expected to debut in Q1 2026" (Dec. 11, 2025)](https://www.theverge.com/news/842657/openai-chatgpt-adult-mode-debut-q1-2026)
- [PCWorld, "OpenAI just nixed ChatGPT's erotic 'adult' mode" (Mar. 26, 2026)](https://www.pcworld.com/article/3099680/openai-just-nixed-chatgpt-erotic-adult-mode.html)
- [Ofcom, investigation into X over Grok (Jan. 12, 2026)](https://www.ofcom.org.uk/online-safety/illegal-and-harmful-content/ofcom-launches-investigation-into-x-over-grok-sexualised-imagery)
- [Ofcom, update on the X investigation and scope of the Online Safety Act](https://www.ofcom.org.uk/online-safety/illegal-and-harmful-content/investigation-into-x-and-scope-of-the-online-safety-act)
- [California Attorney General, investigation into xAI/Grok (Jan. 2026)](https://oag.ca.gov/news/press-releases/attorney-general-bonta-launches-investigation-xai-grok-over-undressed-sexual-ai)
- [European Commission, investigation of Grok and X under the DSA (Jan. 26, 2026)](https://digital-strategy.ec.europa.eu/en/news/commission-investigates-grok-and-xs-recommender-systems-under-digital-services-act)
- [BBC, "X to stop Grok AI from undressing images of real people after backlash" (Jan. 14, 2026)](https://www.bbc.co.uk/news/articles/ce8gz8g2qnlo)
- [The Guardian, "Grok AI: what do limits on tool mean for X, its users and UK media watchdog?" (Jan. 15, 2026)](https://www.theguardian.com/technology/2026/jan/15/grok-ai-images-uk-limits-x-app-ofcom)
- [Business Insider, "Elon Musk responds to backlash over Grok being used to create sexualized images of minors" (Jan. 5, 2026)](https://www.businessinsider.com/elon-musk-grok-bikini-response-sexualized-images-minors-remove-clothes-2026-1)
- [WIRED, "Grok Is Still Hosting Sexualized Deepfakes of Famous Women" (Jun. 11, 2026)](https://www.wired.com/story/grok-is-still-hosting-sexualized-deepfakes-of-famous-women/)
- [Axios, "Exclusive: Grok jailbreak creates sexual, violent images" (Jul. 14, 2026)](https://www.axios.com/2026/07/14/exclusive-grok-jailbreak-creates-sexual-violent-images)
- [Ars Technica, "xAI can't deny Grok makes CSAM anymore. So it's suing users." (Jul. 16, 2026)](https://arstechnica.com/tech-policy/2026/07/xai-cant-deny-grok-makes-csam-anymore-so-its-suing-users/)
- [xAI Acceptable Use Policy, effective June 26, 2026 (archived copy, Compute Terms Observatory)](https://www.termsobservatory.org/version-grok-aup-2026-07-18T01-54-16Z.html)

**Musk statements**
- [The Guardian, "Elon Musk defends stance on diversity and free speech during tense interview" (Mar. 18, 2024)](https://www.theguardian.com/technology/2024/mar/18/elon-musk-defends-stance-diversity-free-speech-interview-don-lemon)
- [Fortune, "What did Elon Musk say in his interview with Don Lemon" (Mar. 18, 2024)](https://fortune.com/2024/03/18/what-did-elon-musk-say-in-don-lemon-interview-free-speech/)
- [ABC News segment transcript of the Lemon interview coverage](https://pickscribe.com/v/bOwNUiZLhRc)
- [Musk post of Jan. 14, 2026 (archive)](https://elonmuskarchive.org/posts/2011562747620712927)

**Law**
- [CRS, "Section 230 Immunity and Generative Artificial Intelligence" (LSB11097, Dec. 28, 2023)](https://www.congress.gov/crs-product/LSB11097)
- [CRS, "The TAKE IT DOWN Act" (LSB11314, May 20, 2025)](https://www.congress.gov/crs-product/LSB11314)
- [47 U.S.C. § 223a](https://uscode.house.gov/us/usc/119-138/t47/s223a/)
- [Public Citizen, "Two-Thirds of States Enact Bills Protecting Public from Deepfake Porn"](https://www.citizen.org/news/two-thirds-of-states-enact-bills-protecting-public-from-deepfake-porn/)
- [*Moody v. NetChoice, LLC*, No. 22-277 (U.S. July 1, 2024)](https://www.supremecourt.gov/opinions/23pdf/22-277new_8mjp.pdf)
- [*Garcia v. Character Technologies*, No. 6:24-cv-1903 (M.D. Fla. May 2025) (order)](https://www.courthousenews.com/wp-content/uploads/2025/05/garcia-v-character-technologies-order.pdf)
- [Lawfare, "If AI Outputs Aren't Speech, Who Has to Prove They're Human?"](https://www.lawfaremedia.org/article/if-ai-outputs-aren-t-speech--who-has-to-prove-they-re-human)
- [Sen. Hawley, Hawley–Blumenthal bill to deny AI companies Section 230 immunity](https://www.hawley.senate.gov/hawley-blumenthal-introduce-bipartisan-legislation-protect-consumers-and-deny-ai-companies-section/)

**Frameworks and compliance**
- [NIST, AI Risk Management Framework (AI RMF 1.0)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
- [NIST, Generative AI Profile (AI 600-1)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [ISO/IEC 42001:2023, AI management systems](https://www.iso.org/standard/42001)
- [Federal Reserve, CA 09-6, Revised FFIEC Fair Lending Examination Procedures](https://www.federalreserve.gov/boarddocs/caletters/2009/0906/caltr0906.htm)
- [Federal Reserve, SR 11-7, Model Risk Management guidance](https://www.federalreserve.gov/boarddocs/srletters/2011/sr1107.pdf)
