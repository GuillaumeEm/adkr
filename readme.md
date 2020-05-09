# Automatic dnssec key rotation

A simple script to automatize the rotation of dnssec keys on my self hosted dns server (Bind9)

### Usage

```
cd /etc/bind/zones/example.com

python3 main.py run
```

### Example of zone I use

```
;example.com.zone

$TTL 50000

; example.com
@                       IN              SOA     ns.example.com    postmaster     ( 2020020202 ; Ser
                                        3600;
                                        1500;
                                        2419200;
                                        3600);
; Refresh - Retry - Expire - Minimum

                        IN              NS              ns.example.com.
                        IN              NS              ns6.gandi.net.

@                       IN              A               127.0.0.1
www                     IN              A               127.0.0.1
dev                     IN              A               127.0.0.1
guillaume               IN              A               127.0.0.1
*                       IN              A               127.0.0.1
*                       IN              AAAA            0000:000:0000:0000::1

;mail
@       3000            IN              MX 30           spool.mail.gandi.net.


;canonical names
imap        10000       IN              CNAME   access.mail.gandi.net.
smtp        10000       IN              CNAME   relay.mail.gandi.net.

_imap._tcp.example.com  IN              SRV  0  0 0   .
_imaps._tcp.example.com IN              SRV  0  1 993 spool.mail.gandi.net.

;mail info
@                       IN              TXT     "v=spf1 mx -all"
mail._domainkey.example.com. IN         TXT     "v=DKIM1; k=rsa; p=MIGfMA0aCSqGSIb3qGEBAQUAA4GNADCBiQKBgQCdHtUXtUYfLWDz/vKKOcax3k3wRXW+a7SkQmqAz3xeSXG+OGk5XQiFHEJFcjXLRE6vSIyd2VdH1SuulUg4Sre6mHKr7/8i4LElCAXL2qxaxdcsBc/32lPaQrWdM3B9cPiOkT8jYndC84U8RHsleVmCkVUrn7cNzO0DVG39QUaOYwIDAQac"
_dmarc.example.com.     IN              TXT     "v=DMARC1; p=reject; rua=mailto:postmaster@example.com; ri=604800"

;valid google
@                       IN              TXT     "google-site-verification=btsk7WMWuBj8jCvSjZ2V4DpH3WqYLbgM8c3ca3g29Wm"

;letsencrypt
;_acme-challenge  60 IN      TXT     ..
```

### Output of example zone

