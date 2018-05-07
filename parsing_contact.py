import requests
secCode = ""
url = 'https://ssl.allegro.pl/auth/oauth/token'
payload = {'grant_type': secCode, 'code': secCode, 'api-key': 'eyJjbGllbnRJZCI6IjdiNDc4ZjU2LTk2YTYtNDY0Mi04Y2Q2LWYxNjI1MmQ5NWI5OSJ9.CrK_vs2aTBmvvDpZWreEP0ed9zh0vonfbjor2iLdcLA=', 'redirect_uri': 'http:/Justcheckinghow.pl'}



#eyJjbGllbnRJZCI6IjdiNDc4ZjU2LTk2YTYtNDY0Mi04Y2Q2LWYxNjI1MmQ5NWI5OSJ9.CrK_vs2aTBmvvDpZWreEP0ed9zh0vonfbjor2iLdcLA=


# POST with form-encoded data
r = requests.post(url, data=payload, header={"Authorization": "N2I0NzhmNTYtOTZhNi00NjQyLThjZDYtZjE2MjUyZDk1Yjk5:UWlKRHJPSjUzMkFEbmZGa0tSQ1RjeHEzbWtMbmliZ2pLbHM2OFBpUk5PTzkzVE9HYzNWYWhQaGt1cU9qU0VEQw=="})
# Response, status etc
r.text
r.status_code


#https://ssl.allegro.pl/auth/oauth/token?grant_type=authorization_code&code=pOPEy9Tq94aEss540azzC7xL6nCJDWto&api-key=eyJ....My0&redirect_uri=http://justcheckinghow.pl
