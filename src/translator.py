from json import JSONDecodeError
from collections import OrderedDict
import googletrans
import argparse
import json
from os import path
from sys import exit
from fake_useragent import UserAgent
from httpcore import SyncHTTPProxy
import proxyscrape

"""
-i input json file
-o output folder
-l languages
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Json Translator Tool')
    parser.add_argument('--input', '-i', help='input json file', type=str, required=True)
    parser.add_argument('--output', '-o', help='output folder', type=str, required=True)
    parser.add_argument('--input-language', '-il', help='input language', type=str, required=True, choices=googletrans.constants.LANGUAGES.keys())
    parser.add_argument('--output-languages', '-ol', help='output language', type=str, nargs='+', required=True, choices=googletrans.constants.LANGUAGES.keys())
    args = parser.parse_args()

    if not path.exists(args.output):
        print('output folder is not exist')
        exit(1)

    try:
        with open(args.input) as json_file:
            json_result: OrderedDict = OrderedDict(json.load(json_file))
            keys = [x for x in json_result.keys()]
            ua = UserAgent(verify_ssl=False)
            collector = proxyscrape.create_collector('default', ['http', 'https'])
            for output_lang in args.output_languages:
                http = collector.get_proxy({'type': 'http'})
                translator = googletrans.Translator(proxies={
                    'http': SyncHTTPProxy((b'http', http.host.encode(), http.port.encode(), b'')),
                }, user_agent=ua.random)
                translations = translator.translate([str(x) for x in json_result.values()], src=args.input_language, dest=output_lang)
                result = dict()
                for index in range(len(translations)):
                    if json_result[keys[index]] == translations[index].text:
                        print('!!!! invalid translate, key: {}, value: {} !!!!'.format(keys[index], translations[index].text))
                    result[keys[index]] = translations[index].text
                with open(path.join(args.output, output_lang + '.json'), mode='w', encoding='utf-8') as output_json_file:
                    json.dump(result, output_json_file, ensure_ascii=False)
                print('translate to {}'.format(output_lang))
            print('finish translations')
    except IOError:
        print('file is not exist, {}'.format(args.input))
        exit(1)
    except JSONDecodeError:
        print('file is not json, {}'.format(args.input))
        exit(1)
