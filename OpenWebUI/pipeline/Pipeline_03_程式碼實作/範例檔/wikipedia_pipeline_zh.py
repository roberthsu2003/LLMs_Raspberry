"""
title: Wikipedia Article Retrieval chinese
author: Unknown
author_url: Unknown
description: Wikipedia Search and Return
required_open_webui_version: 0.4.3
requirements: wikipedia
version: 0.4.3
licence: MIT
"""

import os
import re
import time
from datetime import datetime
from logging import getLogger
from typing import Generator, Iterator, List, Union

import requests
import wikipedia
from pydantic import BaseModel, Field

wikipedia.set_lang("zh")

logger = getLogger(__name__)
logger.setLevel("DEBUG")


class Pipeline:
    class Valves(BaseModel):
        RATE_LIMIT: int = Field(default=5, description="Rate limit for the pipeline")
        WORD_LIMIT: int = Field(
            default=300, description="Word limit when getting page summary"
        )
        WIKIPEDIA_ROOT: str = Field(
            default="https://zh.wikipedia.org/wiki",
            description="Wikipedia（中文）根網址",
        )

    def __init__(self):
        self.name = "中文維基百科 Pipeline"
        self.valves = self.Valves(
            **{k: os.getenv(k, v.default) for k, v in self.Valves.model_fields.items()}
        )

    async def on_startup(self):
        logger.debug(f"on_startup:{self.name}")
        pass

    async def on_shutdown(self):
        logger.debug(f"on_shutdown:{self.name}")
        pass

    def rate_check(self, dt_start: datetime):
        dt_end = datetime.now()
        time_diff = (dt_end - dt_start).total_seconds()
        time_buffer = 1 / self.valves.RATE_LIMIT
        if time_diff >= time_buffer:
            return False
        time.sleep(time_buffer - time_diff)
        return True

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        logger.debug(f"pipe:{self.name}")

        if ("broad tags categorizing" in user_message.lower()) or (
            "Create a concise" in user_message.lower()
        ):
            logger.debug(f"Title Generation (aborted): {user_message}")
            return "(title generation disabled)"

        logger.info(f"User Message: {user_message}")
        dt_start = datetime.now()
        multi_part = False
        streaming = body.get("stream", False)
        context = ""

        for query in user_message.split(";"):
            self.rate_check(dt_start)
            query = query.strip()

            if multi_part:
                if streaming:
                    yield "---\n"
                else:
                    context += "---\n"
            if body.get("stream", True):
                yield from self.stream_retrieve(query, dt_start)
            else:
                for chunk in self.stream_retrieve(query, dt_start):
                    context += chunk
            multi_part = True

        if not streaming:
            return context if context else "No information found"

    def stream_retrieve(
        self,
        query: str,
        dt_start: datetime,
    ) -> Generator:
        re_query = re.compile(r"[^0-9A-Z]", re.IGNORECASE)
        re_rough_word = re.compile(r"[\w]+", re.IGNORECASE)

        titles_found = None
        try:
            titles_found = wikipedia.search(query)
            logger.info(f"Query: {query}, Found: {titles_found}")
        except Exception as e:
            logger.error(f"Search Error: {query} -> {e}")
            yield f"Page Search Error: {query}"

        if titles_found is None or not titles_found:
            yield f"No information found for '{query}'"
            return

        self.rate_check(dt_start)

        try:
            title_check = titles_found[0]
            wiki_page = wikipedia.page(title_check, auto_suggest=False)
        except wikipedia.exceptions.DisambiguationError as e:
            str_error = str(e).replace("\n", ", ")
            str_error = f"## Disambiguation Error ({query})\n* Status: {str_error}"
            logger.error(str_error)
            yield str_error + "\n"
            return
        except wikipedia.exceptions.RedirectError as e:
            str_error = str(e).replace("\n", ", ")
            str_error = f"## Redirect Error ({query})\n* Status: {str_error}"
            logger.error(str_error)
            yield str_error + "\n"
            return
        except Exception as e:
            if titles_found:
                str_error = f"## Page Retrieve Error ({query})\n* Found Topics (matched '{title_check}') {titles_found}"
                logger.error(f"{str_error} -> {e}")
            else:
                str_error = f"## Page Not Found ({query})\n* Unknown error"
                logger.error(f"{str_error} -> {e}")
            yield str_error + "\n"
            return

        logger.info(f"Page Sections[{query}]: {wiki_page.sections}")
        yield f"## {title_check}\n"

        summary_full = wiki_page.summary
        word_positions = [x.start() for x in re_rough_word.finditer(summary_full)]
        if len(word_positions) > self.valves.WORD_LIMIT:
            yield summary_full[: word_positions[self.valves.WORD_LIMIT]] + "...\n"
        else:
            yield summary_full + "\n"

        yield "### Learn More" + "\n"
        yield f"* [Read more on Wikipedia...]({wiki_page.url})\n"

        link_md = [
            f"[{x}]({self.valves.WIKIPEDIA_ROOT}/{re_query.sub('_', x)})"
            for x in titles_found
        ]
        yield f"* Related topics: {', '.join(link_md)}\n"

        if wiki_page.images:
            yield f"\n![Image: {title_check}]({wiki_page.images[0]})\n"

        return
