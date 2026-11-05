# RAG Tenant Fence

Audit retrieval traces for cross-tenant document exposure and missing provenance.

RAG Tenant Fence checks recorded retrieval results against an authoritative query tenant. It fails closed on unknown documents or missing tenant metadata and separately reports missing source provenance. It is designed for offline review of redacted traces or CI fixtures; it does not implement a vector database.

The central invariant is tested on what was actually returned, not on what a retriever claims it intended to return. A clean report is evidence about the supplied trace only.

## Install and run

Requires Python 3.11 or newer. The tool uses only the standard library.

~~~sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
rag-fence-audit examples/input.json
~~~

Run the regression suite:

~~~sh
python -m unittest discover -s tests -v
~~~

## Design constraints

This project is a local, deterministic analysis component. It does not call a model, contact a provider, or make changes to external systems. Findings are evidence for review, not a guarantee that an application is safe.

## References

- [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) (retrieval and data-security risks)
- [OWASP GenAI Data Security Best Practices](https://genai.owasp.org/)

## License

MIT. See LICENSE.
