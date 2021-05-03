ALIVE = 1
DEAD = 0

story = {
    'start': {
        'text': [
            "You're Huang, a Chinese exchange student on the last day of your stay in Singapore.",
        ],
        'choices': [
            ("beep beep beep...", 'alarm'),
        ]
    },
    'alarm': {
        'text': [
            '"Beep beep beep boom beep beep..."',
            ('the alarm goes off. You wake up from a nap, still carrying a headache from this morning\'s hangover. It takes a'
            'few seconds for you to orient yourself. You take a peek at your phone.'),
            ('\"Oh shit! It\'s 9\". It wasn\'t a nap, it was a coma. You hastily jump out of bed, straight into the shower. You get'
            'dressed, check out of the hotel and head straight to the airport.'),
        ],
        'choices': [
            ("Arrive at the airport", 'airport_arrival'),
        ]
    },
    'airport_arrival': {
        'text': [
            ('You just arrived at the airport. You complete the security process. It\'s 11:35pm. You check your boarding pass - flight'
            ' no. MH370, departure time 12:40am, boarding gates open at 11:55 pm at gate 10.'),
            ('\"Woof, that was fast. I\'ve 20 minutes to spare, let me grab a quck bit.\" You look around and decide to go to Din by'
            'Din Tai Fung or Starbucks.'),
        ],
        'choices': [
            ('Din by Din Tai Fung', 'din_tai_fung'),
            ('Starbucks', 'starbucks'),
        ]
    },
    'starbucks': {
        'text': [
            'You order a chicken panini sandwich with either a regular cafe latte or cafe latte with 3 expresso shots.'
        ],
        'choices': [
            ('Regular cafe latte', 'board_flight'),
            ('Cafe latte with 3 expresso shots', 'rush_to_airport_restroom'),
        ]
    },
    'din_tai_fung': {
        'text': [
            'You order chicken dumplings with soup. It\'s delicious as always. You proceed to Gate 10.',
        ],
        'choices': [
            ('Board the flight', 'board_flight'),
        ]
    },
    'rush_to_airport_restroom': {
        'text': [
            'You digestive system can\'t handle 3 extra shots of espresso. You die due to instant acute diarrhoea.', 
            'RIP, Huang. Lawsuit is filed against Starbucks but their lobbyists help them settle. THE END.',
        ],
        'choices': DEAD
    },
    'board_flight': {
        'text': [
            'You\'ve boarded the flight.', 
            ('\"Welcome aboard Malaysian Airlines...\" and safety instructions follow. In a few moments, the flight takes off.'
            'Seat belts sign\'s off and you decide to sleep or watch the movie Her.'),
        ],
        'choices': [
            ('Sleep', 'sleep'),
            ('Watch the movie Her', 'watch_her'),
        ]
    },
    'sleep': {
        'text': [
            ('It\'s half past one after midnight and the plance inexplicably turns right and nosedives into a stall.'
            'MH370 disappears off the skies. 239 presumed dead. THE END.')
        ],
        'choices': DEAD
    },
    'watch_her': {
        'text': [
            ('\"... and, and this terrible thought -  are these feelings even real or are these programming? The idea really hurts.\"'
            ', Her\'s dialog becomes too overwhelming as you recount your own breakup. You keep watching or pause it ' 
            'and get a cup of coffee.'), 
        ],
        'choices': [
            ('Info about Her', 'her_info'),
            ('Keep watching', 'keep_watching'),
            ('Pause it and get a cup of coffee', 'get_coffee'),
        ]
    },
    'keep_watching': {
        'text': [
            ('The movie finishes off, leaves you in a very desolate state. You can\'t take it anymore and start sobbing. '
            'You open the emergency hatch door and jump off, yelling \"Now, you can never have me, Song!!\".'),
            'THE END.',
        ],
        'choices': DEAD
    },
    'get_coffee': {
        'text': [
            ('You have had too much coffee especially for your sensitive stomach. You rush to the restroom in the front-most '
            'section of the plane next to the cockpit. Flush! and you relieved yourself. As you step out, you hear a squabble ' 
            'from the cockpit. You look around and '),
        ],
        'choices': [
            ('Walk into the cockpit', 'walk_into_cockpit'),
            ('Return to your seat', 'return_seat'),
        ]
    },
    'walk_into_cockpit': {
        'text': [
            ('\"Rescue me from this insane guy. He\'s planning to put in a nose dive and kill all these people." pleads the ' 
            'first officer who was held by his neck by the captain who now threatens you, \"Stay away from this, kid. I just want '
            'to go home.\"'),
            'You decide to ',
        ],
        'choices': [
            ('Help the captain', 'help_captain'),
            ('Help the first officer', 'help_first_officer'),
        ]
    },
    'return_seat': {
        'text': [
            ('You call on the flight attendant or just settle down in your seat.'),
            'You decide to ',
        ],
        'choices': [
            ('Call on the flight attendant', 'call_flight_attendant'),
            ('Just settle down in your seat', 'settle_seat'),
        ]
    },
    'help_first_officer': {
        'text': [
            ('The first officer regained the control of the plane and you two together tied the captain. Upon landing ' 
            'in Beijing, you\'re praised for your heroics and you live to fight another day.'),
            'THE END.',
        ],
        'choices': ALIVE
    },
    'help_captain': {
        'text': [
            ('You hold the first officer\'s lower body as the captain is sealing his mouth with tape. The captain resists both '
            'of you and air-arrests you. You land in Beijing and the police holds you in custody. You\'ve charged with '
            '\"being a accomplice in an attempt to mass murder\". You\'re sentenced for life. You\'ve brought great shame to '
            'your family.'),
            'THE END.',
        ],
        'choices': DEAD
    },
    'call_flight_attendant': {
        'text': [
            ('You describe her what you saw. She reassures you, \"Don\'t worry, I\'ll take a look.\" As she starts retracing '
            'her steps back to the front, you hear a noise.'),
        ],
        'choices': [
            ('Crash!', 'plane_disappear'),
        ]
    },
    'call_flight_attendant': {
        'text': [
            ('You abandon your current thoughts and your mind starts veering towards home cooked food your mother will make for '
            'you on arrival. You hear a noise.'),
        ],
        'choices': [
            ('Crash!', 'plane_disappear'),
        ]
    },
    'plane_disappear': {
        'text': [
            ('The plane starts stalling. Everyone around you starts panicking as you hear the first officer screaming, \"Help! '
            'he\'s locked me out. He wants to kill us all!". It\'s too late, in a matter of moments MH370 disappears from the sky '
            'with 239 passengers.'),
            'THE END.',
        ],
        'choices': DEAD
    },
}
