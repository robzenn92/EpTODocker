# Cyclon

Cyclon [1] is a complete framework for inexpensive membership management in very large P2P overlays. It an improvement of the basic shuffling protocol developed by Stavrou et al. [2]. It is highly scalable, very robust, and completely decentralized. Most important is that the resulting communication graphs share important properties with random graphs.

## Cyclon as a container

You should think of Cyclon as a single peer that autonomously runs the cyclon protocol. In fact, this is not simulation of peers which run Cyclon. To archive that, everything inside this folder is packed as a Docker container. This allows us to deploy as many containers as we want so that each of them play the role of a peer. Each container (peer) periodically exchange its [PartialView](https://github.com/robzenn92/EpTODocker/tree/master/partialView) via messages sent over the network by first contacting other peers through the APIs exposed by `app.py` and then executing Cyclon functions based on the messages received.

## The structure

Cyclon has been developed as a web service. Although the core features such as shuffle and periodic view exchanges are defined in `cyclon.py`, it relies on REST APIs exposed as a Flask application in `app.py`. This allows peers to send messages each other over the network.

## References

[1] S. Voulgaris, D. Gavidia, M. van Steen. [CYCLON: Inexpensive Membership Management for Unstructured P2P Overlays](http://gossple2.irisa.fr/~akermarr/cyclon.jnsm.pdf). J. Network Syst. Manage. 13(2): 197-217 (2005)

[2] A. Stavrou, D. Rubenstein, and S. Sahu, [A lightweight robust P2P system to handle flash crowds](http://ieeexplore.ieee.org/document/1181410/), IEEE Journal on Selected Areas in Communications, Vol. 22, No. 1, pp. 6–17, 2004.