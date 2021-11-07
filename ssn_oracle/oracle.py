import opencontracts
from bs4 import BeautifulSoup
import email, re

with opencontracts.enclave_backend() as enclave:

  def extract_from_ssn(mhtml):
    mhtml = email.message_from_string(mhtml.replace("=\n", ""))
    html = [_ for _ in mhtml.walk() if _.get_content_type() == "text/html"][0]
    parsed = BeautifulSoup(html.get_payload(decode=False))
    name = parsed.find(attrs={'id': '3D"uef-container-tabs0"'}).a.text.strip()
    ssnBox = parsed.find(attrs={'id': '3D"mySSAOverviewSSN"'})
    ssn, _, bday, _ = ssnBox.findChild().findChild().findChildren()
    last4ssn = re.findall('[0-9]{4}', ssn.text.strip())[0]
    bday = bday.text.strip()[14:].strip()
    return name, bday, last4ssn

  identityHash = enclave.keccak(name, bday, last4ssn, types=('string', 'string', 'string'))
  enclave.submit(identityHash, types=('bytes32',), function_name='createIdentity')
