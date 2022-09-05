# How I acheived task 0

## ❓Project task❓
```
Our mission is to execute a script 'user_authenticating_into_server' locally on our machine and, using tcpdump, sniff the network to find my password.
Without being a Holberton student, you won't be able to get a hold of the script.

However, running the script would do use telnet to automate sending an email performing the steps below.
```
```
    Trying 167.89.121.145...
    Connected to smtp.sendgrid.net.
    Escape character is '^]'.
    220 SG ESMTP service ready at ismtpd0013p1las1.sendgrid.net
    EHLO ismtpd0013p1las1.sendgrid.net
    250-smtp.sendgrid.net
    250-8BITMIME
    250-PIPELINING
    250-SIZE 31457280
    250-STARTTLS
    250-AUTH PLAIN LOGIN
    250 AUTH=PLAIN LOGIN
    auth login           
    334 VXNlcm5hbWU6
    VGhpcyBpcyBteSBsb2dpbg==
    334 UGFzc3dvcmQ6
    WW91IHJlYWxseSB0aG91Z2h0IEkgd291bGQgbGV0IG15IHBhc3N3b3JkIGhlcmU/ISA6RA==
    235 Authentication successful
    mail from: sylvain@kalache.fr
    250 Sender address accepted
    rcpt to: julien@google.com
    250 Recipient address accepted
    data
    354 Continue
    To: Julien
    From: Sylvain
    Subject: Hello from the insecure world

    I am sending you this email from a Terminal.
    .
    250 Ok: queued as Aq1zhMM3QYeEprixUiFYNg
    quit
    221 See you later
    Connection closed by foreign host.
```

## ❗Solution❗

