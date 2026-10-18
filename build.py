#!/usr/bin/env python3
"""Generates the static site into this folder. Run: python3 build.py
Edit SITE_URL once the final address is known. Content lives in the data blocks below."""
import os, json, html
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = os.environ.get("SITE_URL", "https://www.roadsafetyexpertdrivingschool.co.uk")  # TODO: set to final live URL
PHONE_D, PHONE_T, EMAIL = "07450 157678", "+447450157678", "atta.sadaat@gmail.com"
E = html.escape
pages = []  # (path, title) for sitemap

# ---------- DATA ----------
AREAS = ["Mill Hill","Greenford","Hendon","Pinner","Harrow","Wembley","Northolt","Ruislip","Ealing","Perivale","Kingsbury","Stanmore"]

# approved=False keeps a photo off the public site until the owner confirms consent.
PHOTOS = [
 ("pass-test-centre","Smiling learner holding a Passed My Test sign and pass certificate beside an RSE driving school car",True),
 ("pass-toyota-yaris","Learner holding a Passed My Test sign in front of an RSE hybrid learner car",True),
 ("pass-green-hedge","Learner making a peace sign with a Passed My Test sign in front of a driving school car",True),
 ("pass-yaris-cross","Learner holding her pass certificate beside an RSE learner car",True),
 ("pass-certificate","Learner holding a practical test pass certificate beside a driving school car",False),  # shows another phone number on roof sign: confirm before publishing
]
OK_PHOTOS = [p for p in PHOTOS if p[2]]

SERVICES = [
 ("Manual lessons","Learn in a car with a clutch and gears. Suits anyone who wants a licence that covers both manual and automatic cars.","Beginners, returners and learners wanting the full licence.","Clear step-by-step coaching on clutch control, gear changes and busy-road decisions at your own pace."),
 ("Automatic lessons","Learn without a clutch, so you can focus on observation, road positioning and decision-making.","Learners who want a simpler start, or who plan to drive an automatic.","Lessons in an automatic car. Note that an automatic test pass only covers automatic cars."),
 ("Beginner lessons","A calm start for people who have never driven. We begin with the controls and build up gradually.","Complete beginners of any age.","Quiet practice areas first, then residential roads as your confidence grows."),
 ("Refresher lessons","Rebuild confidence after a break, or after moving to the UK.","Licence holders who feel rusty or nervous.","A first lesson to see where you are, then a plan to work on the areas you choose."),
 ("Mock driving tests","A practice run under test-style conditions so test day feels familiar.","Learners close to test standard.","A test-style drive, followed by honest feedback on what to improve."),
 ("Test day car hire","Use the instructor's car for your practical test, including a pre-test warm-up.","Learners booked for a practical test.","A warm-up drive before the test, in a car you already know. Contact us to confirm availability and cost."),
 ("Pass Plus","Extra training for new drivers who want more experience in different conditions. Some insurers may offer a discount, but this is not guaranteed.","Drivers who have recently passed.","Contact us to confirm what the course covers and how it is arranged."),
 ("Theory test support","Guidance on how to revise for the theory test, with short theory chats linked to real situations during lessons.","Anyone preparing for the theory test.","Revision advice, multiple-choice technique and links to our free Learning Centre."),
 ("Nervous learner support","Lessons with a patient, calm approach and clear communication.","Anyone anxious about driving.","You set the pace. We talk through each step before you do it."),
]

FAQ = [
 ("Do you offer manual and automatic lessons?","Yes, we offer both manual and automatic lessons."),
 ("Do you teach complete beginners?","Yes. Many of our learners have never driven before. We start with the basics and move at your pace."),
 ("Do I need to pass my theory test before taking driving lessons?","No. You need a provisional licence to start lessons, but you do not have to pass the theory test first. You do need to pass it before you can book your practical test."),
 ("How many lessons might I need?","It varies from person to person. It depends on your starting point, how often you practise and how confident you feel. Your instructor will give you an honest view as you progress."),
 ("How often should I take lessons?","Regular lessons help you remember what you have learned. Many learners find one or two a week works well. We can discuss what suits your schedule."),
 ("Do you offer refresher lessons?","Yes. See our services page, or contact us to talk about what you need."),
 ("Do you teach nervous learners?","Yes. We aim for calm, stress-free lessons with clear communication."),
 ("Can you help me prepare for my practical test?","Yes. We offer test preparation and mock driving tests, and our Learning Centre explains how the test works."),
 ("Can I use your car for my driving test?","Yes, test day car hire is available, including a pre-test warm-up. Contact us to confirm availability and cost."),
 ("Can you help me book a driving test?","Yes, contact us and we can discuss how we can help with test bookings."),
 ("What happens if it rains?","Lessons normally go ahead in rain, and learning to drive in different weather is useful. Contact your instructor if you have concerns about severe weather."),
 ("What should I bring to my first lesson?","Bring your provisional driving licence. If you wear glasses or contact lenses to drive, bring them too. Contact us if you are unsure about anything else."),
 ("Can I be picked up from home, work or college?","Pick-up arrangements depend on the area and availability. Contact us with your postcode and we will confirm."),
 ("Do you offer intensive courses?","Contact us to ask about availability and what we can arrange."),
 ("Do you offer motorway lessons?","Contact us to ask about motorway tuition. Learners may use motorways only with an approved driving instructor in a car with dual controls."),
 ("Do you provide Pass Plus?","Yes, Pass Plus training is available for new drivers who want more experience."),
 ("How do I enquire about lessons?","Call "+PHONE_D+" or email "+EMAIL+". Tell us your postcode and whether you want manual or automatic."),
 ("What is your cancellation policy?","Please contact the school to confirm the current cancellation terms before booking. [Owner: add policy here.]"),
 ("When do I pay for lessons?","Please contact the school to confirm payment arrangements. [Owner: add details here.]"),
 ("Can I get a refund for unused lessons?","Please contact the school to confirm the refund policy. [Owner: add policy here.]"),
]

