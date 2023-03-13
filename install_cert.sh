mkdir /usr/share/ca-certificates/extra
cp ~/.mitmproxy/mitmproxy-ca-cert.cer /usr/share/ca-certificates/extra
echo "extra/mitmproxy-ca-cert.cer" >> /etc/ca-certificates.conf
update-ca-certificates