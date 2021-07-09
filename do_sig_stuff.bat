makecert -r -pe -n "CN=My CA" -ss CA -sr CurrentUser -a sha256 -cy authority -sky signature -sv MyCA.pvk MyCA.cer 
certutil -user -addstore Root MyCA.cer
makecert -pe -n "CN=My SPC" -a sha256 -cy end -sky signature -ic MyCA.cer -iv MyCA.pvk -sv MySPC.pvk MySPC.cer
pvk2pfx -pvk MySPC.pvk -spc MySPC.cer -pfx MySPC.pfx