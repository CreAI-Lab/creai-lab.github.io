---
title: Team
nav:
  order: 3
  tooltip: About our team
---

# {% include icon.html icon="fa-solid fa-users" %}Team

{% include section.html %}

The CreAI Lab is based in the Psychological Methods group at the University of Amsterdam and is part of the [A.D. de Groot Cognitive AI Centre](https://degroot.ai). The lab is led by Claire Stevenson (Principal Investigator).

## Team

{% include list.html data="members" component="portrait" filter="role == 'principal investigator'" %}

{% include list.html data="members" component="portrait" filter="group == 'team' && role != 'principal investigator'" %}

## Collaborators

{% include list.html data="members" component="portrait" filter="group == 'collaborators'" %}

## Alumni

{% include list.html data="members" component="portrait" filter="group == 'alumni'" %}





{% raw %}
<!--
{% include section.html background="images/background.jpg" dark=true %}

 Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

{% include section.html %}

{% capture content %}

{% include figure.html image="images/photo.jpg" %}
{% include figure.html image="images/photo.jpg" %}
{% include figure.html image="images/photo.jpg" %}

{% endcapture %}

{% include grid.html style="square" content=content %} 
-->
{% endraw %}
