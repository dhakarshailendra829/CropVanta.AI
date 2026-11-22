
from ddgs import DDGS

from modules.core.logger import get_logger

logger = get_logger("AI_Researcher")



def fetch_agri_trends(crop_name: str) -> list[dict]:
    """Fetch agricultural search results using short fallback queries."""

    queries = [
        f"{crop_name} cultivation India",
        f"{crop_name} farming NHB ICAR India",
        f"{crop_name} crop management agriculture",
    ]

    try:
        with DDGS() as ddgs:
            for query in queries:
                try:
                    logger.info("Trying agricultural search query: %s", query)

                    results = ddgs.text(
                        query,
                        max_results=5,
                    )

                    valid_results = [
                        result for result in results
                        if result.get("title")
                        and result.get("body")
                        and result.get("href")
                    ]

                    if valid_results:
                        logger.info(
                            "Retrieved %d results for %s",
                            len(valid_results),
                            crop_name,
                        )
                        return valid_results

                except Exception as exc:
                    logger.warning(
                        "Search query failed (%s): %s",
                        query,
                        exc,
                    )
                    continue

    except Exception as exc:
        logger.warning("DDGS initialization failed: %s", exc)

    logger.warning("All agricultural search queries failed for %s", crop_name)
    return []


def perform_crop_research(crop_name: str) -> str:
    """Generate a research summary from available sources or safe fallback."""

    logger.info("Starting autonomous research for: %s", crop_name)

    results = fetch_agri_trends(crop_name)

    if not results:
        return (
            f"Research search is currently unavailable for {crop_name}. "
            "Please consult local agricultural extension services for "
            "region-specific cultivation and crop-management guidance."
        )

    report = [
        f"### Agricultural Research: {crop_name.capitalize()}",
        "",
        "**Retrieved web references:**",
        "",
    ]

    for index, result in enumerate(results, start=1):
        title = result.get("title", "Untitled source")
        body = result.get("body", "")
        url = result.get("href", "")

        report.extend([
            f"{index}. **{title}**",
            body,
            f"Source: {url}" if url else "Source URL unavailable",
            "",
        ])

    report.extend([
        "---",
        "Research note: Verify recommendations against local soil, "
        "weather, and agricultural extension guidance before making "
        "cultivation decisions.",
    ])

    return "\n".join(report)
