from parse_summa import is_latin

text_english = "FIRST PART (FP: Questions 1-119)"
print(f"Testing: '{text_english}' -> {is_latin(text_english)}")

text_nav = "To place our purpose within proper limits, we first endeavor to investigate the nature and extent of this sacred doctrine. Concerning this there are ten points of inquiry:"
print(f"Testing: '{text_nav}' -> {is_latin(text_nav)}")

text_obj = 'Objection 1: It seems that, besides philosophical science, we have no need of any further knowledge. For man should not seek to know what is above reason: "Seek not the things that are too high for thee" (Ecclus. 3:22). But whatever is not above reason is fully treated of in philosophical science. Therefore any other knowledge besides philosophical science is superfluous.'
print(f"Testing Obj: {is_latin(text_obj)}")