```
;example.com.zone

$TTL 50000

; example.com
@                       IN              SOA     ns.example.com    postmaster     ( 2020050906 ; Ser
                                        3600;
                                        1500;
                                        2419200;
                                        3600);
; Refresh - Retry - Expire - Minimum

                        IN              NS              ns.example.com.
                        IN              NS              ns6.gandi.net.

@                       IN              A               127.0.0.1
www                     IN              A               127.0.0.1
dev                     IN              A               127.0.0.1
guillaume               IN              A               127.0.0.1
*                       IN              A               127.0.0.1
*                       IN              AAAA            0000:000:0000:0000::1

;mail
@       3000            IN              MX 30           spool.mail.gandi.net.


;canonical names
imap        10000       IN              CNAME   access.mail.gandi.net.
smtp        10000       IN              CNAME   relay.mail.gandi.net.

_imap._tcp.example.com  IN              SRV  0  0 0   .
_imaps._tcp.example.com IN              SRV  0  1 993 spool.mail.gandi.net.

;mail info
@                       IN              TXT     "v=spf1 mx -all"
mail._domainkey.example.com. IN         TXT     "v=DKIM1; k=rsa; p=MIGfMA0aCSqGSIb3qGEBAQUAA4GNADCBiQKBgQCdHtUXtUYfLWDz/vKKOcax3k3wRXW+a7SkQmqAz3xeSXG+OGk5XQiFHEJFcjXLRE6vSIyd2VdH1SuulUg4Sre6mHKr7/8i4LElCAXL2qxaxdcsBc/32lPaQrWdM3B9cPiOkT8jYndC84U8RHsleVmCkVUrn7cNzO0DVG39QUaOYwIDAQac"
_dmarc.example.com.     IN              TXT     "v=DMARC1; p=reject; rua=mailto:postmaster@example.com; ri=604800"

;valid google
@                       IN              TXT     "google-site-verification=btsk7WMWuBj8jCvSjZ2V4DpH3WqYLbgM8c3ca3g29Wm"

;letsencrypt
;_acme-challenge  60 IN      TXT     ..

; This is a zone-signing key, keyid 14147, for example.com.
; Created: 20200509114437 (Sat May  9 13:44:37 2020)
; Publish: 20200509114437 (Sat May  9 13:44:37 2020)
; Activate: 20200509114437 (Sat May  9 13:44:37 2020)
example.com. IN DNSKEY 256 3 10 AwEAAZ1rkhrLkeJGattwHwP8PmAQtC11pLOEgJ7/L3N1lOkflgLkp0rZ 17HQDEC0yMhDQ2doErufije2j2ZEVoBlqSLyk8lA05Pzklx88hN+KepB pk2OIN/UaLaX+XhYWa92aFcFw/MD/sDw6CL9wuue6xNBiJaCkzUysmWd fkVMvvzLRK/WxlcPnFd+xAf4BKt+MXNMtca+Zt+o0qEi4br/Odb6vcCc tWSH2qNuqhbeCBVmiVNOLBWNrOjWNC8D27pAe9IdvxiEqbKDkY6MWMKv qFuaGEfw510WD8u6EJbHwwUYpRx4lnA0DB5Kxc7GfGTXZKmY3hbJdTfr 9CRCRfPUydJ43tMFe9QaZy/hm6zLLO1dZqp5IrIiLyE1P5508ihncvKY VRmjgcs682Mkfd+yswkCCYk/Gu+RLbHPIB0XBDeMygopzed8ByOy9zQA Z/7hBBqMxCESnE3T+XFyy6pdWRyd6hM5ycCEo5MWAAOFER0Un6evkgfI QZDGEC+PeiyxNqpmFR0+X2gFCiLxAlnuliG+9MTMeGNkZBrjxbvuENZS kbYG32aYh3gKLI4NcoI2K1PxOL2BQ6v191bXs9hN55td0qY5tvddA1TU MEnVbTj4yIm1bxcBjIJy4RLNUw6SxmVq8rbPc0/ZTtCdnrYfdc6g2vUa bnjfrs3ha3wRPWBt
; This is a key-signing key, keyid 60444, for example.com.
; Created: 20200509114437 (Sat May  9 13:44:37 2020)
; Publish: 20200509114437 (Sat May  9 13:44:37 2020)
; Activate: 20200509114437 (Sat May  9 13:44:37 2020)
example.com. IN DNSKEY 257 3 10 AwEAAfjYYCd8jSYSfjkg1xK6ARco6YANfMXw0HYpMFMqmq1RVxDn0eYR 3Twwxu0QLVp9Nq5BjdkkFwTh+1Iy64+bjggiMlFBLRJzjh6cN56bsuTc JwLmmxNu8Bh4jNLYXY1TCYTSkC+V7abjXitcaXvyqjN4D5lw+LXXwDGP HujqYdUqO3spHxEe5F8es6C/gIJqAagHVQveECMugeBCNPyOBmcR91km t9E0uwoOqjovRCiS8bOCZpA4ed13vS/DmvSbKq0XTWJofFQ6zo3L0aCi h3Z5hTLCzmSfL6PqhY2ZXE0LnCrJDnY2yWyvQ2QbAQYn+1OXd3uGH4UP ka7XfNR5WZEsEVnkpvOQqICwKKXm56r8/M82f621msO52cI79Vox2Kbv OPi4OAKBZnVtCoaLwqro3tcLFGT71HwzV+hfx6GUFBVJH8Z3vhE9GF6e OrbQvuiPF3syBMDsUh7E8aGvY68DDzElMApYBSHVJxKvV9cI4dnzmUby NVBe97S3/M5IG5u8thS7qieB993GEW8gYuuL1ODRTV2wISijaUyp4hkd 3VpWO3w4tqj8xommqf2kWSwRTkZCD8sDKztFNHFvilIz4ZnZz6PIBgbw bZX9WxphpiN12grN0jjPse+l2239CuWZJaWa3I4P/BuG7AXeNxv0Kz06 RVtt+8T7wKhiqVTH

```

### Future improvements

* Cleaner _zone_serial retrieval
* Use [dnspython](https://github.com/rthalley/dnspython) ?
* Check if dnssec is available for the domain
* Allow different algorithm/bitsizes
* Use a lib to generate those keys instead of subprocess to dnssec-tools bins
* Handle Fatal errors of dnssec-tools bins (such as -r params not needed anymore on newer versions)
* Awaiting Gand.net support response for v5 api (I can't use rpc anymore)

If you want to use it, please keep in mind that changes are _probably_ needed to get it to work on your side, either to the python script or to your dns configs files
