import opencontracts
from bs4 import BeautifulSoup
import email, re, os

with opencontracts.enclave_backend() as enclave:
  enclave.print(f'Proof of Identity started running in enclave!')
  
  def parser(mhtml):
    mhtml = email.message_from_string(mhtml.replace("=\n", ""))
    html = [_ for _ in mhtml.walk() if _.get_content_type() == "text/html"][0]
    url = mhtml['Snapshot-Content-Location']
    target_url = "https://secure.ssa.gov/myssa/myprofile-ui/main"
    assert url == target_url, f"You clicked 'Submit' on '{url}', but should do so on '{target_url}'."
    strings = list(BeautifulSoup(html.get_payload(decode=False)).strings)
    for key, value in zip(strings[:-1],strings[1:]):
      if key.startswith("Name:"): name = value.strip()
      if key.startswith("SSN:"): last4ssn = int(re.findall('[0-9]{4}', value.strip())[0])
      if key.startswith("Date of Birth:"): bday = value.strip()
    return name, bday, last4ssn
  
  name, bday, last4ssn = enclave.interactive_session(url='https://secure.ssa.gov/RIL/', parser=parser,
                                                     instructions="Login and visit your SSN account page.")
  
  # we divide all 10000 possible last4ssn into 32 random buckets, by using only the last 5=log2(32) bits
  # so last4ssn isn't revealed even if ssn_bucket can be reverse-engineered from ID
  ssn_bucket = int(enclave.keccak(last4ssn, types=('uint256',))[-1]) % 32
  ID = enclave.keccak(name, bday, ssn_bucket, types=('string', 'string', 'uint8'))  
  
  # publishing your SSN reveals that last4ssn was one of the following possibilites:
  possibilities = list()
  for possibility in range(10000):
    bucket = int(enclave.keccak(possibility, types=("uint256",))[-1]) % 32
    if bucket == ssn_bucket: possibilities.append(str(possibility).zfill(4))
  n = len(possibilities)

  warning = f'Computed your ID: {"0x" + ID.hex()}, which may reveal your name ({name}), birthday ({bday})'
  enclave.print(warning + f' and that your last 4 SSN digits are one of the following {n} possibilites: {possibilities}')
  
  enclave.submit(enclave.user(), ID, types=('address', 'bytes32',), function_name='createID')
