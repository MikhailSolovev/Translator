import requests
import argparse
from bs4 import BeautifulSoup


def web_page(lang_in, lang_out, word):
    link = 'https://context.reverso.net/translation/' + language[lang_in - 1].lower() + '-' \
           + language[lang_out - 1].lower() + '/' + word
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/88.0.4324.150 Safari/537.36'}
    r = requests.get(link, headers=headers)
    if r:
        # print(str(r.status_code) + ' OK')
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup
    else:
        # print(str(r.status_code) + ' FAIL')
        return None


def translation(html_page, lang_in, lang_out, word):
    try:
        d = html_page.find('div', {'id': 'translations-content'})
    except AttributeError:
        print(f'Sorry, unable to find {word}')
        exit()
    translations = []
    for i in d.find_all('a'):
        translations.append(i.text.strip())
    e = html_page.find_all('div', {'class': 'example'})
    examples = []
    for div in e:
        if lang_in == 1 or lang_in == 6:
            examples.append(div.find('div', {'class': 'src rtl'}).span.text.strip())
        else:
            examples.append(div.find('div', {'class': 'src ltr'}).span.text.strip())
        if lang_out == 6:
            examples.append(div.find('div', {'class': 'trg rtl'}).find('span', {'class': 'text'}).text.strip())
        elif lang_out == 1:
            examples.append(div.find('div', {'class': 'trg rtl arabic'}).find('span', {'class': 'text'}).text.strip())
        else:
            examples.append(div.find('div', {'class': 'trg ltr'}).find('span', {'class': 'text'}).text.strip())
    return translations, examples


def output(translations, examples, count_tr, count_ex, lang_out, out=None):
    if out is not None:
        print('\n' + language[lang_out - 1] + ' Translations:', file=out, flush=True)
        for i in translations[:count_tr]:
            print(i, file=out, flush=True)
        if count_ex == 1:
            print('\n' + language[lang_out - 1] + ' Example:', file=out, flush=True)
        else:
            print('\n' + language[lang_out - 1] + ' Examples:', file=out, flush=True)
        for i, j in zip(examples[:(count_ex + 1):2], examples[1:(count_ex + 1):2]):
            print(i + ':\n' + j + '\n', file=out, flush=True)
    print('\n' + language[lang_out - 1] + ' Translations:')
    for i in translations[:count_tr]:
        print(i)
    if count_ex == 1:
        print('\n' + language[lang_out - 1] + ' Example:')
    else:
        print('\n' + language[lang_out - 1] + ' Examples:')
    for i, j in zip(examples[:(count_ex + 1):2], examples[1:(count_ex + 1):2]):
        print(i + ':\n' + j + '\n')


language = ["Arabic", "German", "English", "Spanish", "French", "Hebrew", "Japanese", "Dutch", "Polish", "Portuguese",
            "Romanian", "Russian", "Turkish"]

# print("Hello, you're welcome to the translator. Translator supports:")
# for i in range(len(language)):
#     print(str(i + 1) + '.', language[i])
# print('Type the number of your language:')
# lang_in = int(input('> '))
# print("Type the number of a language you want to translate to or '0' to translate to all languages:")
# lang_out = int(input('> '))
# print('Type the word you want to translate:')
# word = input('> ')

parser = argparse.ArgumentParser()
parser.add_argument("lang_in")
parser.add_argument("lang_out")
parser.add_argument("word")
args = parser.parse_args()
word = args.word
try:
    lang_in = language.index(args.lang_in.capitalize()) + 1
except ValueError:
    print(f"Sorry, the program doesn't support {args.lang_in}")
    exit()
try:
    if args.lang_out != 'all':
        lang_out = language.index(args.lang_out.capitalize()) + 1
    else:
        lang_out = 0
except ValueError:
    print(f"Sorry, the program doesn't support {args.lang_out}")
    exit()

if lang_out == 0:
    out = open(word + '.txt', 'w')
    for i in range(1, len(language) + 1):
        if i == lang_in:
            continue
        try:
            html_page = web_page(lang_in, i, word)
        except requests.exceptions.ConnectionError:
            print('Something wrong with your internet connection')
            exit()
        translations, examples = translation(html_page, lang_in, i, word)
        output(translations, examples, 2, 2, i, out)
    out.close()
else:
    out = open(word + '.txt', 'w')
    try:
        html_page = web_page(lang_in, lang_out, word)
    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')
        exit()
    translations, examples = translation(html_page, lang_in, lang_out, word)
    output(translations, examples, 3, 3, lang_out, out)
    out.close()
