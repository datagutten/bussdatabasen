import json
import xml.etree.ElementTree as ET

import requests


def opplysninger(regnr, return_json=False):
    r = requests.get('https://www.vegvesen.no/System/mobilapi?registreringsnummer='+regnr)
    root = ET.fromstring(r.text)

    opplysninger = dict()
    for child in root:
        opplysninger[child.tag] = str(child.text).strip()
    if return_json:
        return json.dumps(opplysninger)
    else:
        return opplysninger
