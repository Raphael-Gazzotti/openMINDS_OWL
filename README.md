<a href="/img/openMINDS-OWL_logo_light.png">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="/img/openMINDS-OWL_logo_dark.png">
    <source media="(prefers-color-scheme: light)" srcset="/img/openMINDS-OWL_logo_light.png">
    <img alt="openMINDS-OWL logo" src="/img/openMINDS-OWL_logo_light.png" title="Logo created by R. Gazzotti, U. Schlegel, L. Zehl, C. Hagen Blixhavn" align="right" height="70">
  </picture>
</a>

# openMINDS_OWL

[![GitHub][license-shield]][license-url]
[![GitHub contributors][contributors-shield]][contributors-url]

**openMINDS OWL** is a complete collection of schemas for the metadata models of the openMINDS metadata framework. All schemas are expressed in OWL and available in multiple syntaxes (*.owl for Turtle, *.xml for RDF-XML and *.jsonld for JSON-LD).

## How to contribute

The openMINDS metadata framework is an open-source project and community contributions are highly appreciated. If you want to contribute please follow our :arrow_right: [**contribution guidelines**][contribution-url].

This repository has two main branches: pipeline and main. The pipeline contains the code for building the Java library from the openMINDS schemas. The build process is triggered by changes to the schemas, and runs as a GitHub action. The resultant library is copied to the main branch.

General usage questions should be raised and discussed in our :arrow_right: [**community forum**][community-forum].  
Alternatively you can email us: `support@openmetadatainitiative.org`

## Funding and acknowledgements

The openMINDS metadata framework development started in the [Human Brain Project (HBP)][hbp-website], funded from the European Union’s Horizon 2020 Framework Programme for Research and Innovation under the Specific Grant Agreements [SGA-1 (No.720270)][hbp-sga1-doi], [SGA-2 (No.785907)][hbp-sga2-doi], and [SGA-3 (No. 945539)][hbp-sga3-doi]. 

The framework is further developed as part of the EBRAINS 2.0 project, funded from the European Union's Research and Innovation Program Horizon Europe under Grant Agreement [GA (No.101147319)][ebrains2-doi].

The framework also receives support from the [BigBrain Project](https://bigbrainproject.org/), funded by [HIBALL][hiball-url].

## Collaboration partners

The openMINDS metadata framework is closely collaborating with the [InterLex Project][interlex-dashboard] of the [SciCrunch Data and Resource Infrastructure][scicrunch-website] and the [KnowledgeSpace][ks-website] hosted by the [International Neuroinformatics Coordinating Facility (INCF)][incf-website].

[contributors-url]: https://github.com/openMetadataInitiative/openMINDS_OWL/graphs/contributors
[contributors-shield]: https://img.shields.io/github/contributors/openMetadataInitiative/openMINDS_OWL
[license-url]: https://www.apache.org/licenses/LICENSE-2.0
[license-shield]: https://img.shields.io/badge/License-Apache_2.0-blue.svg
[contribution-url]: https://openminds-documentation.readthedocs.io/en/latest/shared/contribution_guidelines.html
[ebrains2-doi]: https://doi.org/10.3030/101147319
[hiball-url]: https://bigbrainproject.org/hiball.html
[hbp-sga1-doi]: https://doi.org/10.3030/720270
[hbp-sga2-doi]: https://doi.org/10.3030/785907
[hbp-sga3-doi]: https://doi.org/10.3030/945539
[hbp-website]: https://www.humanbrainproject.eu
[incf-website]: https://www.incf.org
[interlex-dashboard]: https://scicrunch.org/scicrunch/interlex/dashboard
[ks-website]: https://knowledge-space.org
[scicrunch-website]: https://scicrunch.org
