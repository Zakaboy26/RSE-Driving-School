# RSE Driving School website

Static site, no backend, free on GitHub Pages.

## Edit and build
All page content lives in `build.py` (data blocks at the top: SERVICES, FAQ, TELL, SHOW, QUIZ, DICT, PHOTOS). Edit, then run `python3 build.py` (Python 3, plus nothing to install). Styles are in `css/style.css`, behaviour in `js/main.js`.

## Deploy
1. Push to GitHub, Settings > Pages > Source: GitHub Actions. 
2. For a custom domain, add a `CNAME` file and set repository variable `SITE_URL` (used for canonical URLs and sitemap). All links are relative, so project-site URLs work.

## Needs owner confirmation
- Final live URL (`SITE_URL`).
- Photo consent: `PHOTOS` in `build.py`; set `False` to hide one. `pass-certificate` is hidden by default because its roof sign shows a different phone number. Number plate in `pass-yaris-cross` was blurred; check other photos.
- Instructor photos (initials shown as placeholders), languages spoken, cancellation/payment/refund policy, prices, pick-up rules, intensive/motorway availability.
- Privacy and terms pages are drafts, not legally reviewed.
- Theory test (50 questions, pass 43) and HPT details came from the old site/general knowledge and should be re-checked on GOV.UK.

## Sources
GOV.UK "Car show me, tell me vehicle safety questions" (DVSA, OGL v3.0), GOV.UK driving test pages, GOV.UK test centre finder.

## Not built yet (shown as Coming soon)
How to drive, manoeuvres, hazard perception, independent driving, adverse weather, laws, insurance, disabilities, general FAQs.
