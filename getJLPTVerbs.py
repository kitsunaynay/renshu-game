import requests
from bs4 import BeautifulSoup

def fetch_jlpt_verbs(level):
    kanji_list = []
    hiragana_list = []
    meaning_list = []
    
    url = f"https://jlptsensei.com/jlpt-n{level}-verbs-vocabulary-list/"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve page, status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select('.jl-row')
    for row in rows:
        cell = row.select_one('td.jl-td-v.align-middle > a')
        if cell:
            verb = cell.get_text(strip=True)
            kanji_list.append(verb)

        cell = row.select_one('td.jl-td-vr.align-middle > a')
        if cell:
            verb = cell.get_text(strip=True)
            hiragana_list.append(verb)

        cell = cell.find_next_sibling('td.jl-td-vm.align-middle')
        if cell:
            verb = cell.get_text(strip=True)
            meaning_list.append(verb)

    page = 2
    base_url = f"https://jlptsensei.com/jlpt-n{level}-verbs-vocabulary-list/page/"
    while True:
        url = f"{base_url}{page}/"
        response = requests.get(url)
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select('.jl-row')
        for row in rows:
            cell = row.select_one('td.jl-td-v.align-middle > a')
            if cell:
                verb = cell.get_text(strip=True)
                kanji_list.append(verb)

            cell = row.select_one('td.jl-td-vr.align-middle > a')
            if cell:
                verb = cell.get_text(strip=True)
                hiragana_list.append(verb)

            cell = cell.find_next_sibling('td.jl-td-vm.align-middle')
            if cell:
                verb = cell.get_text(strip=True)
                meaning_list.append(verb)
            
        page += 1
        meaning_list = [""] * len(hiragana_list)
    return [f"{x}; {y}; {z}" for x, y, z in zip(kanji_list, hiragana_list, meaning_list)]

def save_verbs_to_file(verbs, filename='jlpt_verbs.csv'):
    with open(filename, 'w', encoding='utf-8') as f:
        for verb in verbs:
            f.write(verb + '\n')
    print(f"Verbs saved to {filename}")



jlpt_verbs = fetch_jlpt_verbs(level='5')

save_verbs_to_file(jlpt_verbs)