# (question, official model answer (GOV.UK, OGL v3.0), plain-English explanation, safety note)
TELL = [
 ("Tell me how you'd check that the brakes are working before starting a journey.","Brakes should not feel spongy or slack. Brakes should be tested as you set off. Vehicle should not pull to one side.","Press the brake pedal: it should feel firm. Then, when you first move off slowly, brake gently and check the car stays straight.","Test the brakes at low speed in a safe, clear place."),
 ("Tell me where you'd find the information for the recommended tyre pressures for this car and how tyre pressures should be checked.","Manufacturer's guide, use a reliable pressure gauge, check and adjust pressures when tyres are cold, don't forget spare tyre, remember to refit valve caps.","The car's handbook lists the right pressures (some cars also show them inside the door or fuel flap). Use a gauge, ideally when the tyres are cold.","Wrong pressures affect grip, braking and tyre wear."),
 ("Tell me how you make sure your head restraint is correctly adjusted so it provides the best protection in the event of a crash.","The head restraint should be adjusted so the rigid part of the head restraint is at least as high as the eye or top of the ears, and as close to the back of the head as is comfortable. Note: Some restraints might not be adjustable.","The head restraint is there to limit whiplash. Set the top level with your eyes or the tops of your ears, and close to the back of your head.","Adjust it before you drive, not on the move."),
 ("Tell me how you'd check the tyres to ensure that they have sufficient tread depth and that their general condition is safe to use on the road.","No cuts and bulges, 1.6mm of tread depth across the central three-quarters of the breadth of the tyre, and around the entire outer circumference of the tyre.","Look at each tyre for cuts and bulges. The legal minimum tread depth is 1.6mm across the central three-quarters of the tyre and all the way round.","Tread helps clear water, so worn tyres lengthen stopping distances in the wet."),
 ("Tell me how you'd check that the headlights and tail lights are working. You don't need to exit the vehicle.","Explain you'd operate the switch (turn on ignition if necessary), then walk round vehicle (as this is a 'tell me' question, you don't need to physically check the lights).","Switch the lights on, then say you would walk round the car to check each light is working.","You only need to explain it. You do not need to get out."),
 ("Tell me how you'd know if there was a problem with your anti-lock braking system.","Warning light should illuminate if there is a fault with the anti-lock braking system.","If there is a fault, an ABS warning light shows on the dashboard.","Do not ignore the light. Have the car checked."),
 ("Tell me how you'd check the direction indicators are working. You don't need to exit the vehicle.","Explain you'd operate the switch (turn on ignition if necessary), and then walk round vehicle (as this is a 'tell me' question, you don't need to physically check the lights).","Switch the indicators on, then say you would walk round to check the front, side and rear lights flash.","You only need to explain it."),
 ("Tell me how you'd check the brake lights are working on this car.","Explain you'd operate the brake pedal, make use of reflections in windows or doors, or ask someone to help.","Press the brake pedal and check the lights, using reflections in a window or door, or ask someone to look.","Brake lights warn drivers behind you."),
 ("Tell me how you'd check the power-assisted steering is working before starting a journey.","If the steering becomes heavy, the system may not be working properly. Before starting a journey, 2 simple checks can be made. Gentle pressure on the steering wheel, maintained while the engine is started, should result in a slight but noticeable movement as the system begins to operate. Alternatively turning the steering wheel just after moving off will give an immediate indicator that the power assistance is functioning.","Power steering makes the wheel light. Hold gentle pressure on the wheel while starting the engine and feel it move slightly, or check how it feels as you move off.","Heavy steering is a warning sign."),
 ("Tell me how you'd switch on the rear fog light(s) and explain when you'd use it/them. You don't need to exit the vehicle.","Operate switch (turn on dipped headlights and ignition if necessary). Check warning light is on. Explain use.","Rear fog lights are bright. Switch them on (dipped headlights first in many cars), check the dashboard light, and explain they are for seriously reduced visibility, such as thick fog.","Switch them off when visibility improves, as they can dazzle drivers behind."),
 ("Tell me how you switch your headlight from dipped to main beam and explain how you'd know the main beam is on.","Operate switch (with ignition or engine on if necessary), check with main beam warning light.","Push or pull the light stalk. A blue light on the dashboard shows main beam is on.","Dip main beam for oncoming traffic and when following other vehicles."),
 ("Open the bonnet and tell me how you'd check that the engine has sufficient oil.","Identify dipstick/oil level indicator, describe check of oil level against the minimum and maximum markers.","Find the dipstick, pull it out and wipe it, put it back, pull it out again and check the level sits between minimum and maximum.","You need to open the bonnet for this one. Do it with the engine off and cool."),
 ("Open the bonnet and tell me how you'd check that the engine has sufficient engine coolant.","Identify high and low level markings on header tank where fitted or radiator filler cap, and describe how to top up to correct level.","Find the coolant tank and check the level between the high and low marks.","Never open a hot cooling system. Wait until the engine is cool."),
 ("Open the bonnet and tell me how you'd check that you have a safe level of hydraulic brake fluid.","Identify reservoir, check level against high and low markings.","Find the brake fluid reservoir and check the fluid is between the high and low marks.","A falling level can point to a leak or worn pads. Get it checked."),
]
SHOW = [
 ("When it's safe to do so, can you show me how you wash and clean the rear windscreen?","Find the rear washer/wiper control (it varies between cars) and use it. Check where it is before test day."),
 ("When it's safe to do so, can you show me how you wash and clean the front windscreen?","Use the wiper stalk to operate the washers and wipers. Find the setting for your car."),
 ("When it's safe to do so, can you show me how you'd switch on your dipped headlights?","Operate the light switch and point to the dashboard light that confirms it."),
 ("When it's safe to do so, can you show me how you'd set the rear demister?","Find the heated rear window button and press it. Know which symbol it uses."),
 ("When it's safe to do so, can you show me how you'd operate the horn?","Press the horn button. Do it only when safe and when it will not startle other road users."),
 ("When it's safe to do so, can you show me how you'd demist the front windscreen?","Set the fan, temperature, air direction (screen) and air conditioning if needed. Controls differ by car."),
 ("When it's safe to do so, can you show me how you'd open and close the side window?","Use the window switch. Find which button is yours."),
]

