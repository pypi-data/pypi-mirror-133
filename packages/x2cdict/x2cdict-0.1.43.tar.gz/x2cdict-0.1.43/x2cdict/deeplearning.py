import deepl
import os

def reform_pos(pos):
  return pos.lower() + "." if pos != None else None


class DeepLVocabDict:
  def __init__(self, from_lang, to_lang="zh-cn"):
    self.from_lang, self.to_lang = from_lang, "zh-cn" if to_lang == "cn" else to_lang 
    self.api = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))

  def search(self, w, pos):
    try:
      _r = self.api.translate_text(w, source_lang=self.from_lang, target_lang=self.to_lang)
      _pos = reform_pos(pos)
      result = {
        "word": w,
        "dict_pos": _pos,
        "meaning": _r.text,
        "extension": None,
        "variations": None,
        "from": "DeepL"
      }
    except Exception as e:
      result = None
    return result


class DeepLPhraseDict:

  def __init__(self, from_lang, to_lang="zh-cn"):
    self.from_lang, self.to_lang = from_lang, "zh-cn" if to_lang == "cn" else to_lang 
    self.api = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))

  def search(self, p):
    try:
      _r = self.api.translate_text(p, source_lang=self.from_lang, target_lang=self.to_lang)
      result = {
        "original": p,
        "translated": _r.text,
        "from": "DeepL"
      }
    except Exception as e:
      print(e)
      result = None
    return result


