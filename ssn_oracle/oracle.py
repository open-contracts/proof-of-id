import opencontracts
from bs4 import BeautifulSoup
import email, re, os

with opencontracts.enclave_backend() as enclave:

  def parser(mhtml):
    mhtml = email.message_from_string(mhtml.replace("=\n", ""))
    html = [_ for _ in mhtml.walk() if _.get_content_type() == "text/html"][0]
    parsed = BeautifulSoup(html.get_payload(decode=False))
    name = parsed.find(attrs={'id': '3D"uef-container-tabs0"'}).a.text.strip()
    ssn_box = parsed.find(attrs={'id': '3D"mySSAOverviewSSN"'})
    ssn, _, bday, _ = ssn_box.findChild().findChild().findChildren()
    last4ssn = re.findall('[0-9]{4}', ssn.text.strip())[0]
    bday = bday.text.strip()[14:].strip()
    return name, bday, last4ssn
  
  enclave.print(f'Proof of Identity started running in enclave!')
  name, bday, last4ssn = enclave.interactive_session(url='https://secure.ssa.gov/RIL/', parser=parser, instructions=instructions)
  need_more_unique_data_for_privacy = os.urandom(32) # e.g. get dna data from https://23andme.com?
  ID = enclave.keccak(name, bday, last4ssn, need_more_unique_data_for_privacy, types=('string', 'string', 'string', 'bytes32'))  
  enclave.print(f'Confirmed your ID: {ID}')
  enclave.submit(ID, types=('bytes32',), function_name='createID')