QUIZ = [  # first option is always the correct one (JS shuffles)
 ("What is the minimum legal tyre tread depth for a car?",["1.6mm across the central three-quarters of the tyre","1.0mm across the whole width","3mm in winter","There is no legal minimum"],"The legal minimum is 1.6mm across the central three-quarters of the tyre and around the whole circumference."),
 ("What is the national speed limit for a car on a single carriageway road, unless signs show otherwise?",["60 mph","50 mph","70 mph","40 mph"],"60 mph applies on single carriageways, 70 mph on dual carriageways and motorways, unless signs say otherwise."),
 ("In good conditions, a car doing 30 mph has a typical overall stopping distance of about:",["23 metres","12 metres","40 metres","6 metres"],"The Highway Code gives 23 metres: 9 for thinking distance and 14 for braking."),
 ("On a wet road, stopping distances should be expected to be:",["At least double","About the same","A little shorter","Halved"],"Tyres have less grip on wet roads, so you need at least double the gap."),
 ("When should you use rear fog lights?",["When visibility is seriously reduced","Whenever it is raining","At night on any road","When towing"],"Use them only when visibility is seriously reduced, and turn them off when it improves."),
 ("Learner car drivers may use a motorway:",["Only with an approved instructor in a dual-control car","Never","With any adult in the car","Only during daylight"],"Learners can use motorways only with an approved driving instructor in a car with dual controls."),
 ("What is the minimum pass mark for the theory test multiple-choice section?",["43 out of 50","35 out of 50","50 out of 50","40 out of 50"],"You need at least 43 out of 50 correct to pass."),
 ("You are approaching a zebra crossing and a pedestrian has stepped onto it. You should:",["Slow down and stop to let them cross","Sound your horn","Speed up to pass","Flash your lights and continue"],"Give way to anyone who has stepped onto a zebra crossing."),
 ("Which is the safest following gap in good conditions?",["At least a two-second gap","A one-second gap","Half a second","As close as the car allows"],"Stay back at least two seconds, and more in poor weather."),
 ("Holding a mobile phone while driving is:",["Illegal, even when stopped at traffic lights","Allowed at traffic lights","Allowed for short calls","Allowed if you use only one hand"],"Using a hand-held phone while driving is illegal, including when queuing or stopped at lights."),
]

DICT = [
 ("Biting point","The point where the clutch plates begin to connect and the car starts to move. You feel the engine note change slightly."),
 ("Blind spot","An area around the car you cannot see in your mirrors. Check it by looking over your shoulder before moving off or changing position."),
 ("Box junction","A junction marked with yellow criss-cross lines. Do not enter unless your exit is clear (you may wait to turn right if only oncoming traffic stops you)."),
 ("Carriageway","The part of the road used by vehicles. A dual carriageway has a central reservation separating the two directions."),
 ("Clutch control","Using the clutch pedal smoothly to control the car's speed at very low speeds, for example when manoeuvring."),
 ("Dual carriageway","A road with a central reservation or barrier separating traffic travelling in opposite directions."),
 ("Emerging","Pulling out from a junction onto another road. Look carefully, then go only when it is safe."),
 ("Hazard","Anything that may require you to change speed or direction, such as a pedestrian stepping out or a parked car door opening."),
 ("Independent driving","A part of the practical test where you drive for a while without step-by-step directions, following signs or a sat nav."),
 ("Junction","A place where two or more roads meet. Examples include T-junctions, crossroads and roundabouts."),
 ("National speed limit","The maximum speed for the type of road and vehicle when no other limit is shown. For cars it is 60 mph on single carriageways and 70 mph on dual carriageways and motorways."),
 ("Observation","Looking around you, ahead, to the sides and in mirrors, to understand what is going on and plan ahead."),
 ("Roundabout","A junction where traffic moves around a central island. Give way to traffic from the right unless signs or markings say otherwise."),
 ("Serious fault","A driving fault that is potentially dangerous. It fails the test."),
 ("Stopping distance","The distance you travel while you react (thinking distance) plus the distance you travel once you brake (braking distance)."),
 ("Undue hesitation","Waiting when it is safe to go, so you hold up other road users."),
]

