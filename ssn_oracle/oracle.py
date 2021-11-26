import opencontracts
from bs4 import BeautifulSoup
import email, re, os

warning = """
Warning: This is a prototype contract. It allows you to create a unique ID from 
information that identifies you in the real world, and tie it to your Ethereum account.
This is cool if you want to get loans without collateral, or take part in
one-human-one-vote democracy on the blockchain. But here's the bummer: 

Identifying yourself is pretty much at odds with privacy, for now.

Your ID is currently computed from your name ({}), birthday ({}) and last SSN digit ({}).
By proceeding to create your ID on the blockchain, *it will become public*.
Anyone who knows (or eventually guesses) these inputs can verify that they produce your ID.
They will then know this information about you, as well as your current Ethereum account, 
including all its past and future transactions. Are you *sure* you want to proceed?
"""

instructions = "Login and visit your SSN account page."

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
  name, bday, last4ssn = enclave.interactive_session(url='https://secure.ssa.gov/RIL/',
                                                     parser=parser, instructions=instructions)
  ID = enclave.keccak(name, bday, last4ssn[-1], types=('string', 'string', 'string'))
  enclave.print(f'Computed your ID: {ID}.')

  enclave.print(warning.format(name, bday, last4ssn[-1]))
  enclave.submit(ID, types=('bytes32',), function_name='createID')
