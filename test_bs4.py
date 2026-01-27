from bs4 import BeautifulSoup

html = """
<tr valign="top">
  <td style="text-align:justify">Et ut intentio nostra sub aliquibus certis limitibus comprehendatur, necessarium est primo investigare de ipsa sacra doctrina, qualis sit, et ad quae se extendat. Circa quae quaerenda sunt decem.
  <td style="text-align:justify">
    <p>To place our purpose within proper limits, we first endeavor to investigate the nature and extent of this sacred doctrine. Concerning this there are ten points of inquiry:
"""

soup = BeautifulSoup(html, 'html.parser')
rows = soup.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    print(f"Cols count: {len(cols)}")
    for i, col in enumerate(cols):
        print(f"Col {i}: {col.get_text()[:30]}...")
