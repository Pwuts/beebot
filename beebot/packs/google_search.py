from typing import Type

from langchain import GoogleSerperAPIWrapper
from pydantic import BaseModel, Field

from beebot.packs.system_base_pack import SystemBasePack

PACK_NAME = "google_search"
PACK_DESCRIPTION = (
    "Search Google for websites matching a given query. Useful for when you need to answer questions "
    "about current events."
)


class GoogleSearchArgs(BaseModel):
    query: str = Field(..., description="The query string")


class GoogleSearch(SystemBasePack):
    name: str = PACK_NAME
    description: str = PACK_DESCRIPTION
    args_schema: Type[BaseModel] = GoogleSearchArgs
    categories: list[str] = ["Web", "Information"]

    def _run(self, query: str) -> list[str]:
        try:

            results = GoogleSerperAPIWrapper().results(query).get("organic", [])
            formatted_results = []
            for result in results:
                formatted_results.append(
                    f"{result.get('link')}: {result.get('snippet')}"
                )

            return f"Your search results are: {' | '.join(formatted_results)}"

        except Exception as e:
            return f"Error: {e}"