LC_CATS = [  # slug, title, blurb, live?
 ("show-me-tell-me","Show Me, Tell Me questions","All 21 official vehicle safety questions with explanations and flashcard revision.",True),
 ("theory-test","Theory test","How the theory test works, plus an unofficial practice quiz.",True),
 ("practical-test","Practical test","What happens on test day and how the examiner marks your driving.",True),
 ("driving-dictionary","Driving dictionary","A searchable glossary of driving terms in plain English.",True),
 ("test-centres","Test centres","How to find your official theory and practical test centre.",True),
 ("how-to-drive","How to drive a car","Cockpit drill, controls, moving off and junctions.",False),
 ("manoeuvres","Manoeuvres","Parallel parking, bay parking and reversing.",False),
 ("hazard-perception","Hazard perception","Developing hazards and how to practise.",False),
 ("independent-driving","Independent driving","Following signs and sat navs.",False),
 ("adverse-weather","Adverse weather","Rain, fog, snow and ice.",False),
 ("driving-laws","Driving laws","Speed limits, phones, insurance and penalty points.",False),
 ("car-insurance","Car insurance","How cover works for first-time drivers.",False),
 ("disabilities","Driving with disabilities","Adaptations, medical rules and support.",False),
]

# ---------- TEMPLATE ----------
def base_of(path): return "../" * path.count("/")
def nav(b, cur):
    items = [("","Home"),("about/","About"),("services/","Services"),("areas/","Areas"),("learning-centre/","Learning Centre"),("success-stories/","Success stories"),("faq/","FAQ")]
    li = "".join('<li><a href="%s%s"%s>%s</a></li>' % (b, u, ' aria-current="page"' if u == cur else "", t) for u, t in items)
    return li + '<li><a class="call" href="tel:%s">Call %s</a></li>' % (PHONE_T, PHONE_D)

def crumbs(b, trail):
    s = '<nav class="crumbs wrap" aria-label="Breadcrumb"><a href="%s">Home</a>' % (b or "./")
    for u, t in trail: s += ' / ' + ('<a href="%s%s">%s</a>' % (b, u, t) if u else '<span aria-current="page">%s</span>' % t)
    return s + "</nav>"

