---
title: Images
parent: Chimie
layout: default
has_toc: false
nav_order: 2
---

# Images et Schéma de chimie

Cette page rassemble les illustrations utilisées en physique.

[📥 Télécharger toutes les images]({{ site.baseurl }}/assets/downloads/images-chimie.zip){: .btn .btn-primary }


---

## Galerie

<div class="gallery">
{% assign images = site.static_files | where_exp: "item", "item.path contains '/chimie/images/'" %}

{% for image in images %}
  <a href="{{ image.path | relative_url }}">
    <img src="{{ image.path | relative_url }}"
         alt="{{ image.name }}">
  </a>
{% endfor %}
</div>


