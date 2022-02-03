import opencontracts
from bs4 import BeautifulSoup
import email, re, os

with opencontracts.enclave_backend() as enclave:
  enclave.print(f'Proof of Identity started running in enclave!')
  
  def parser(mhtml):
    mhtml = email.message_from_string(mhtml.replace("=\n", ""))
    url = mhtml['Snapshot-Content-Location']
    target_url = "https://secure.ssa.gov/mySSA/start"
    assert url == target_url, f"You clicked 'Submit' on '{url}', but should do so on '{target_url}'."
    html = [_ for _ in mhtml.walk() if _.get_content_type() == "text/html"][0]
    parsed = BeautifulSoup(html.get_payload(decode=False))
    name = parsed.find(attrs={'id': '3D"uef-container-tabs0"'}).a.text.strip()
    ssn_box = parsed.find(attrs={'id': '3D"mySSAOverviewSSN"'})
    ssn, _, bday, _ = ssn_box.findChild().findChild().findChildren()
    last4ssn = int(re.findall('[0-9]{4}', ssn.text.strip())[0])
    bday = bday.text.strip()[14:].strip()
    return name, bday, last4ssn
  
  name, bday, last4ssn = enclave.interactive_session(url='https://secure.ssa.gov/RIL/', parser=parser,
                                                     instructions="Login and visit your SSN account page.")
  
  # we divide all 10000 possible last4ssn into 2^5=32 random buckets, by using only the last 5 bits of hash(last4ssn)
  ssn_bucket = int(enclave.keccak(last4ssn, types=('uint256',))[-1]) % 32
  # the same ssn_bucket could have been computed from 10000/32≈312 different 4-digit combinations
  # so last4ssn isn't revealed even if ssn_bucket can be reverse-engineered from ID
  ID = enclave.keccak(name, bday, ssn_bucket, types=('string', 'string', 'uint8'))
  
  warning = f'Computed your ID: {"0x" + ID.hex()}, which may reveal your name ({name}), birthday ({bday})'
  enclave.print(warning + f' and that your SSN is one of those in bucket no. {ssn_bucket} of 32.')
  
  enclave.submit(enclave.user(), ID, types=('address', 'bytes32',), function_name='createID')