def page(path, title, desc, body, cur="", trail=None, head="", foot="", register=True):
    b = base_of(path + "x") if path else ""
    url = SITE_URL.rstrip("/") + "/" + path.replace("index.html", "")
    ld = {"@context":"https://schema.org","@type":"LocalBusiness","name":"Road Safety Expert Driving School","url":SITE_URL,"telephone":PHONE_T,"email":EMAIL,"areaServed":AREAS,"founder":{"@type":"Person","name":"Atta Ur Rahman"}}
    h = '''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title><meta name="description" content="%s"><link rel="canonical" href="%s">
<meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:type" content="website"><meta property="og:url" content="%s"><meta property="og:image" content="%sassets/images/logo.png">
<meta name="theme-color" content="#0c2951"><link rel="icon" href="%sassets/images/logo.png"><link rel="stylesheet" href="%scss/style.css">%s
<script type="application/ld+json">%s</script></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap"><a class="logo" href="%s"><img src="%sassets/images/logo.png" alt="Road Safety Expert Driving School home" width="88" height="50"></a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav-list">Menu</button><nav aria-label="Main"><ul id="nav-list">%s</ul></nav></div></header>
%s<main id="main">%s</main>
<footer class="site"><div class="wrap"><div class="cols">
<div><h2>Road Safety Expert Driving School</h2><p>Friendly, personalised driving lessons in West and North West London.</p><p><a href="tel:%s">%s</a><br><a href="mailto:%s">%s</a></p></div>
<div><h2>Explore</h2><ul><li><a href="%sservices/">Lessons and services</a></li><li><a href="%sareas/">Areas we cover</a></li><li><a href="%slearning-centre/">Learning Centre</a></li><li><a href="%ssuccess-stories/">Success stories</a></li><li><a href="%sfaq/">FAQ</a></li></ul></div>
<div><h2>Areas</h2><p>%s and surrounding locations.</p></div>
<div><h2>Legal</h2><ul><li><a href="%sprivacy/">Privacy and cookies</a></li><li><a href="%sterms/">Website terms</a></li></ul></div></div>
<p class="small">&copy; 2026 Road Safety Expert Driving School. Learning Centre content is educational guidance, not official DVSA material.</p></div></footer>
<button class="btn sm" id="top" hidden onclick="scrollTo({top:0})" style="position:fixed;right:1rem;bottom:1rem">Back to top</button>
<script src="%sjs/main.js" defer></script>%s</body></html>'''
    h = h % (E(title), E(desc), url, E(title), E(desc), url, SITE_URL.rstrip("/") + "/", b, b, head, json.dumps(ld),
             b or "./", b, nav(b, cur), crumbs(b, trail) if trail else "", body, PHONE_T, PHONE_D, EMAIL, EMAIL, b, b, b, b, b, ", ".join(AREAS), b, b, b, foot)
    full = os.path.join(ROOT, path or "index.html")
    if not full.endswith(".html"): full = os.path.join(full, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(h)
    if register: pages.append((path.replace("index.html", ""), title))

def cta(b, text="Ready to start learning?"):
    return '<section class="cta"><div class="wrap"><h2>%s</h2><p>Call or email to ask about lessons and availability in your area.</p><div class="btns"><a class="btn" href="tel:%s">Call %s</a><a class="btn alt" href="mailto:%s?subject=Driving%%20lesson%%20enquiry">Email us</a></div></div></section>' % (text, PHONE_T, PHONE_D, EMAIL)

def head(t, p): return '<div class="pagehead"><div class="wrap"><h1>%s</h1><p>%s</p></div></div>' % (t, p)
def faq_html(items): return "".join("<details><summary>%s</summary><div><p>%s</p></div></details>" % (E(q), E(a)) for q, a in items)
def img(name, alt, thumb=True, lazy=True, w=420, h=560):
    return '<img src="%s" alt="%s" width="%d" height="%d"%s>' % ("%s", E(alt), w, h, ' loading="lazy"' if lazy else "")

def photo(b, n, alt, thumb=False, lazy=True):
    f = "%sassets/images/%s%s.webp" % (b, n, "-thumb" if thumb else "")
    return '<img src="%s" alt="%s" width="%d" height="%d"%s>' % (f, E(alt), 420 if thumb else 765, 560 if thumb else 1020, ' loading="lazy"' if lazy else "")

def gal_button(b, n, alt, thumb=True):
    return '<button type="button" data-lb="%sassets/images/%s.webp" data-alt="%s" aria-label="Enlarge photo: %s">%s</button>' % (b, n, E(alt), E(alt), photo(b, n, alt, True))

LB = '''<dialog class="lb" id="lb" aria-label="Photo viewer"><div class="lb-bar"><button id="lb-prev">Previous</button><span id="lb-cap" aria-live="polite"></span><button id="lb-next">Next</button><button id="lb-close">Close</button></div><img alt="" src=""></dialog>'''

# ---------- PAGES ----------
# Home
svc_cards = "".join('<div class="card red"><h3>%s</h3><p>%s</p></div>' % (t, d.split(". ")[0].rstrip(".") + ".") for t, d, *_ in SERVICES[:7])
why = [("Personalised instruction","Every lesson is tailored to your pace, strengths and the areas you want to improve."),("Friendly and patient","Calm, clear communication so you feel supported behind the wheel."),("Support for nervous learners","We talk through each step before you do it."),("Real-world experience","Practical skills for everyday roads, not only for the test."),("Test preparation","Mock tests and guidance that match what you need.")]
learn = [("Show Me, Tell Me","learning-centre/show-me-tell-me/"),("Theory practice quiz","learning-centre/theory-test/"),("Practical test guide","learning-centre/practical-test/"),("Driving dictionary","learning-centre/driving-dictionary/")]
home = '''<section class="hero"><div class="wrap"><div><div class="dash"></div><h1>Learn to drive with confidence in West London</h1>
<p class="lead">Road Safety Expert Driving School gives friendly, personalised manual and automatic lessons, from first-timers to test-ready learners.</p>
<div class="btns"><a class="btn" href="#enquire">Enquire about lessons</a><a class="btn alt" href="learning-centre/">Free Learning Centre</a></div></div>
<figure>%s<figcaption>Passed with Road Safety Expert</figcaption></figure></div></section>
<section class="s"><div class="wrap"><h2>Why choose RSE Driving School?</h2><div class="grid">%s</div></div></section>
<section class="s alt"><div class="wrap"><h2>Lessons and services</h2><div class="grid">%s</div><div class="btns"><a class="btn alt" href="services/">See all services</a></div></div></section>
<section class="s"><div class="wrap"><h2>Meet the instructors</h2><div class="grid">
<div class="person"><div class="avatar" aria-hidden="true">AR</div><div><h3>Atta Ur Rahman</h3><p>Owner and founder, with over 10 years of experience as a professional instructor. Known for a friendly approach to comprehensive driving tuition.</p></div></div>
<div class="person"><div class="avatar" aria-hidden="true">RB</div><div><h3>Rizwan Butt</h3><p>Instructor who specialises in helping learners pass with ease and build safe driving habits.</p></div></div></div>
<p style="margin-top:1rem"><a href="about/">More about the school</a></p></div></section>
<section class="s alt"><div class="wrap"><h2>Our students' success stories</h2><p>Every pass is a result of a learner's hard work. Here are some of our recent successes.</p>
<div class="gallery home-gal">%s</div><div class="btns"><a class="btn" href="#enquire">Start your driving journey</a><a class="btn alt" href="success-stories/">View all passes</a></div></div></section>
<section class="s"><div class="wrap"><h2>Areas we cover</h2><ul class="areas">%s</ul><p>Plus surrounding locations. If your area isn't listed, get in touch as we may still be able to help.</p><a href="areas/">Areas page</a></div></section>
<section class="s alt"><div class="wrap"><h2>Free Learning Centre</h2><p>Free guides, flashcards and a practice quiz. No account needed.</p><div class="grid">%s</div><div class="btns"><a class="btn" href="learning-centre/">Open the Learning Centre</a></div></div></section>
<section class="s"><div class="wrap"><h2>Common questions</h2>%s<p style="margin-top:1rem"><a href="faq/">All FAQs</a></p></div></section>
<div id="enquire">%s</div>%s''' % (
    photo("", "pass-test-centre", "", False, False).replace("%s", "") if False else photo("", "pass-test-centre", PHOTOS[0][1], False, False),
    "".join('<div class="card"><h3>%s</h3><p>%s</p></div>' % x for x in why), svc_cards,
    "".join(gal_button("", n, a) for n, a, ok in OK_PHOTOS[:3]), "".join("<li>%s</li>" % a for a in AREAS),
    "".join('<a class="card" href="%s"><h3>%s</h3></a>' % (u, t) for t, u in learn), faq_html(FAQ[:5]), cta(""), LB)
page("index.html", "Driving Lessons in West & North West London | Road Safety Expert Driving School", "Friendly manual and automatic driving lessons across West and North West London, plus a free Learning Centre for learner drivers.", home, "")

# About
page("about/index.html", "About Us | Road Safety Expert Driving School", "Meet Atta Ur Rahman and Rizwan Butt and learn how Road Safety Expert Driving School teaches safe, confident drivers.", head("About us", "Friendly, personalised lessons that build safe drivers for life.") + '''<section class="s"><div class="wrap"><h2>Our approach</h2>
<p>Road Safety Expert Driving School was founded by Atta Ur Rahman, out of a passion for teaching safe driving. He saw the need for a school that put personalised instruction and student-centred learning first.</p>
<p>We focus on more than passing your test. Our goal is a confident, safe and independent driver. Lessons are adapted to your pace, strengths and areas for improvement, with calm, clear communication.</p>
<p>Our instructors are friendly, professional and speak multiple languages, so learners from all backgrounds feel comfortable. <em>[Owner: confirm which languages to list.]</em></p>
<h2>Instructors</h2><div class="grid"><div class="person"><div class="avatar" aria-hidden="true">AR</div><div><h3>Atta Ur Rahman</h3><p>Owner and professional instructor with over 10 years of experience, dedicated to comprehensive tuition with a friendly approach.</p></div></div>
<div class="person"><div class="avatar" aria-hidden="true">RB</div><div><h3>Rizwan Butt</h3><p>Instructor who specialises in helping learners pass with ease and developing safe driving habits.</p></div></div></div></div></section>''' + cta("", "Talk to us about lessons"), "about/", [("", "About us")])

# Services
sv = "".join('<section class="s%s" id="%s"><div class="wrap"><h2>%s</h2><p>%s</p><p><strong>Suitable for:</strong> %s</p><p><strong>What to expect:</strong> %s</p><a class="btn sm" href="mailto:%s?subject=%s%%20enquiry">Enquire about this</a></div></section>' % (" alt" if i % 2 else "", t.lower().replace(" ", "-"), t, d, s, w, EMAIL, t.replace(" ", "%20")) for i, (t, d, s, w) in enumerate(SERVICES))
page("services/index.html", "Driving Lessons & Services | Road Safety Expert Driving School", "Manual and automatic lessons, refresher lessons, mock tests, test day car hire, Pass Plus and theory support.", head("Lessons and services", "Prices are available on request. Please call or email.") + sv + cta("", "Ask about availability"), "services/", [("", "Services")])

# Areas
page("areas/index.html", "Driving Lessons in Ealing, Harrow, Wembley & More | Areas We Cover", "Driving lessons across West and North West London including Mill Hill, Greenford, Hendon, Pinner, Harrow, Wembley, Northolt, Ruislip, Ealing, Perivale, Kingsbury and Stanmore.", head("Areas we cover", "Automatic and manual lessons across West and North West London.") + '<section class="s"><div class="wrap"><p>We currently teach in the areas below, with more being added. Our instructors know the local roads, busy junctions and quiet residential practice areas.</p><ul class="areas">' + "".join("<li>%s</li>" % a for a in AREAS) + '</ul><h2>Not sure if you are covered?</h2><p>We also teach in surrounding locations. Send us your postcode and we will tell you if we can help, including pick-up options.</p><div class="btns"><a class="btn" href="tel:%s">Call %s</a><a class="btn alt" href="mailto:%s?subject=Postcode%%20check">Email your postcode</a></div></div></section>' % (PHONE_T, PHONE_D, EMAIL), "areas/", [("", "Areas")])

# FAQ
page("faq/index.html", "Driving Lesson FAQs | Road Safety Expert Driving School", "Answers to common questions about driving lessons, tests, car hire and booking.", head("Frequently asked questions", "Anything else? Call or email us.") + '<section class="s"><div class="wrap">%s</div></section>' % faq_html(FAQ) + cta("", "Still have a question?"), "faq/", [("", "FAQ")])

# Success
cards = "".join('<li style="list-style:none">%s</li>' % gal_button("../", n, a) for n, a, ok in OK_PHOTOS)
page("success-stories/index.html", "Student Success Stories | Road Safety Expert Driving School", "Photos of learners who passed their driving test with Road Safety Expert Driving School.", head("Student success stories", "Congratulations to every learner who passed.") + '<section class="s"><div class="wrap"><p>Select a photo to enlarge it. Use the arrow keys to move between photos.</p><ul class="gallery" style="padding:0">%s</ul><div class="btns"><a class="btn" href="mailto:%s?subject=Driving%%20lesson%%20enquiry">Start your driving journey</a></div></div></section>' % (cards, EMAIL) + LB + cta("", "Want to be next?"), "success-stories/", [("", "Success stories")])

# Learning centre index
idx = []
def add(t, u, c, k=""): idx.append({"t": t, "u": u, "c": c, "k": k})
cc = ""
for s, t, d, live in LC_CATS:
    if live:
        cc += '<a class="card" href="%s/"><h3>%s</h3><p>%s</p></a>' % (s, t, d); add(t, "learning-centre/%s/" % s, "Category", d)
    else:
        cc += '<div class="card soon"><h3>%s</h3><p>%s</p><span class="tag">Coming soon</span></div>' % (t, d)
for i, (q, *_ ) in enumerate(TELL): add(q, "learning-centre/show-me-tell-me/#tell-%d" % (i + 1), "Tell me")
for i, (q, _) in enumerate(SHOW): add(q, "learning-centre/show-me-tell-me/#show-%d" % (i + 1), "Show me")
for t, d in DICT: add(t, "learning-centre/driving-dictionary/#" + t.lower().replace(" ", "-"), "Dictionary", d)
add("Theory practice quiz", "learning-centre/theory-test/#quiz", "Quiz", "practice questions revision")
open(os.path.join(ROOT, "js", "search-index.js"), "w").write("window.SEARCH_INDEX=" + json.dumps(idx) + ";")
lcbody = head("Learning Centre", "Free guides and revision tools for UK learner drivers. No account needed.") + '''<section class="s"><div class="wrap"><form id="lc-form" role="search" class="search"><label for="lc-search" class="skip" style="position:static;width:0;height:0;overflow:hidden;padding:0">Search</label><input id="lc-search" type="search" placeholder="Search, e.g. tyre, roundabout, biting point" autocomplete="off"><button class="btn" type="submit">Search</button></form>
<p id="result-status" aria-live="polite" style="margin-top:1rem"></p><ul id="results"></ul>
<h2 style="margin-top:2rem">Browse by topic</h2><div class="grid">%s</div>
<div class="note"><p>More topics are being added. Our content is educational guidance written by the school. Always check official GOV.UK and DVSA information for the latest rules.</p></div></div></section>''' % cc + cta("", "Want a real instructor beside you?")
page("learning-centre/index.html", "Free Learning Centre for Learner Drivers | Road Safety Expert", "Free guides, Show Me Tell Me flashcards, a theory practice quiz and a driving dictionary.", lcbody, "learning-centre/", [("", "Learning Centre")], foot='<script>var SITE_BASE="../";</script><script src="../js/search-index.js"></script>')

LC = [("learning-centre/", "Learning Centre")]
def related(b): return '<div class="note"><p><a href="%s">Back to the Learning Centre</a> | <a href="mailto:%s?subject=Driving%%20lesson%%20enquiry">Enquire about lessons</a></p></div>' % (b + "learning-centre/", EMAIL)

# Show me tell me
def qa(kind, i, q, ans, simple, note):
    return '<div class="qa" id="%s-%d" data-type="%s" data-q="%s" data-a="%s"><details><summary>%s</summary><div><div class="off"><strong>Official answer (DVSA):</strong> %s</div><p><strong>In plain English:</strong> %s</p><p><strong>Safety:</strong> %s</p></div></details></div>' % (kind, i, kind, E(q), E(ans), E(q), E(ans) if ans else "", E(simple), E(note))
tell = "".join(qa("tell", i + 1, q, a, s, n) for i, (q, a, s, n) in enumerate(TELL))
show = "".join(qa("show", i + 1, q, "Not published by DVSA. School guidance: " + g, g, "Only do this when it is safe. The examiner will mark you down if your driving becomes dangerous while you answer.").replace('<strong>Official answer (DVSA):</strong> Not published by DVSA. School guidance: ' + E(g), '<strong>What to do (school guidance, not an official DVSA answer):</strong> ' + E(g)) for i, (q, g) in enumerate(SHOW))
smt = head("Show Me, Tell Me questions", "All 21 official car vehicle safety questions, with explanations and flashcards.") + '''<section class="s"><div class="wrap">
<p>You are asked two vehicle safety questions on your car test: a <strong>tell me</strong> question before you drive and a <strong>show me</strong> question while driving. A wrong answer to one or both is one driving fault. You fail if your driving becomes dangerous or potentially dangerous while answering the show me question.</p>
<div class="note"><p>Question wording and tell me answers are from the official DVSA list on GOV.UK (reproduced under the Open Government Licence v3.0, list last updated 4 December 2017). DVSA publishes no answers for the show me questions, so our notes on those are school guidance only. Controls differ between cars, so learn yours. <a href="https://www.gov.uk/government/publications/car-show-me-tell-me-vehicle-safety-questions/car-show-me-tell-me-vehicle-safety-questions">Check the official list</a>.</p></div>
<h2>Flashcard revision</h2><div class="fc" id="fc"><p><label for="fc-type">Practise: </label><select id="fc-type"><option value="all">All questions</option><option value="tell">Tell me only</option><option value="show">Show me only</option></select> <button class="btn alt sm" id="fc-shuffle" type="button">Shuffle</button></p>
<p id="fc-stat" aria-live="polite"></p><h3 id="fc-q">Loading...</h3><div class="a" id="fc-a" hidden></div><button class="btn" id="fc-reveal" type="button">Reveal answer</button>
<div id="fc-rate" hidden><button class="btn" id="fc-known" type="button">I knew it</button> <button class="btn alt" id="fc-again" type="button">Review again</button></div></div>
<noscript><p>Flashcards need JavaScript. The full list is below.</p></noscript>
<h2 style="margin-top:2.5rem">Tell me questions (14)</h2>%s<h2 style="margin-top:2.5rem">Show me questions (7)</h2>%s%s</div></section>''' % (tell, show, related("../../"))
page("learning-centre/show-me-tell-me/index.html", "Show Me, Tell Me Questions & Flashcards | Road Safety Expert", "All 21 official DVSA car show me tell me questions with plain-English explanations and flashcard revision.", smt, "learning-centre/", LC + [("", "Show Me, Tell Me")])

# Theory
qj = json.dumps([{"q": q, "o": o, "e": e} for q, o, e in QUIZ])
theory = head("Theory test", "How the test works, and an unofficial practice quiz.") + '''<section class="s"><div class="wrap"><h2>How the test works</h2>
<p>The car theory test is multiple choice with 50 questions, and you need at least 43 correct to pass. There is also a separate hazard perception part. Check the current format on <a href="https://www.gov.uk/theory-test">GOV.UK</a> before you book.</p>
<p>Revise the Highway Code, not just practice answers. Understanding why a rule exists makes the answer easier to work out. When a question seems unclear, look for key words and rule out answers that are clearly unsafe.</p>
<h2 id="quiz">Practice quiz</h2><div class="note"><p>This quiz is unofficial. The questions are original, written by our school for revision, and are not DVSA questions.</p></div>
<div class="quiz card" id="quiz"><div id="quiz-box" aria-live="off"><noscript>The quiz needs JavaScript.</noscript></div></div>%s</div></section>''' % related("../../")
page("learning-centre/theory-test/index.html", "Theory Test Guide & Practice Quiz | Road Safety Expert", "Learn how the theory test works and try an unofficial practice quiz with explanations.", theory, "learning-centre/", LC + [("", "Theory test")], foot="<script>window.QUIZ=%s.map(x=>({q:x.q,o:x.o,e:x.e}));</script>" % qj)

# Practical
prac = head("Practical driving test", "What to expect on test day.") + '''<section class="s"><div class="wrap">
<p>This is a plain-English overview. For the full, current rules see <a href="https://www.gov.uk/driving-test">GOV.UK</a>.</p>
<h2>Parts of the test</h2><ul><li>An eyesight check (failing it ends the test).</li><li>Two vehicle safety questions: <a href="../show-me-tell-me/">Show Me, Tell Me</a>.</li><li>General driving ability, including independent driving.</li><li>One reversing manoeuvre.</li></ul>
<h2>Faults</h2><p>Minor mistakes are driving faults and do not on their own fail the test. Serious or dangerous faults do fail it. The examiner stops the test only if they think your driving is a danger to others.</p>
<h2>Preparing</h2><p>Test routes are not published, so you cannot memorise them. Learn to observe and decide for yourself on any road. Practise regularly, take a mock test if you can, and ask your instructor for honest feedback. Nothing can guarantee a pass, but good preparation helps you feel calm.</p>%s</div></section>''' % related("../../")
page("learning-centre/practical-test/index.html", "Practical Driving Test Guide | Road Safety Expert", "A plain-English overview of what happens on the UK practical driving test.", prac, "learning-centre/", LC + [("", "Practical test")])

# Dictionary
dl = "".join('<dt id="%s">%s</dt><dd>%s</dd>' % (t.lower().replace(" ", "-"), t, d) for t, d in DICT)
page("learning-centre/driving-dictionary/index.html", "Driving Dictionary | Road Safety Expert", "Plain-English definitions of common driving terms.", head("Driving dictionary", "Plain-English definitions of driving terms.") + '<section class="s"><div class="wrap"><p class="filter"><label for="dict-filter">Filter terms</label><br><input id="dict-filter" type="search" placeholder="Type a word"></p><p id="dict-count" aria-live="polite">%d terms shown</p><dl id="dict">%s</dl>%s</div></section>' % (len(DICT), dl, related("../../")), "learning-centre/", LC + [("", "Driving dictionary")])

# Test centres
page("learning-centre/test-centres/index.html", "Find a Driving Test Centre | Road Safety Expert", "How to find your official theory or practical driving test centre.", head("Test centres", "Find your official centre.") + '''<section class="s"><div class="wrap"><p>Centres change, so we link to the official service instead of listing addresses here.</p>
<ul><li><a href="https://www.gov.uk/find-driving-test-centre">Find a driving test centre (GOV.UK)</a></li><li><a href="https://www.gov.uk/book-driving-test">Book your driving test (GOV.UK)</a></li></ul>
<h2>Choosing a centre</h2><p>Consider travel time and which centre is nearest to where you practise. Familiar local roads help you feel at ease, but routes vary, so focus on good observation rather than memorising roads. Ask us if you want help deciding.</p>%s</div></section>''' % related("../../"), "learning-centre/", LC + [("", "Test centres")])

# Legal
page("privacy/index.html", "Privacy and Cookies | Road Safety Expert Driving School", "How this website handles your information.", head("Privacy and cookies", "Draft for the owner to review.") + '''<section class="s"><div class="wrap"><div class="note"><p>This policy has not been legally reviewed. Owner: please check and complete the placeholders.</p></div>
<h2>What this website collects</h2><p>This website has no accounts, forms or tracking and sets no cookies. It does not collect personal information itself. If you phone or email us we will use your details only to respond to your enquiry. Quiz and flashcard progress stays in your browser and is not sent anywhere.</p>
<h2>Who is responsible</h2><p>Road Safety Expert Driving School. Contact: %s. [Owner: add registered business name and address.]</p><h2>Your rights</h2><p>You can ask us what information we hold about you and ask us to delete it. You can complain to the Information Commissioner's Office (ico.org.uk).</p></div></section>''' % EMAIL, "", [("", "Privacy")])
page("terms/index.html", "Website Terms | Road Safety Expert Driving School", "Terms of use for this website.", head("Website terms", "Draft for the owner to review.") + '''<section class="s"><div class="wrap"><div class="note"><p>This text has not been legally reviewed. Owner: please check it.</p></div>
<p>Learning Centre material is general educational guidance and is not official DVSA or government content. Rules change, so check GOV.UK. Reading this site does not create a booking or contract. Lessons and prices are agreed directly with the school. We try to keep information accurate but cannot accept responsibility for errors.</p></div></section>''', "", [("", "Terms")])

# 404
page("404.html", "Page not found | Road Safety Expert Driving School", "Page not found.", '<section class="s"><div class="wrap"><h1>Page not found</h1><p>That page does not exist. Try the <a href="./">homepage</a>. If you are on a GitHub project site, use the menu above..</p></div></section>', register=False)

# sitemap, robots
sm = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join("<url><loc>%s/%s</loc></url>" % (SITE_URL.rstrip("/"), p) for p, _ in pages) + "</urlset>"
open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
open(os.path.join(ROOT, "robots.txt"), "w").write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE_URL.rstrip("/"))
open(os.path.join(ROOT, ".nojekyll"), "w").write("")
print("Built", len(pages), "pages")
