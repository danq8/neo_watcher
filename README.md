<img src="https://raw.githubusercontent.com/danq8/hacs_neo_watcher/main/icon.png" alt="Near Earth Object Watcher logo" title="Near Earth Object Watcher" align="right" height="60" />

# Near Earth Object Watcher

![GitHub Release](https://img.shields.io/github/v/release/danq8/hacs_neo_watcher)

**A custom component for Home Assistant that retrieves NEO data from NASA.**

NASA's Near-Earth Object (NEO) program focuses on detecting, tracking, and characterizing potentially hazardous asteroids and comets that could approach Earth, with the goal of understanding and mitigating potential risks.

They watch so you don't have to worry.

# What this component does

<img src="https://raw.githubusercontent.com/danq8/hacs_neo_watcher/main/doc/Example_Page.JPG" alt="Near Earth Object Watcher example page" title="Near Earth Object Watcher example page" height="500" />

<a href="https://raw.githubusercontent.com/danq8/hacs_neo_watcher/main/doc/Example_view.yaml" target=”_blank”>Download the Home Assistant example page yaml here</a><br/>

This component takes the data for the next 1 week (up to 2 years) provided by the NASA Near Earth Object Web Service<br />  For your chosen time period, it can show you anything from the top 1 to the top 20 "potentially dangerous" and non "potentially dangerous" objects passing by Earth.<br />There is also the option of watching specific NEOs (like everyone's favourite "2024 YR4").<br />  The sensors contain attributes including speed, size, how close to earth it will get, and the date that it will be at it's closest, or the next time it will be close.<br />The orbit detail is especially fascinating as it gives you an incredible 4D model that shows you how the object will pass through our solar system over time. (That's NASA's work!)

<img src="https://raw.githubusercontent.com/danq8/hacs_neo_watcher/main/doc/NASA_NEO_Orbital_Viewer.JPG" alt="NASA Near Earth Object Orbital Viewer" title="NASA's Near Earth Object Orbital Viewer" height="300" />


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

Once initialised you should see the new sensors. There will be one showing the integration stats, along with how ever many NEOs you've selected to watch.

# Configuration

Simply go to Settings --> "Devices and services" --> "Add integration"<br/>choose the NEO Watcher integration<br/>
You will then see this page:<br/>
<img src="https://raw.githubusercontent.com/danq8/hacs_neo_watcher/main/doc/Config_Page_1.JPG" alt="NEO Watcher 1st configuration page" title="NEO Watcher 1st configuration page" height="250" /><br/>
Paste in your NASA API key,<br/>choose between watching a particular object or having the top (closest) objects,<br/>then choose what hour of day you want the data refreshed.<br/><br/>
<table><tr><td>
Top NEOs:<br/>
<img src="https://raw.githubusercontent.com/danq8/hacs_neo_watcher/main/doc/Config_Page_2a.JPG" alt="NEO Watcher 2nd configuration page" title="NEO Watcher 2nd configuration page" height="250" /><br/>
Here you'll be able to choose how far to look into the future in weeks (Maximum 2 years).<br/>
As well as whether you just want the top 1 objects (potentially dangerous and non-potentially dangerous) all the way up to the top 20 for each.<br/></td><td>
Watch a specific NEO:<br/>
<img src="https://raw.githubusercontent.com/danq8/hacs_neo_watcher/main/doc/Config_Page_2b.JPG" alt="NEO Watcher 3rd configuration page" title="NEO Watcher 3rd configuration page" height="250" /><br/>
Here you'll simply need to type in the name or designation of the object.<br/>(You can find these on NASA's NEO page: [https://cneos.jpl.nasa.gov/ca/](https://cneos.jpl.nasa.gov/ca/)<br/>
  </td></tr></table>
Click submit and the data will start to load<br/>



# Contributing To The Project

![python badge](https://img.shields.io/badge/Made%20with-Python-orange)
![github contributors](https://img.shields.io/github/contributors/danq8/hacs_neo_watcher?color=orange)
![last commit](https://img.shields.io/github/last-commit/danq8/hacs_neo_watcher?color=orange)

There are several ways of contributing to this project, they include:

- Suggesting new sensors or NEO information as a feature request

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

# My appreciation

My appreciation goes out to NASA,<br/>
and especially the SpaceRocks Team: David Greenfield, Arezu Sarvestani, Jason English and Peter Baunach.<br/>
[https://github.com/SpaceRocks/](https://github.com/SpaceRocks/)<br/><br/>
I have to mention the amazing work of the Home Assistant team [https://www.home-assistant.io/](https://www.home-assistant.io/)<br/>
And the HACS team [https://www.hacs.xyz/](https://www.hacs.xyz/)<br/><br/>
Also, I have to say a big thanks to Google Gemini, without whose help I couldn't have done it.<br/>Gemini was a game collaborator, but did go off on a few tangents,<br/> telling me on a few occasions that they were certain, certain, certain, certain that this time they had understood the errors from the logs, the hints and documentation I'd provided and that the new, new, new, new suggestion would be the right one.<br/>I'd liken working with Gemini 2.5 with walking a puppy in a park for the first time. Full of enthusiasm and energy, but a little too focused on the strange new bug crawling around on the ground, rather than on me calling it back to safety.<br/>Between us we got the job done, and for that I'm grateful.<br/>
[https://gemini.google.com/app](https://gemini.google.com/app)
