---
title: Projects
nav:
  order: 2
  tooltip: Grants and posters
---

# {% include icon.html icon="fa-solid fa-wrench" %}Projects

Here you can find the grants that fund our research and posters about our work. The public posters explain our studies for a general audience, and some let you take part yourself by solving the same puzzles we give to AI. The conference posters summarize results we have presented at scientific meetings. For the full list of papers, see the [Research page]({{ "/research/" | relative_url }}).

<!-- {% include tags.html tags="participate, infographic, resource" %} -->

{% include search-info.html %}

{% include section.html %}

## Grants

{% include list.html component="card" data="projects" filter="group == 'grants'" %}

{% include section.html %}

## Posters for the public

{% include list.html component="card" data="projects" filter="group == 'public-posters'" %}

{% comment %}
uncomment the section below once conference posters are added to _data/projects.yaml

{% include section.html %}

## Conference posters

{% include list.html component="card" data="projects" filter="group == 'conference-posters'" %}
{% endcomment %}

{% include section.html %}


<!--
## More

{% include list.html component="card" data="projects" filter="!group" style="small" %}
-->
