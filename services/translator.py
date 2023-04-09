import json

from translate import Translator
import langid

from services.abstract_service import AbstractService

class Service(AbstractService):
    """
Builtin service that translate posts to desired languages
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dst_langs = ["fr", "en", "de", "es", "ru"]
        self.on_post_max_size = 10

    def on_post(self, post):
        if post["type"] == "wrote_crew_wall_message"\
        and not post["content"].startswith("/")\
        and not post["content"].startswith(":ntrs"):
            is_translated = False
            for comment in post["comments"]:
                if int(comment["actor"]["id"]) == self.connector.get_self_player().id:
                    is_translated = True
            if not is_translated:
                content = post["content"]
                src_lang, _ = langid.classify(content)
                for dst_lang in self.dst_langs:
                    if dst_lang != src_lang:
                        translator = Translator(from_lang=src_lang, to_lang=dst_lang)
                        translation = translator.translate(content)
                        if translation != content:
                            self.connector.comment_post(post["id"], f"[{dst_lang}]"+translation)

    def start(self):
        self.running = True