## 1️⃣
So, this seemed pretty simple. I followed the tutorial found [here](https://opensource.com/article/18/10/introduction-tcpdump), but it didn't really help as much as I would have liked.

So, google searching "how to analyse tcpdump packets" brought me to [here](https://linuxhint.com/tcpdump-beginner-guide/). Which gave me some good ideas, but ultimately a flawed idea of how to execute. I was executing the following.

```
tcpdump | ./user_authenticating_into_server
```

So i was runng tcpdump, and the executing the file hoping that the answer would magically appear on screen in plain text. But alas, all I got was nothing, until i sent the signal interupt:

```
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
^C3 packets captured
6 packets received by filter
0 packets dropped by kernel
```
So I was missing something.
## 2️⃣
After some more reading [here](https://geekflare.com/tcpdump-examples/), [here](https://www.linuxtechi.com/capture-analyze-packets-tcpdump-command-linux/), and [here](https://medium.com/@eranda/analyze-tcp-dumps-a089c2644f19), I realised my understanding was lacking. So instead, I tried to print the verbose output (much more detailed description of the packets):
```
tcpdump -vv | ./user_authenticating_into_server
```
This slight change resulted in absolutly no change in output. Then back to my reading, I realised I can save the output into a file. A-Ha, maybe this is what I want to do, so I tried:
```
tcpdump -w file_name.pcap | ./user_authenticating_into_server
```
after waiting 5 mins (i just guessed how long it would take to execute ./user_authenticating_into_server, then added 4 minutes to be sure), I then sent the signal interupt. Next, i read the files to the screen with:
```
tcpdump -tttt -r file_name.pcap
```
which gave me the output:
```
reading from file file_name.pcap, link-type EN10MB (Ethernet)
2022-09-05 03:52:37.125251 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [P.], seq 1938969967:1938969979, ack 2341492700, win 501, options [nop,nop,TS val 2655778244 ecr 4164262725], length 12
2022-09-05 03:52:37.126564 IP ec2-107-20-8-136.compute-1.amazonaws.com.submission > bbaa4b2616a6.37982: Flags [P.], seq 1:19, ack 12, win 509, options [nop,nop,TS val 4164264660 ecr 2655778244], length 18
2022-09-05 03:52:37.126580 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [.], ack 19, win 501, options [nop,nop,TS val 2655778245 ecr 4164264660], length 0
2022-09-05 03:52:39.126270 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [P.], seq 12:26, ack 19, win 501, options [nop,nop,TS val 2655780245 ecr 4164264660], length 14
2022-09-05 03:52:39.127572 IP ec2-107-20-8-136.compute-1.amazonaws.com.submission > bbaa4b2616a6.37982: Flags [P.], seq 19:37, ack 26, win 509, options [nop,nop,TS val 4164266661 ecr 2655780245], length 18
2022-09-05 03:52:39.127586 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [.], ack 37, win 501, options [nop,nop,TS val 2655780246 ecr 4164266661], length 0
2022-09-05 03:52:40.242775 ARP, Request who-has bbaa4b2616a6 tell ip-172-17-0-1.ec2.internal, length 28
2022-09-05 03:52:40.242798 ARP, Reply bbaa4b2616a6 is-at 02:42:ac:11:00:0f (oui Unknown), length 28
2022-09-05 03:52:41.127469 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [P.], seq 26:48, ack 37, win 501, options [nop,nop,TS val 2655782246 ecr 4164266661], length 22
2022-09-05 03:52:41.166923 IP ec2-107-20-8-136.compute-1.amazonaws.com.submission > bbaa4b2616a6.37982: Flags [P.], seq 37:89, ack 48, win 509, options [nop,nop,TS val 4164268700 ecr 2655782246], length 52
2022-09-05 03:52:41.166956 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [.], ack 89, win 501, options [nop,nop,TS val 2655782286 ecr 4164268700], length 0
2022-09-05 03:52:41.166928 IP ec2-107-20-8-136.compute-1.amazonaws.com.submission > bbaa4b2616a6.37982: Flags [F.], seq 89, ack 48, win 509, options [nop,nop,TS val 4164268700 ecr 2655782246], length 0
2022-09-05 03:52:41.167054 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [F.], seq 48, ack 90, win 501, options [nop,nop,TS val 2655782286 ecr 4164268700], length 0
2022-09-05 03:52:41.168333 IP ec2-107-20-8-136.compute-1.amazonaws.com.submission > bbaa4b2616a6.37982: Flags [.], ack 49, win 509, options [nop,nop,TS val 4164268702 ecr 2655782286], length 0
```
Which to be honset, was a whole lot of gibberish to me at that point. 
## 3️⃣
So, now I have my recorded packets, how to I read them?? well, if I read my documentation correctly I would have seen that recording the packets is just one part, we can display the ascii values in the packets by using the -A flag. as such:
```
tcpdump -A -r file_name.pcap
```

This gave me:
```
reading from file file_name.pcap, link-type EN10MB (Ethernet)
03:52:37.125251 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [P.], seq 1938969967:1938969979, ack 2341492700, win 501, options [nop,nop,TS val 2655778244 ecr 4164262725], length 12
E..@..@.@.*?....k....^.Ks.Uo..W............
.K...5.Eauth login

03:52:37.126564 IP ec2-107-20-8-136.compute-1.amazonaws.com.submission > bbaa4b2616a6.37982: Flags [P.], seq 1:19, ack 12, win 509, options [nop,nop,TS val 4164264660 ecr 2655778244], length 18
E..F..@.;.5.k........K.^..W.s.U{....y%.....
.5...K..334 VXNlcm5hbWU6

03:52:37.126580 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [.], ack 19, win 501, options [nop,nop,TS val 2655778245 ecr 4164264660], length 0
E..4..@.@.*J....k....^.Ks.U{..W............
.K...5..
03:52:39.126270 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [P.], seq 12:26, ack 19, win 501, options [nop,nop,TS val 2655780245 ecr 4164264660], length 14
E..B..@.@.*;....k....^.Ks.U{..W............
.K...5..bXlsb2dpbg==

03:52:39.127572 IP ec2-107-20-8-136.compute-1.amazonaws.com.submission > bbaa4b2616a6.37982: Flags [P.], seq 19:37, ack 26, win 509, options [nop,nop,TS val 4164266661 ecr 2655780245], length 18
E..F..@.;.5.k........K.^..W.s.U.....F|.....
.5...K..334 UGFzc3dvcmQ6

03:52:39.127586 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [.], ack 37, win 501, options [nop,nop,TS val 2655780246 ecr 4164266661], length 0
E..4..@.@.*H....k....^.Ks.U...X............
.K...5..
03:52:40.242775 ARP, Request who-has bbaa4b2616a6 tell ip-172-17-0-1.ec2.internal, length 28
.........B(c................
03:52:40.242798 ARP, Reply bbaa4b2616a6 is-at 02:42:ac:11:00:0f (oui Unknown), length 28
.........B.........B(c......
03:52:41.127469 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [P.], seq 26:48, ack 37, win 501, options [nop,nop,TS val 2655782246 ecr 4164266661], length 22
E..J..@.@.*1....k....^.Ks.U...X............
.L.f.5..bXlwYXNzd29yZDk4OTgh

03:52:41.166923 IP ec2-107-20-8-136.compute-1.amazonaws.com.submission > bbaa4b2616a6.37982: Flags [P.], seq 37:89, ack 48, win 509, options [nop,nop,TS val 4164268700 ecr 2655782246], length 52
E..h..@.;.4.k........K.^..X.s.U............
.5...L.f535 Authentication failed: Bad username / password

03:52:41.166956 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [.], ack 89, win 501, options [nop,nop,TS val 2655782286 ecr 4164268700], length 0
E..4..@.@.*F....k....^.Ks.U...X4...........
.L...5..
03:52:41.166928 IP ec2-107-20-8-136.compute-1.amazonaws.com.submission > bbaa4b2616a6.37982: Flags [F.], seq 89, ack 48, win 509, options [nop,nop,TS val 4164268700 ecr 2655782246], length 0
E..4..@.;.5+k........K.^..X4s.U............
.5...L.f
03:52:41.167054 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [F.], seq 48, ack 90, win 501, options [nop,nop,TS val 2655782286 ecr 4164268700], length 0
E..4..@.@.*E....k....^.Ks.U...X5...........
.L...5..
03:52:41.168333 IP ec2-107-20-8-136.compute-1.amazonaws.com.submission > bbaa4b2616a6.37982: Flags [.], ack 49, win 509, options [nop,nop,TS val 4164268702 ecr 2655782286], length 0
E..4..@.;.5*k........K.^..X5s.U............
.5...L..
```
Which if you were anything like me, was super exciting... but unfortunately more gibberish. Some useful parts
```
535 Authentication failed: Bad username / password
```
showed me that the password and username was sent before this package, but that was essentially all the packets.  

So I started to google all types of crazy things like   
* Why is my tcpdump Ascii output gibberish
* why are the Ascii values of packets not readable   

and so on until I had the thought... If the script was using Telnet, could the packets and the way we read them have something to do with telnet and the way it encrypts the packets. So, I googled
```
what encoding does telnet use?
```
which, turns out is Ascii, so the answers were in my packets AND in plain text. I was on the right path, just asking the wrong question.
So I looked at the script that was being automated again, and focused on lines relating to the authentication, specifically:
```
    250 AUTH=PLAIN LOGIN
    auth login           
    334 VXNlcm5hbWU6
    VGhpcyBpcyBteSBsb2dpbg==
    334 UGFzc3dvcmQ6
    WW91IHJlYWxseSB0aG91Z2h0IEkgd291bGQgbGV0IG15IHBhc3N3b3JkIGhlcmU/ISA6RA==
    235 Authentication successful
```
I figured, if I figured out what was going on there, I could figure this out.
## 4️⃣
So I wanted to know everything about the telnet Authentication process and what encryption is used. Which brought me [here](https://www.ndchost.com/wiki/mail/test-smtp-auth-telnet). One of the first sentences on the page was
```
The first thing you need to do is get a base64 encoding of your username and password.
```
BAM!!! Telnet use ascii characters, converted to Base64 encoding. So, back to my packets.
```
reading from file file_name.pcap, link-type EN10MB (Ethernet)
03:52:37.125251 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [P.], seq 1938969967:1938969979, ack 2341492700, win 501, options [nop,nop,TS val 2655778244 ecr 4164262725], length 12
E..@..@.@.*?....k....^.Ks.Uo..W............
.K...5.Eauth login

03:52:37.126564 IP ec2-107-20-8-136.compute-1.amazonaws.com.submission > bbaa4b2616a6.37982: Flags [P.], seq 1:19, ack 12, win 509, options [nop,nop,TS val 4164264660 ecr 2655778244], length 18
E..F..@.;.5.k........K.^..W.s.U{....y%.....
.5...K..334 VXNlcm5hbWU6

03:52:37.126580 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [.], ack 19, win 501, options [nop,nop,TS val 2655778245 ecr 4164264660], length 0
E..4..@.@.*J....k....^.Ks.U{..W............
.K...5..
03:52:39.126270 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [P.], seq 12:26, ack 19, win 501, options [nop,nop,TS val 2655780245 ecr 4164264660], length 14
E..B..@.@.*;....k....^.Ks.U{..W............
.K...5..bXlsb2dpbg==

03:52:39.127572 IP ec2-107-20-8-136.compute-1.amazonaws.com.submission > bbaa4b2616a6.37982: Flags [P.], seq 19:37, ack 26, win 509, options [nop,nop,TS val 4164266661 ecr 2655780245], length 18
E..F..@.;.5.k........K.^..W.s.U.....F|.....
.5...K..334 UGFzc3dvcmQ6

03:52:39.127586 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [.], ack 37, win 501, options [nop,nop,TS val 2655780246 ecr 4164266661], length 0
E..4..@.@.*H....k....^.Ks.U...X............
.K...5..
03:52:40.242775 ARP, Request who-has bbaa4b2616a6 tell ip-172-17-0-1.ec2.internal, length 28
.........B(c................
03:52:40.242798 ARP, Reply bbaa4b2616a6 is-at 02:42:ac:11:00:0f (oui Unknown), length 28
.........B.........B(c......
03:52:41.127469 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [P.], seq 26:48, ack 37, win 501, options [nop,nop,TS val 2655782246 ecr 4164266661], length 22
E..J..@.@.*1....k....^.Ks.U...X............
.L.f.5..bXlwYXNzd29yZDk4OTgh

03:52:41.166923 IP ec2-107-20-8-136.compute-1.amazonaws.com.submission > bbaa4b2616a6.37982: Flags [P.], seq 37:89, ack 48, win 509, options [nop,nop,TS val 4164268700 ecr 2655782246], length 52
E..h..@.;.4.k........K.^..X.s.U............
.5...L.f535 Authentication failed: Bad username / password

03:52:41.166956 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [.], ack 89, win 501, options [nop,nop,TS val 2655782286 ecr 4164268700], length 0
E..4..@.@.*F....k....^.Ks.U...X4...........
.L...5..
03:52:41.166928 IP ec2-107-20-8-136.compute-1.amazonaws.com.submission > bbaa4b2616a6.37982: Flags [F.], seq 89, ack 48, win 509, options [nop,nop,TS val 4164268700 ecr 2655782246], length 0
E..4..@.;.5+k........K.^..X4s.U............
.5...L.f
03:52:41.167054 IP bbaa4b2616a6.37982 > ec2-107-20-8-136.compute-1.amazonaws.com.submission: Flags [F.], seq 48, ack 90, win 501, options [nop,nop,TS val 2655782286 ecr 4164268700], length 0
E..4..@.@.*E....k....^.Ks.U...X5...........
.L...5..
03:52:41.168333 IP ec2-107-20-8-136.compute-1.amazonaws.com.submission > bbaa4b2616a6.37982: Flags [.], ack 49, win 509, options [nop,nop,TS val 4164268702 ecr 2655782286], length 0
E..4..@.;.5*k........K.^..X5s.U............
.5...L..
```
armed with [this](https://www.base64decode.org/) base64 decoder, I started to just copy and paste every piece of gibberish longer that 3 characters to see what I got.
* VXNlcm5hbWU6 decoded to 'Username:'
* bXlsb2dpbg== decoded to 'mylogin'
* UGFzc3dvcmQ6 decoded to 'Password:'
* bXlwYXNzd29yZDk4OTgh decoded to 'mypassword9898!'

This wasn't some attempt to make this article more exciting, that is genuinely the order I decoded in. But in the end, there was the password.   
I hope you enjoyed the process of using TCPdump to get the password from a Telnet connection.