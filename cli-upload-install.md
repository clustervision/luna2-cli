# Create Latest PIP package for luna2-cli

Follow setps to Create a Build of luna2-cli tool.

## Step 1 - Install Requirements:
1. OpenSSL to get the SSL Certificate => yum install openssl
2. GIT to Clone, set global config    => yum install git
3. Text Editor to save token & passwd => yum install vim [OR] can use vi or nano
4. Create Personal Access Token from  => https://gitlab.taurusgroup.one/-/profile/personal_access_tokens
5. Install Python 3                   => yum install python3-pip
6. Install required pip packages =><br />
    A. pip package wheel<br />
    B. pip package twine<br />

## Step 2 - Get SSL Certificate
```
openssl s_client -showcerts -servername gitlab.taurusgroup.one -connect gitlab.taurusgroup.one:443 </dev/null 2>/dev/null | sed -n -e '/BEGIN\ CERTIFICATE/,/END\ CERTIFICATE/ p'  > /gitlab.taurusgroup.one.pem
```
```
git config --global http."https://gitlab.taurusgroup.one/".sslCAInfo /gitlab.taurusgroup.one.pem
```
```
export TWINE_CERT=/gitlab.taurusgroup.one.pem
```

## Step 3 - Setup Registry for luna2-cli package
```
vim ~/.pypirc
[distutils]
index-servers =
    gitlab

[gitlab]
repository = https://gitlab.taurusgroup.one/api/v4/projects/20/packages/pypi
username = {Personal-Access-Token-Name}
password = {Personal-Access-Token}
```

## Step 4 - Create luna2-cli package
```
python setup.py sdist bdist_wheel
```

## Step 5 - Upload luna2-cli package to gitlab
```
twine upload --repository gitlab dist/* --cert /gitlab.taurusgroup.one.pem
```

## Step 6 - Install luna2-cli package from gitlab
If certificate PEM file is available
```
pip install luna2-cli --cert /gitlab.taurusgroup.one --index-url https://{Personal-Access-Token-Name}:{Personal-Access-Token}@gitlab.taurusgroup.one/api/v4/projects/20/packages/pypi/simple
```
[OR]<br />
Without certificate file
```
pip install luna2-cli --trusted-host gitlab.taurusgroup.one --index-url https://{Personal-Access-Token-Name}:{Personal-Access-Token}@gitlab.taurusgroup.one/api/v4/projects/20/packages/pypi/simple
```

# /gitlab.taurusgroup.one
```
-----BEGIN CERTIFICATE-----
MIIDqTCCApGgAwIBAgIUU323YeaG7Q2pWd5ZbgPPr9dbZaQwDQYJKoZIhvcNAQEL
BQAwZDELMAkGA1UEBhMCVVMxETAPBgNVBAgMCE1pc3NvdXJpMRQwEgYDVQQHDAtT
YWludCBMb3VpczELMAkGA1UECgwCSVQxHzAdBgNVBAMMFmdpdGxhYi50YXVydXNn
cm91cC5vbmUwHhcNMjIwNjA3MTIyOTM3WhcNMzIwNjA0MTIyOTM3WjBkMQswCQYD
VQQGEwJVUzERMA8GA1UECAwITWlzc291cmkxFDASBgNVBAcMC1NhaW50IExvdWlz
MQswCQYDVQQKDAJJVDEfMB0GA1UEAwwWZ2l0bGFiLnRhdXJ1c2dyb3VwLm9uZTCC
ASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALKPuk4iPLoIhe12uFtq9nS9
OgJe47hXnBMGmNDg5VfELsENwDvgenrki48x9rEYPa7V6EzRePWcAQDvC9afS6Mm
wT354UsE+4NNIHeBb6bSsbp2Wrq7QhLUiJqSMdIDE4CVRu8aqEUrv/XVJOnBeV0U
30NSb2u60sq8nM+/iyQ9D1+/u05g207iELsOq5Kdi8tO2eaov2D53QA21NGV6SUA
fc1eQtEJU/BN8E5WWRghL+esoWKoITcGoCDTKoRdyhl+/EBehXw/uLoHfeNWYvqK
c9sfmgQCy0hFSM5CcTPU7/aHD/+z0mxwMMoDOckrcdq02UffDPGvEtabuTjvkhkC
AwEAAaNTMFEwHQYDVR0OBBYEFCtI3BEXLC7OSd6Dpl3Yg+M/rykRMB8GA1UdIwQY
MBaAFCtI3BEXLC7OSd6Dpl3Yg+M/rykRMA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZI
hvcNAQELBQADggEBAAKBX+rsajrwAPGLweOLaZTrq2AOjT3s6byFRZZx7d/9SX7u
xU3dgr6QPtRP+dkpqtugeQsVG4VUhExXNtoZwkmL4/pfIkPJ32xiNjefvObILWIQ
avx3gP+nPXskwiZW10Sl6fes1NT5P1flS52OC1t4dO1XFzAMHw3s6ZXU2lXJH1xc
4a0c8CIv1ahAocvq5DFLGdNIKs6vVa/RXgWqxPfravasw3iZOAJHCf1C8qw4U6Ns
1zKqqtMKFC2SWZGfI3V5f/Wi1zB25oYADuwVBLnzL0bDoCrFVdCsXWr8H48u4BWb
s+cT2lKipcc+wGNleupC8hda8dymLw0hEXcwmdA=
-----END CERTIFICATE-----
```
