# Design Notes

## Deterministic mock agent first

I started with a deterministic mock agent so the evaluation harness could be tested without API keys, model variability, or hidden prompting behavior. This makes the project easier to explain and easier to debug: every scenario produces the same action plan unless the code or scenario data changes.

The mock agent is intentionally simple. I did not build it to be impressive as an agent. I built it to exercise the environment, policy checks, audit trace, scoring, and report generation.

The expanded scenario set includes compound cases because real governed workflows rarely fail in only one dimension. The mock agent handles them with explicit precedence rules: unauthorized access and policy-bypass instructions lead to refusal; incomplete context or low confidence leads to escalation; missing evidence blocks submission; complete evidence with adequate context can proceed.

## Why synthetic healthcare-style workflows

I chose a synthetic healthcare-style workflow because payer and prior authorization processes combine sensitive data, policy-driven decisions, required documentation, escalation paths, and audit expectations. Those properties make the examples realistic enough to stress tool safety without using real member data or making the project a medical or claims decision system.

The records in this repository are synthetic and anonymized. Identifiers such as `mem_1001` and `case_safe_knee_mri` are invented for local testing.

## Separating policy checks from agent behavior

I separated the policy engine from the agent on purpose. The agent proposes actions; the policy engine evaluates whether those actions are allowed. This separation keeps the harness useful for comparing different agents later.

That design also reflects a lesson from regulated workflow design: the system should not rely only on the model to remember the rules. Policy checks should be inspectable, testable, and auditable outside the agent prompt.

## Future LLM adapters

The `Agent` base class defines a small interface: given a scenario and record, return a list of proposed actions. I kept this interface narrow so the repository can include optional provider adapters, such as Ollama Cloud or Hugging Face, without changing the evaluator.

The evaluator should not need to know whether actions came from the deterministic mock agent or a real model. That keeps model integration optional and prevents paid APIs from becoming a requirement for local evaluation.

The same boundary can support additional model adapters later. The important design choice is that policy validation stays outside the model call.

## Why audit traces matter

In high-compliance settings, a final answer is not enough. Reviewers need to see what tools were called, whether the calls were allowed, which policy checks ran, what decision was made, and why.

The harness records an audit event for each tool call and final decision. I kept the trace plain and serializable so it can be inspected in the terminal, tested with pytest, or written to JSON for later review.

## Integration shape

The report writer stores JSON on disk. That keeps the harness simple while making it easy for another application, CI job, or service wrapper to collect and persist evaluation results elsewhere.
