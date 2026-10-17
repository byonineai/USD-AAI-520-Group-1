from tools.usd_llm_provider_interface import USDLLMProviderInterface


class USDAnalysisGenerator:

    def __init__(self, llm_provider_interface: USDLLMProviderInterface):
        self.llm_provider_interface = llm_provider_interface

    def generate(self, combined_report: dict) -> dict:

        results = combined_report.get("results", [])
        all_sections = []
        synthesis_sections = []

        for result in results:

            all_sections.append(
                {
                    "agent": result.agent,
                    "summary": result.summary,
                    "evidence": result.evidence,
                }
            )

            synthesis_sections.append(f"{result.agent.upper()}: " f"{result.summary}")

        # Generate the synthesis

        if self.llm_provider_interface is not None:

            prompt = self._build_llm_prompt(results)

            final_synthesis = self.llm_provider_interface.generate(prompt)

        else:

            # The deterministic fallback

            final_synthesis = " ".join(synthesis_sections)

        return {
            "specialist_count": len(results),
            "results": results,  # Original Results
            "sections": all_sections,
            "synthesis": final_synthesis,
        }

    def _build_llm_prompt(self, results) -> str:

        all_specialist_sections = []

        for result in results:

            evidence = "\n".join(f"- {item}" for item in result.evidence)

            all_specialist_sections.append(f"""
    SPECIALIST: {result.agent.upper()}

    SUMMARY:
    {result.summary}

    EVIDENCE:
    {evidence}
    """)

        # IMPORTANT:
        # This happens AFTER all specialists
        # have been processed.
        all_specialist_findings = "\n".join(all_specialist_sections)

        return f"""
    You are a professional investment research assistant.

    Create a detailed and unified analysis using all
    the specialist findings listed below.

    Requirements:
    - Do not invent or make up financial data.
    - Use only the supplied evidence.
    - Distinguish factual observations from interpretation.
    - Always mention important limitations.
    - Do not provide personalized financial advice.
    - Keep the analysis and synthesis professional and concise.
    - Explain relevant relationships between specialist findings.
    - Do not omit a specialist when evidence has been supplied.

    - Do not claim that a value increased, decreased, improved,
    worsened, accelerated, or declined unless evidence from
    multiple time periods is provided.
    - Do not infer market liquidity, investor sentiment, valuation
    quality, financial strength, or financial weakness from a
    single metric unless supporting evidence is provided.
    - When comparative evidence is unavailable, report the value
    factually without assigning a qualitative label.
    - If an interpretation cannot be supported by the supplied
    evidence, explicitly state that the available evidence is
    insufficient to make that interpretation.
    - Do not infer a trend from a single observation.
    - General financial relationships may be explained, but they
    must be clearly identified as general interpretation rather
    than a company-specific conclusion.

    SPECIALIST FINDINGS:

    {all_specialist_findings}
    """
