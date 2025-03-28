<img src="https://raw.githubusercontent.com/danq8/hacs_neo_watcher/main/icon.png" alt="Near Earth Object Watcher logo" title="Near Earth Object Watcher" align="right" height="60" />

# Near Earth Object Watcher

![GitHub Release](https://img.shields.io/github/v/release/danq8/hacs_neo_watcher)

**A custom component for Home Assistant that retrieves NEO data from NASA.**

NASA's Near-Earth Object (NEO) program focuses on detecting, tracking, and characterizing potentially hazardous asteroids and comets that could approach Earth, with the goal of understanding and mitigating potential risks.

They watch so you don't have to worry.

# What this component does

<img src="https://raw.githubusercontent.com/danq8/hacs_neo_watcher/main/doc/Example_Page.JPG" alt="Near Earth Object Watcher example page" title="Near Earth Object Watcher example page" align="right" height="600" />
[Download Home Assistant page yaml here](https://raw.githubusercontent.com/danq8/hacs_neo_watcher/main/doc/Example_view.yaml)
  It takes the data for the next 28 days provided by the NASA Near Earth Object Web Service<br />  It discounts any objects that have not been categorised as "potentially dangerous"<br />    It then picks out the closest 5, creates a sensor for each one,<br />  and fills the attributes including speed, size, how close to earth it will get, and the date that it will be at it's closest.

# Why create this component?

I created this Home Assistant integration for two reasons

- Because NASA has made this information public
  
  I had been searching for public API's with interesting information that I could display on HA.<br />  I wanted to learn more about what it takes to create an integration and expose entities with attributes.


- Because the NEO project is a testament to human curiosity and ingenuity.

  It's a reminder that science is not just a subject in school; it's a powerful tool for understanding and safeguarding our world.<br />  The more we know, the less we have to fear, and the more we can appreciate the incredible universe we live in.<br />  This component is meant for people who are curious to know how often large, potentially dangerous objects pass us by on a monthly basis.
  
  If you're looking for an early warning system,<br />   the NASA website and the mainstream news organisations will have the information before it's shown here, sorry.
  
  You can find out more about the NASA project here: https://science.nasa.gov/planetary-defense-neoo/<br />  and here: https://cneos.jpl.nasa.gov/ca/neo_ca_intro.html<br />  and here: https://neo.gsfc.nasa.gov/

  You can find out more about the NASA API here: https://api.nasa.gov/

# Installation

You will need a NASA API key, don't worry, it's free (They just need your email address).

The key can be obtained here, under "Generate API Key": https://api.nasa.gov/

*Please mention this github repository under "How will you use the APIs?"

I plan to submit this repository to the folks at HACS (https://hacs.xyz/).

In the meantime you can install this component by

- going to the HACS menu,<br />  clicking the three dots in the top right of the screen,<br />  selecting "Custom repositories" and adding https://github.com/danq8/hacs_neo_watcher as a repository, <br />  then selecting Type = Integration.

- search the HACS store for NEO Watcher, click on the three dots to the right of the row and click on Download

- You'll be asked to reboot HA

- After the reboot go to Settings --> Devices & services, and click on "+ ADD INTEGRATION"

- Search for NEO Watcher, click on the result, enter your API key and click SUBMIT.

Once initialised you should see 7 new sensors, your allowed API rate limit, how many API calls you have left, and the 5 sensors showing the 5 closest potentially dangerous objects.

# Contributing To The Project

![python badge](https://img.shields.io/badge/Made%20with-Python-orange)
![github contributors](https://img.shields.io/github/contributors/danq8/hacs_neo_watcher?color=orange)
![last commit](https://img.shields.io/github/last-commit/danq8/hacs_neo_watcher?color=orange)

There are several ways of contributing to this project, they include:

- Suggesting new sensors as a feature request

  using this link: [Request a feature](https://github.com/danq8/hacs_neo_watcher/issues/new?template=FEATURE-REQUEST.yml)


- Adding new sensors
- Updating or improving the documentation
- Helping answer/fix any issues raised

  For further details see [contributing](/doc/contributing.md) guidelines.

# Licence

![github licence](https://img.shields.io/badge/Licence-MIT-orange)

This project uses the MIT Licence, for more details see the <a href="/doc/LICENSE">licence</a> document.

# Showing Your Appreciation

If you like this project, please give it a star on [GitHub](https://github.com/danq8/hacs_neo_watcher)
