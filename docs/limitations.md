# Limitations

This project is an early local harness, not a production safety system. I am sharing it as a research-engineering prototype and a concrete study artifact, not as a validated claims or clinical decision product.

- The environment is synthetic and does not use real member, patient, provider, or claims data.
- The default agent is deterministic and rule-based, so it does not capture the full variability of real LLM behavior.
- The optional LLM adapter is a thin structured-output adapter for Ollama Cloud and Hugging Face, not a complete model evaluation platform.
- The project is not a medical, clinical, utilization management, or claims decision system.
- The scenarios are not validated on real-world operational data.
- The policy checks are simplified examples and do not represent actual payer policy logic.
- The scoring rubric is intentionally lightweight and should not be treated as a formal benchmark.
- The project makes no claim of production readiness.

Future work I would prioritize includes more model adapters, broader adversarial scenario sets, more complex workflow states, richer policy retrieval failures, service integration, and human review loops.
