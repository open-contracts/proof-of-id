import opencontracts
from bs4 import BeautifulSoup
import email, re, os

warning = """
Warning: This is a prototype contract. It allows you to create a unique ID from 
information that identifies you in the real world, and tie it to your Ethereum account.
This is cool if you want to get loans without collateral, or take part in
one-human-one-vote democracy on the blockchain. But here's the bummer: 

Identifying yourself is pretty much at odds with privacy, for now.

Your ID is currently computed from your name ({}), birthday ({}) and the "bucket-number" ({}),
which indicates which bucket (among 32 buckets total) contains your last 4 SSN digits.

By proceeding to create your ID on the blockchain, *it will become public*.
Anyone who knows (or eventually guesses) these inputs can verify that they 
produce your ID and see that it belongs to your Ethereum account ({}).

For example, someone who knows your name and birthday can quickly compute your bucket-number
by trying out all 32 possible values. Every bucket contains around 1000/32≈312 possibilites 
for your last 4 ssn digits, and they will learn that it is one of those, without knowing which.

Are you *sure* you want to proceed?
"""

instructions = "Login and visit your SSN account page."

with opencontracts.enclave_backend() as enclave:

  def parser(mhtml):
    mhtml = email.message_from_string(mhtml.replace("=\n", ""))
    url = mhtml['Snapshot-Content-Location']
    target_url = "https://secure.ssa.gov/mySSA/start"
    assert url == target_url, "You clicked 'Submit' on '{url}', but should do so on '{target_url}'."
    html = [_ for _ in mhtml.walk() if _.get_content_type() == "text/html"][0]
    parsed = BeautifulSoup(html.get_payload(decode=False))
    name = parsed.find(attrs={'id': '3D"uef-container-tabs0"'}).a.text.strip()
    ssn_box = parsed.find(attrs={'id': '3D"mySSAOverviewSSN"'})
    ssn, _, bday, _ = ssn_box.findChild().findChild().findChildren()
    last4ssn = int(re.findall('[0-9]{4}', ssn.text.strip())[0])
    bday = bday.text.strip()[14:].strip()
    return name, bday, last4ssn
  
  enclave.print(f'Proof of Identity started running in enclave!')
  name, bday, last4ssn = enclave.interactive_session(url='https://secure.ssa.gov/RIL/',
                                                     parser=parser, instructions=instructions)
  # preimage attacks only reveal that last4ssn had one of 10^4/32≈312 values
  bucket_number = int(enclave.keccak(last4ssn, types=('uint256',))[0]) % 32

  ID = enclave.keccak(name, bday, bucket_number, types=('string', 'string', 'uint8'))
  
  enclave.print(f'Computed your ID: {"0x" + ID.hex()}, which may reveal your name, birthday and bucket number.')

  enclave.print(warning.format(name, bday, bucket_number))
  enclave.submit(enclave.user(), ID, types=('bytes32',), function_name='createID')
