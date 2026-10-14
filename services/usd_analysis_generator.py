class USDAnalysisGenerator:

  def generate(
    self,
    combined_report: dict
  ) -> dict:

    results = combined_report.get(
      "results",
      []
    )
    all_sections = []
    synthesis_sections = []

    for result in results:

      all_sections.append(
        {
          "agent": result.agent,
          "summary": result.summary,
          "evidence" : result.evidence
        }
      )

      synthesis_sections.append(
        f"{result.agent.upper()}: "
        f"{result.summary}"
      )

    final_synthesis = " ".join(
      synthesis_sections
    )

    return {
      "specialist_count": len(results),
      "results": results, # Original Results
      "sections": all_sections,
      "synthesis": final_synthesis
    }