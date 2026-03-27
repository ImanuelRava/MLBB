import re
import pandas as pd

# The input text from the file (using a string variable here for the script)
input_text = """
==Match Results==
<big> '''[[Special:RunQuery/Draft Generator|Click here to access the Draft Input generator]]'''</big>
===Round 1===
{{Matchlist|id=M7SWISSRD1|title=Round 1 Matches ({{abbr/Bo1}})|width=330px|matchsection=Round 1
|M1header=January 10
|M1={{Match
    |bestof=1|caster1=Laphel|caster2=Gonie|caster3=GideonQ|mvp=Kiboy
    |opponent1={{TeamOpponent|onic}}
    |opponent2={{TeamOpponent|boostgate esports}}
    |date=January 10, 2026 - 14:00{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=vUNv7L87qhw
        |team1side=blue |team2side=red |length=29:04 |winner=1|comment=<b>Flying Cloud</b>
        <!-- Hero picks -->
        |t1h1=uranus |t1h2=yi sun-shin |t1h3=kadita |t1h4=claude |t1h5=kalea
        |t2h1=sora |t2h2=hayabusa |t2h3=valentina |t2h4=karrie |t2h5=khaleed
        <!-- Hero bans -->
        |t1b1=yve |t1b2=selena |t1b3=yu zhong |t1b4=gatotkaca |t1b5=hylos
        |t2b1=zhuxin |t2b2=fanny |t2b3=grock |t2b4=ruby |t2b5=lunox
    }}
}}
|M2={{Match
    |bestof=1|caster1=Laphel|caster2=Gonie|caster3=GideonQ|mvp=Shin
    |opponent1={{TeamOpponent|black sentence esports}}
    |opponent2={{TeamOpponent|cfu gaming}}
    |date=January 10, 2026 - 15:20{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=BXet4JEADb4
        |team1side=red |team2side=blue |length=18:08 |winner=1|comment=<b>Expanding Rivers</b>
        <!-- Hero picks -->
        |t1h1=yu zhong |t1h2=joy |t1h3=yve |t1h4=karrie |t1h5=grock
        |t2h1=gloo |t2h2=lancelot |t2h3=kagura |t2h4=claude |t2h5=chou
        <!-- Hero bans -->
        |t1b1=zhuxin |t1b2=sora |t1b3=hilda |t1b4=valentina |t1b5=lapu-lapu
        |t2b1=fanny |t2b2=yi sun-shin |t2b3=kalea |t2b4=fredrinn |t2b5=phoveus
    }}
}}
|M3={{Match
    |bestof=1|caster1=Laphel|caster2=Gonie|caster3=GideonQ|mvp=Blink (Burmese_player)
    |opponent1={{TeamOpponent|team zone}}
    |opponent2={{TeamOpponent|yangon galacticos}}
    |date=January 10, 2026 - 16:25{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=zXLZ0qDU83s
        |team1side=red |team2side=blue |length=20:03 |winner=2|comment=<b>Broken Walls</b>
        <!-- Hero picks -->
        |t1h1=yu zhong |t1h2=joy |t1h3=lunox |t1h4=claude |t1h5=gatotkaca
        |t2h1=benedetta |t2h2=baxia |t2h3=zhuxin |t2h4=harith |t2h5=helcurt
        <!-- Hero bans -->
        |t1b1=grock |t1b2=sora |t1b3=yve |t1b4=lapu-lapu |t1b5=arlott
        |t2b1=kalea |t2b2=lancelot |t2b3=yi sun-shin |t2b4=leomord |t2b5=hayabusa
    }}
}}
|M4={{Match
    |bestof=1|caster1=Laphel|caster2=Gonie|caster3=GideonQ|mvp=Trolll
    |opponent1={{TeamOpponent|dfyg}}
    |opponent2={{TeamOpponent|team falcons}}
    |date=January 10, 2026 - 17:25{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=_mSPcv89RoA
        |team1side=red |team2side=blue |length=27:27 |winner=2|comment=<b>Broken Walls</b>
        <!-- Hero picks -->
        |t1h1=yu zhong |t1h2=yi sun-shin |t1h3=pharsa |t1h4=ruby |t1h5=chou
        |t2h1=lapu-lapu |t2h2=fredrinn |t2h3=yve |t2h4=moskov |t2h5=mathilda
        <!-- Hero bans -->
        |t1b1=zhuxin |t1b2=sora |t1b3=kalea |t1b4=arlott |t1b5=uranus
        |t2b1=fanny |t2b2=lancelot |t2b3=esmeralda |t2b4=claude |t2b5=valentina
    }}
}}
|M5={{Match
    |bestof=1|caster1=Reptar|caster2=Mirko|caster3=Naisou|mvp=Sunset Lover
    |opponent1={{TeamOpponent|evil}}
    |opponent2={{TeamOpponent|team spirit}}
    |date=January 10, 2026 - 18:35{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=ebkTT9Hmu-U
        |team1side=blue |team2side=red |length=14:03 |winner=2|comment=<b>Expanding Rivers</b>
        <!-- Hero picks -->
        |t1h1=yu zhong |t1h2=yi sun-shin |t1h3=valentina |t1h4=claude |t1h5=tigreal
        |t2h1=uranus |t2h2=nolan |t2h3=pharsa |t2h4=karrie |t2h5=chou
        <!-- Hero bans -->
        |t1b1=zhuxin |t1b2=hilda |t1b3=fanny |t1b4=guinevere |t1b5=baxia
        |t2b1=lancelot |t2b2=kalea |t2b3=yve |t2b4=grock |t2b5=gatotkaca
    }}
}}
|M6={{Match
    |bestof=1|caster1=Reptar|caster2=Mirko|caster3=Naisou|mvp=Kramm
    |opponent1={{TeamOpponent|srg.og}}
    |opponent2={{TeamOpponent|cg esports}}
    |date=January 10, 2026 - 19:30{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=94AmjNwwrsI
        |team1side=blue |team2side=red |length=14:44 |winner=1|comment=<b>Broken Walls</b>
        <!-- Hero picks -->
        |t1h1=phoveus |t1h2=lancelot |t1h3=zhuxin |t1h4=granger |t1h5=kalea
        |t2h1=yu zhong |t2h2=freya |t2h3=kimmy |t2h4=harith |t2h5=gatotkaca
        <!-- Hero bans -->
        |t1b1=lunox |t1b2=fanny |t1b3=yve |t1b4=hayabusa |t1b5=joy
        |t2b1=sora |t2b2=grock |t2b3=yi sun-shin |t2b4=karrie |t2b5=lapu-lapu
    }}
}}
|M7={{Match
    |bestof=1|caster1=Reptar|caster2=Mirko|caster3=Naisou|mvp=Sanji
    |opponent1={{TeamOpponent|aurora gaming ph}}
    |opponent2={{TeamOpponent|team liquid ph}}
    |date=January 10, 2026 - 20:30{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=YwTb_JeyQx0
        |team1side=blue |team2side=red |length=16:54 |winner=2|comment=<b>Flying Cloud</b>
        <!-- Hero picks -->
        |t1h1=uranus |t1h2=fredrinn |t1h3=yve |t1h4=karrie |t1h5=chou
        |t2h1=alice |t2h2=yi sun-shin |t2h3=luo yi |t2h4=claude |t2h5=hylos
        <!-- Hero bans -->
        |t1b1=yu zhong |t1b2=hilda |t1b3=lancelot |t1b4=pharsa |t1b5=sora
        |t2b1=kalea |t2b2=zhuxin |t2b3=grock |t2b4=lapu-lapu |t2b5=arlott
    }}
}}
|M8={{Match
    |bestof=1|caster1=Reptar|caster2=Mirko|caster3=Naisou|mvp=Yazukee
    |opponent1={{TeamOpponent|alter ego}}
    |opponent2={{TeamOpponent|aurora gaming}}
    |date=January 10, 2026 - 21:35{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=UUSh-QhZjEk
        |team1side=blue |team2side=red |length=25:25 |winner=1|comment=<b>Broken Walls</b>
        <!-- Hero picks -->
        |t1h1=cici |t1h2=leomord |t1h3=zhuxin |t1h4=freya |t1h5=hylos
        |t2h1=sora |t2h2=nolan |t2h3=novaria |t2h4=claude |t2h5=gatotkaca
        <!-- Hero bans -->
        |t1b1=selena |t1b2=fanny |t1b3=yve |t1b4=lunox |t1b5=guinevere
        |t2b1=kimmy |t2b2=hilda |t2b3=grock |t2b4=kalea |t2b5=valentina
    }}
}}
}}
* {{Bgcolortext|up|Winner}} will advance to Round 2: High (1-0)
* {{Bgcolortext|down|Loser}} will advance to Round 2: Low (0-1)

===Round 2===
{{box|start|padding=2em}}
====High (1-0)====
{{Matchlist|id=M7SWISSR20|title=Round 2 Matches ({{abbr/Bo1}})|width=330px|matchsection=Round 2
|M1header=January 11
|M1={{Match
    |bestof=1|caster1=Laphel|caster2=GideonQ|caster3=Arashi|mvp=Sanji
    |opponent1={{TeamOpponent|team falcons}}
    |opponent2={{TeamOpponent|team liquid ph}}
    |date=January 11, 2026 - 15:50 {{Abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=KYyGh1RLIAM
        |team1side=red |team2side=blue |length=15:06 |winner=2|comment=<b>Broken Walls</b>
        <!-- Hero picks -->
        |t1h1=sora |t1h2=akai |t1h3=valentina |t1h4=granger |t1h5=mathilda
        |t2h1=phoveus |t2h2=nolan |t2h3=pharsa |t2h4=claude |t2h5=gatotkaca
        <!-- Hero bans -->
        |t1b1=yu zhong |t1b2=lancelot |t1b3=zhuxin |t1b4=luo yi |t1b5=hayabusa
        |t2b1=kalea |t2b2=yve |t2b3=fredrinn |t2b4=baxia |t2b5=karrie
    }}
}}
|M2={{Match
    |bestof=1|caster1=Laphel|caster2=GideonQ|caster3=Arashi|mvp=Nino
    |opponent1={{TeamOpponent|black sentence esports}}
    |opponent2={{TeamOpponent|alter ego}}
    |date=January 11, 2026 - 16:45 {{Abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=y6P6MZ5o5IE
        |team1side=red |team2side=blue |length=12:24 |winner=2|comment=<b>Dangerous Grass</b>
        <!-- Hero picks -->
        |t1h1=hilda |t1h2=yi sun-shin |t1h3=yve |t1h4=granger |t1h5=akai
        |t2h1=lapu-lapu |t2h2=fanny |t2h3=pharsa |t2h4=claude |t2h5=grock
        <!-- Hero bans -->
        |t1b1=zhuxin |t1b2=leomord |t1b3=sora |t1b4=uranus |t1b5=yu zhong
        |t2b1=baxia |t2b2=esmeralda |t2b3=valentina |t2b4=karrie |t2b5=harith
    }}
}}
|M3={{Match
    |bestof=1|caster1=Reptar|caster2=Mirko|caster3=Naisou|mvp=Innocent
    |opponent1={{TeamOpponent|selangor red giants}}
    |opponent2={{TeamOpponent|team spirit}}
    |date=January 11, 2026 - 18:45 {{Abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=InDJsefR7o8
        |team1side=blue |team2side=red |length=13:11 |winner=1|comment=<b>Expanding Rivers</b>
        <!-- Hero picks -->
        |t1h1=lapu-lapu |t1h2=joy |t1h3=selena |t1h4=claude |t1h5=chou
        |t2h1=uranus |t2h2=yi sun-shin |t2h3=pharsa |t2h4=karrie |t2h5=khaleed
        <!-- Hero bans -->
        |t1b1=fanny |t1b2=yve |t1b3=hilda |t1b4=grock |t1b5=kaja
        |t2b1=kalea |t2b2=zhuxin |t2b3=lancelot |t2b4=valentina |t2b5=kimmy
    }}
}}
|M4={{Match
    |bestof=1|caster1=Reptar|caster2=Mirko|caster3=Naisou|mvp=Ying
    |opponent1={{TeamOpponent|onic}}
    |opponent2={{TeamOpponent|yangon galacticos}}
    |date=January 11, 2026 - 19:40 {{Abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=bB4waJw7C68
        |team1side=blue |team2side=red |length=14:11 |winner=2|comment=<b>Broken Walls</b>
        <!-- Hero picks -->
        |t1h1=sora |t1h2=leomord |t1h3=pharsa |t1h4=karrie |t1h5=gatotkaca
        |t2h1=valentina |t2h2=fanny |t2h3=luo yi |t2h4=claude |t2h5=hylos
        <!-- Hero bans -->
        |t1b1=yve |t1b2=baxia |t1b3=yu zhong |t1b4=grock |t1b5=benedetta
        |t2b1=zhuxin |t2b2=lancelot |t2b3=kalea |t2b4=chou |t2b5=hilda
    }}
}}
}}
* {{Bgcolortext|up|Winner}} will advance to Round 3: High (2-0)
* {{Bgcolortext|down|Loser}} will advance to Round 3: Mid (1-1)
{{box|break|padding=2em}}

====Low (0-1)====
{{Matchlist|id=M7SWISSR21|title=Round 2 Matches ({{abbr/Bo1}})|width=330px|matchsection=Round 2
|M1header=January 11
|M1={{Match
    |bestof=1|caster1=Laphel|caster2=GideonQ|caster3=Arashi|mvp=Bankai
    |opponent1={{TeamOpponent|boostgate esports}}
    |opponent2={{TeamOpponent|team zone}}
    |date=January 11, 2026 - 14:00 {{Abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=A6hM-NgI4zk
        |team1side=blue |team2side=red |length=11:54 |winner=2|comment=<b>Dangerous Grass</b>
        <!-- Hero picks -->
        |t1h1=yu zhong |t1h2=lancelot |t1h3=kimmy |t1h4=granger |t1h5=hylos
        |t2h1=lapu-lapu |t2h2=yi sun-shin |t2h3=pharsa |t2h4=karrie |t2h5=gatotkaca
        <!-- Hero bans -->
        |t1b1=kalea |t1b2=grock |t1b3=yve |t1b4=lunox |t1b5=alice
        |t2b1=hayabusa |t2b2=selena |t2b3=zhuxin |t2b4=claude |t2b5=obsidia
    }}
}}
|M2={{Match
    |bestof=1|caster1=Laphel|caster2=GideonQ|caster3=Arashi|mvp=Seilah
    |opponent1={{TeamOpponent|evil}}
    |opponent2={{TeamOpponent|DianFengYaoGuai}}
    |date=January 11, 2026 - 15:00 {{Abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=qlBjm8gQuII
        |team1side=red |team2side=blue |length=19:53 |winner=1|comment=<b>Flying Cloud</b>
        <!-- Hero picks -->
        |t1h1=arlott |t1h2=yi sun-shin |t1h3=faramis |t1h4=freya |t1h5=grock
        |t2h1=alice |t2h2=lancelot |t2h3=lunox |t2h4=karrie |t2h5=kalea
        <!-- Hero bans -->
        |t1b1=fanny |t1b2=zhuxin |t1b3=yu zhong |t1b4=valentina |t1b5=esmeralda
        |t2b1=baxia |t2b2=yve |t2b3=sora |t2b4=uranus |t2b5=lapu-lapu
    }}
}}
|M3={{Match
    |bestof=1|caster1=Reptar|caster2=Mirko|caster3=Naisou|mvp=Lunar
    |opponent1={{TeamOpponent|cg esports}}
    |opponent2={{TeamOpponent|aurora gaming}}
    |date=January 11, 2026 - 17:45 {{Abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=agBoOF4fyMc
        |team1side=red |team2side=blue |length=15:01 |winner=2|comment=<b>Expanding Rivers</b>
        <!-- Hero picks -->
        |t1h1=yu zhong |t1h2=lancelot |t1h3=pharsa |t1h4=moskov |t1h5=chou
        |t2h1=uranus |t2h2=fanny |t2h3=lunox |t2h4=harith |t2h5=grock
        <!-- Hero bans -->
        |t1b1=zhuxin |t1b2=selena |t1b3=kalea |t1b4=lylia |t1b5=claude
        |t2b1=yve |t2b2=kimmy |t2b3=hilda |t2b4=badang |t2b5=karrie
    }}
}}
|M4={{Match
    |bestof=1|caster1=Reptar|caster2=Mirko|caster3=Naisou|mvp=Edward
    |opponent1={{TeamOpponent|cfu gaming}}
    |opponent2={{TeamOpponent|aurora gaming ph}}
    |date=January 11, 2026 - 20:45 {{Abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=j3To11JqXXs
        |team1side=red |team2side=blue |length=21:02 |winner=2|comment=<b>Broken Walls</b>
        <!-- Hero picks -->
        |t1h1=sora |t1h2=leomord |t1h3=valentina |t1h4=granger |t1h5=badang
        |t2h1=lapu-lapu |t2h2=yi sun-shin |t2h3=lunox |t2h4=claude |t2h5=gatotkaca
        <!-- Hero bans -->
        |t1b1=grock |t1b2=fanny |t1b3=yve |t1b4=cici |t1b5=uranus
        |t2b1=hilda |t2b2=kalea |t2b3=zhuxin |t2b4=karrie |t2b5=hylos
    }}
}}
}}
* {{Bgcolortext|up|Winner}} will advance to Round 3: Mid (1-1)
* {{Bgcolortext|down|Loser}} will advance to Round 3: Low (0-2)
{{box|end|padding=2em}}

===Round 3===
{{box|start|padding=2em}}
====High (2-0)====
{{Matchlist|width=330px|id=M7SWISSR30|title=Round 3 High Matches ({{abbr/Bo3}})|matchsection=Round 3
|M1header=January 12
|M1={{Match
    |bestof=3|caster1=Laphel|caster2=Mirko|caster3=Naisou|mvp=Nino, Owennn{{!}}alekk
    |opponent1={{TeamOpponent|alter ego}}
    |opponent2={{TeamOpponent|yangon galacticos}}
    |date=January 12, 2026 - 18:00{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=FMzUf2KecS0
        |team1side=red |team2side=blue |length=16:45 |winner=1|comment=<b>Dangerous Grass</b>
        <!-- Hero picks -->
        |t1h1=sora |t1h2=leomord |t1h3=yve |t1h4=claude |t1h5=gatotkaca
        |t2h1=benedetta |t2h2=guinevere |t2h3=zhuxin |t2h4=karrie |t2h5=badang
        <!-- Hero bans -->
        |t1b1=baxia |t1b2=helcurt |t1b3=valentina |t1b4=arlott |t1b5=lancelot
        |t2b1=grock |t2b2=yu zhong |t2b3=fanny |t2b4=hylos |t2b5=hayabusa
    }}
    |map2={{Map|vod=https://www.youtube.com/watch?v=Cuvpc3yhCyE
        |team1side=blue |team2side=red |length=14:29 |winner=1|comment=<b>Broken Walls</b>
        <!-- Hero picks -->
        |t1h1=terizla |t1h2=nolan |t1h3=yve |t1h4=freya |t1h5=kalea
        |t2h1=yu zhong |t2h2=fredrinn |t2h3=kimmy |t2h4=claude |t2h5=hylos
        <!-- Hero bans -->
        |t1b1=baxia |t1b2=helcurt |t1b3=valentina |t1b4=pharsa |t1b5=luo yi
        |t2b1=zhuxin |t2b2=grock |t2b3=sora |t2b4=yi sun-shin |t2b5=lapu-lapu
    }}
    |map3={{Map|finished=skip}}
}}
|M2header=January 13
|M2={{Match
    |bestof=3|caster1=Reptar|caster2=GideonQ|caster3=Brigida|mvp=Oheb, Sekys, Stormie
    |opponent1={{TeamOpponent|selangor red giants}}
    |opponent2={{TeamOpponent|team liquid ph}}
    |date=January 13, 2026 - 17:55{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=3D0Xf78sOSc
        |team1side=red |team2side=blue |length=18:46 |winner=2|comment=<b>Flying Cloud</b>
        <!-- Hero picks -->
        |t1h1=phoveus |t1h2=lancelot |t1h3=luo yi |t1h4=sora |t1h5=badang
        |t2h1=valentina |t2h2=hayabusa |t2h3=pharsa |t2h4=claude |t2h5=hilda
        <!-- Hero bans -->
        |t1b1=yu zhong |t1b2=zhuxin |t1b3=yve |t1b4=joy |t1b5=yi sun-shin
        |t2b1=fanny |t2b2=kalea |t2b3=grock |t2b4=karrie |t2b5=chou
    }}
    |map2={{Map|vod=https://www.youtube.com/watch?v=4IeCp1vZQHQ
        |team1side=blue |team2side=red |length=14:32 |winner=1|comment=<b>Flying Cloud</b>
        <!-- Hero picks -->
        |t1h1=cici |t1h2=yi sun-shin |t1h3=zetian |t1h4=sora |t1h5=chou
        |t2h1=lapu-lapu |t2h2=fredrinn |t2h3=kimmy |t2h4=karrie |t2h5=gatotkaca
        <!-- Hero bans -->
        |t1b1=yu zhong |t1b2=lancelot |t1b3=yve |t1b4=arlott |t1b5=pharsa
        |t2b1=kalea |t2b2=claude |t2b3=zhuxin |t2b4=selena |t2b5=luo yi
    }}
    |map3={{Map|vod=https://www.youtube.com/watch?v=M9Q4SQ69ie0
        |team1side=red |team2side=blue |length=27:25 |winner=1|comment=<b>Expanding Rivers</b>
        <!-- Hero picks -->
        |t1h1=uranus |t1h2=hayabusa |t1h3=yve |t1h4=cici |t1h5=hilda
        |t2h1=alice |t2h2=lancelot |t2h3=pharsa |t2h4=granger |t2h5=hylos
        <!-- Hero bans -->
        |t1b1=yu zhong |t1b2=claude |t1b3=zhuxin |t1b4=arlott |t1b5=harith
        |t2b1=fanny |t2b2=kalea |t2b3=sora |t2b4=joy |t2b5=yi sun-shin
    }}
}}
}}
* {{Bgcolortext|up|Winner}} will advance to the [[M7 World Championship/Knockout Stage|Knockout Stage]]
* {{Bgcolortext|down|Loser}} will advance to Round 4: High (2-1)
{{box|break|padding=2em}}

====Mid (1-1)====
{{Matchlist|id=M7SWISSR31|title=Round 3 Mid Matches ({{abbr/Bo1}})|width=330px|matchsection=Round 3
|M1header=January 12
|M1={{Match
    |bestof=1|caster1=Laphel|caster2=Mirko|caster3=Naisou|mvp=Cuffin
    |opponent1={{TeamOpponent|black sentence esports}}
    |opponent2={{TeamOpponent|team falcons}}
    |date=January 12, 2026 - 15:45{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=cH9lxKc9_N0
        |team1side=red |team2side=blue |length=17:07 |winner=2|comment=<b>Expanding Rivers</b>
        <!-- Hero picks -->
        |t1h1=lapu-lapu |t1h2=x.borg |t1h3=pharsa |t1h4=claude |t1h5=gatotkaca
        |t2h1=yu zhong |t2h2=baxia |t2h3=kimmy |t2h4=karrie |t2h5=hylos
        <!-- Hero bans -->
        |t1b1=zhuxin |t1b2=grock |t1b3=yve |t1b4=angela |t1b5=mathilda
        |t2b1=valentina |t2b2=kalea |t2b3=sora |t2b4=lancelot |t2b5=joy
    }}
}}
|M2={{Match
    |bestof=1|caster1=Laphel|caster2=Mirko|caster3=Naisou|mvp=Edward
    |opponent1={{TeamOpponent|team zone}}
    |opponent2={{TeamOpponent|aurora gaming ph}}
    |date=January 12, 2026 - 17:00{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=d0ZMpetH-GY
        |team1side=red |team2side=blue |length=19:31 |winner=2|comment=<b>Flying Cloud</b>
        <!-- Hero picks -->
        |t1h1=lapu-lapu |t1h2=leomord |t1h3=zhuxin |t1h4=karrie |t1h5=gatotkaca
        |t2h1=arlott |t2h2=fredrinn |t2h3=yve |t2h4=claude |t2h5=khaleed
        <!-- Hero bans -->
        |t1b1=grock |t1b2=uranus |t1b3=sora |t1b4=hilda |t1b5=hylos
        |t2b1=kalea |t2b2=yu zhong |t2b3=yi sun-shin |t2b4=lancelot |t2b5=hayabusa
    }}
}}
|M3header=January 13
|M3={{Match
    |bestof=1|caster1=Reptar|caster2=GideonQ|caster3=Brigida|mvp=Sigibum
    |opponent1={{TeamOpponent|evil}}
    |opponent2={{TeamOpponent|aurora gaming}}
    |date=January 13, 2026 - 15:45{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=4sM_6Ta_Dj0
        |team1side=red |team2side=blue |length=17:58 |winner=2|comment=<b>Broken Walls</b>
        <!-- Hero picks -->
        |t1h1=sora |t1h2=joy |t1h3=valentina |t1h4=karrie |t1h5=gatotkaca
        |t2h1=uranus |t2h2=lancelot |t2h3=pharsa |t2h4=claude |t2h5=grock
        <!-- Hero bans -->
        |t1b1=fanny |t1b2=selena |t1b3=zhuxin |t1b4=lapu-lapu |t1b5=yu zhong
        |t2b1=freya |t2b2=yve |t2b3=hylos |t2b4=kalea |t2b5=hilda
    }}
}}
|M4={{Match
    |bestof=1|caster1=Reptar|caster2=GideonQ|caster3=Brigida|mvp=Kid Bomba
    |opponent1={{TeamOpponent|team spirit}}
    |opponent2={{TeamOpponent|onic}}
    |date=January 13, 2026 - 16:45{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=hFSYKNTtVBE
        |team1side=red |team2side=blue |length=14:56 |winner=1|comment=<b>Expanding Rivers</b>
        <!-- Hero picks -->
        |t1h1=esmeralda |t1h2=leomord |t1h3=pharsa |t1h4=granger |t1h5=chou
        |t2h1=lapu-lapu |t2h2=lancelot |t2h3=kadita |t2h4=bruno |t2h5=kalea
        <!-- Hero bans -->
        |t1b1=zhuxin |t1b2=claude |t1b3=yi sun-shin |t1b4=lunox |t1b5=karrie
        |t2b1=yve |t2b2=sora |t2b3=yu zhong |t2b4=guinevere |t2b5=baxia
    }}
}}
}}
* {{Bgcolortext|up|Winner}} will advance to Round 4: High (2-1)
* {{Bgcolortext|down|Loser}} will advance to Round 4: Low (1-2)
{{box|break|padding=2em}}

====Low (0-2)====
{{Matchlist|width=330px|id=M7SWISSR32|title=Round 3 Low Matches ({{abbr/Bo3}})|matchsection=Round 3
|M1header=January 12
|M1={{Match
    |bestof=3|caster1=Laphel|caster2=Mirko|caster3=Naisou|mvp=CikuGais, Garyy
    |opponent1={{TeamOpponent|cg esports}}
    |opponent2={{TeamOpponent|DianFengYaoGuai}}
    |date=January 12, 2026 - 14:00{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=31D128_m02I
        |team1side=blue |team2side=red |length=10:56 |winner=1|comment=<b>Broken Walls</b>
        <!-- Hero picks -->
        |t1h1=lapu-lapu |t1h2=lancelot |t1h3=lunox |t1h4=claude |t1h5=grock
        |t2h1=yu zhong |t2h2=hayabusa |t2h3=valentina |t2h4=moskov |t2h5=chou
        <!-- Hero bans -->
        |t1b1=yve |t1b2=fanny |t1b3=sora |t1b4=karrie |t1b5=harith
        |t2b1=zhuxin |t2b2=kalea |t2b3=hilda |t2b4=uranus |t2b5=esmeralda
    }}
    |map2={{Map|vod=https://www.youtube.com/watch?v=vGV5w9bfkmU
        |team1side=red |team2side=blue |length=21:45 |winner=1|comment=<b>Expanding Rivers</b>
        <!-- Hero picks -->
        |t1h1=uranus |t1h2=lancelot |t1h3=lunox |t1h4=harith |t1h5=chou
        |t2h1=esmeralda |t2h2=yi sun-shin |t2h3=pharsa |t2h4=claude |t2h5=gatotkaca
        <!-- Hero bans -->
        |t1b1=kalea |t1b2=fanny |t1b3=zhuxin |t1b4=guinevere |t1b5=phoveus
        |t2b1=grock |t2b2=yve |t2b3=hilda |t2b4=lapu-lapu |t2b5=yu zhong
    }}
    |map3={{Map|finished=skip}}
}}
|M2header=January 13
|M2={{Match
    |bestof=3|caster1=Reptar|caster2=GideonQ|caster3=Brigida|mvp=Wadu, Detective
    |opponent1={{TeamOpponent|boostgate esports}}
    |opponent2={{TeamOpponent|cfu gaming}}
    |date=January 13, 2026 - 14:00{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=0dgShgTjyNY
        |team1side=red |team2side=blue |length=14:09 |winner=2|comment=<b>Expanding Rivers</b>
        <!-- Hero picks -->
        |t1h1=phoveus |t1h2=hayabusa |t1h3=pharsa |t1h4=claude |t1h5=khaleed
        |t2h1=lapu-lapu |t2h2=fredrinn |t2h3=kimmy |t2h4=moskov |t2h5=kalea
        <!-- Hero bans -->
        |t1b1=grock |t1b2=zhuxin |t1b3=lancelot |t1b4=granger |t1b5=karrie
        |t2b1=yve |t2b2=sora |t2b3=fanny |t2b4=gatotkaca |t2b5=hylos
    }}
    |map2={{Map|vod=https://www.youtube.com/watch?v=SUQFgGQqev8
        |team1side=red |team2side=blue |length=13:09 |winner=2|comment=<b>Dangerous Grass</b>
        <!-- Hero picks -->
        |t1h1=phoveus |t1h2=leomord |t1h3=pharsa |t1h4=karrie |t1h5=gatotkaca
        |t2h1=uranus |t2h2=joy |t2h3=kadita |t2h4=claude |t2h5=chou
        <!-- Hero bans -->
        |t1b1=zhuxin |t1b2=lancelot |t1b3=grock |t1b4=lunox |t1b5=kimmy
        |t2b1=yve |t2b2=sora |t2b3=hayabusa |t2b4=fanny |t2b5=yi sun-shin
    }}
    |map3={{Map|finished=skip}}
}}
}}
* {{Bgcolortext|up|Winner}} will advance to Round 4: Low (1-2)
* {{Bgcolortext|down|Loser}} will be eliminated
{{box|end}}

===Round 4===
{{box|start|padding=2em}}
====High (2-1)====
{{Matchlist|width=330px|id=M7SWISSR41|title=Round 4 High Matches ({{abbr/Bo3}})|matchsection=Round 4
|M1header=January 15
|M1={{Match
    |bestof=3|caster1=Laphel|caster2=Mirko|caster3=Naisou|mvp=Tienzy, Saano, Pagu
    |opponent1={{TeamOpponent|team falcons}}
    |opponent2={{TeamOpponent|aurora gaming}}
    |date=January 15, 2026 - 15:00{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=O2ISb-hK87M
        |team1side=blue |team2side=red |length=13:47 |winner=2|comment=<b>Dangerous Grass</b>
        <!-- Hero picks -->
        |t1h1=lapu-lapu |t1h2=leomord |t1h3=zhuxin |t1h4=karrie |t1h5=grock
        |t2h1=sora |t2h2=harley |t2h3=yve |t2h4=claude |t2h5=hilda
        <!-- Hero bans -->
        |t1b1=fanny |t1b2=kalea |t1b3=lancelot |t1b4=hayabusa |t1b5=phoveus
        |t2b1=baxia |t2b2=mathilda |t2b3=akai |t2b4=esmeralda |t2b5=fredrinn
    }}
    |map2={{Map|vod=https://www.youtube.com/watch?v=3MTY7H2qCHs
        |team1side=blue |team2side=red |length=18:35 |winner=1|comment=<b>Expanding Rivers</b>
        <!-- Hero picks -->
        |t1h1=arlott |t1h2=fredrinn |t1h3=kimmy |t1h4=karrie |t1h5=grock
        |t2h1=terizla |t2h2=guinevere |t2h3=yve |t2h4=claude |t2h5=chou
        <!-- Hero bans -->
        |t1b1=fanny |t1b2=kalea |t1b3=sora |t1b4=yu zhong |t1b5=hayabusa
        |t2b1=baxia |t2b2=mathilda |t2b3=akai |t2b4=esmeralda |t2b5=uranus
    }}
    |map3={{Map|vod=https://www.youtube.com/watch?v=OYmTbJYwG0U
        |team1side=red |team2side=blue |length=18:41 |winner=2|comment=<b>Flying Cloud</b>
        <!-- Hero picks -->
        |t1h1=esmeralda |t1h2=fredrinn |t1h3=valentina |t1h4=karrie |t1h5=minotaur
        |t2h1=terizla |t2h2=lancelot |t2h3=lunox |t2h4=claude |t2h5=grock
        <!-- Hero bans -->
        |t1b1=fanny |t1b2=sora |t1b3=zhuxin |t1b4=yu zhong |t1b5=pharsa
        |t2b1=yve |t2b2=mathilda |t2b3=kimmy |t2b4=arlott |t2b5=uranus
    }}
}}
|M2={{Match
    |bestof=3|caster1=Laphel|caster2=Mirko|caster3=Naisou|mvp=Edward, Light
    |opponent1={{TeamOpponent|aurora gaming ph}}
    |opponent2={{TeamOpponent|team spirit}}
    |date=January 15, 2026 - 17:35{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=_9Jz7z_yTrk
        |team1side=red |team2side=blue |length=20:13 |winner=1|comment=<b>Flying Cloud</b>
        <!-- Hero picks -->
        |t1h1=sora |t1h2=yi sun-shin |t1h3=zetian |t1h4=harith |t1h5=gatotkaca
        |t2h1=gloo |t2h2=nolan |t2h3=pharsa |t2h4=claude |t2h5=kalea
        <!-- Hero bans -->
        |t1b1=yu zhong |t1b2=hilda |t1b3=zhuxin |t1b4=esmeralda |t1b5=uranus
        |t2b1=lunox |t2b2=grock |t2b3=yve |t2b4=kagura |t2b5=lapu-lapu
    }}
    |map2={{Map|vod=https://www.youtube.com/watch?v=cyRTOt8jbzc
        |team1side=red |team2side=blue |length=17:55 |winner=1|comment=<b>Expanding Rivers</b>
        <!-- Hero picks -->
        |t1h1=lapu-lapu |t1h2=fredrinn |t1h3=zhuxin |t1h4=granger |t1h5=chip
        |t2h1=uranus |t2h2=guinevere |t2h3=yve |t2h4=karrie |t2h5=chou
        <!-- Hero bans -->
        |t1b1=claude |t1b2=kalea |t1b3=hilda |t1b4=esmeralda |t1b5=yu zhong
        |t2b1=lunox |t2b2=grock |t2b3=yi sun-shin |t2b4=khaleed |t2b5=pharsa
    }}
    |map3={{Map|finished=skip}}
}}
|M3={{Match
    |bestof=3|caster1=Laphel|caster2=Mirko|caster3=Naisou|mvp=Sanford, Sanford
    |opponent1={{TeamOpponent|team liquid ph}}
    |opponent2={{TeamOpponent|yangon galacticos}}
    |date=January 15, 2026 - 19:30{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=_fVh_34K7iA
        |team1side=blue |team2side=red |length=21:36 |winner=1|comment=<b>Expanding Rivers</b>
        <!-- Hero picks -->
        |t1h1=yu zhong |t1h2=yi sun-shin |t1h3=valentina |t1h4=sora |t1h5=gatotkaca
        |t2h1=uranus |t2h2=nolan |t2h3=pharsa |t2h4=granger |t2h5=kalea
        <!-- Hero bans -->
        |t1b1=fanny |t1b2=baxia |t1b3=yve |t1b4=fredrinn |t1b5=hayabusa
        |t2b1=lancelot |t2b2=claude |t2b3=zhuxin |t2b4=ruby |t2b5=harith
    }}
    |map2={{Map|vod=https://www.youtube.com/watch?v=SLT6KfV9t-w
        |team1side=red |team2side=blue |length=15:31 |winner=1|comment=<b>Broken Walls</b>
        <!-- Hero picks -->
        |t1h1=gloo |t1h2=yi sun-shin |t1h3=zhuxin |t1h4=granger |t1h5=hilda
        |t2h1=arlott |t2h2=guinevere |t2h3=pharsa |t2h4=claude |t2h5=chou
        <!-- Hero bans -->
        |t1b1=fanny |t1b2=baxia |t1b3=helcurt |t1b4=hayabusa |t1b5=fredrinn
        |t2b1=lancelot |t2b2=yu zhong |t2b3=yve |t2b4=ruby |t2b5=sora
    }}
    |map3={{Map|finished=skip}}
}}
}}
* {{Bgcolortext|up|Winner}} will advance to the [[M7 World Championship/Knockout Stage|Knockout Stage]]
* {{Bgcolortext|down|Loser}} will advance to Round 5
{{box|break|padding=2em}}

====Low (1-2)====
{{Matchlist|width=330px|id=M7SWISSR40|title=Round 4 Low Matches ({{abbr/Bo3}})|matchsection=Round 4
|M1header=January 16
|M1={{Match
    |bestof=3|caster1=Reptar|caster2=GideonQ|caster3=Brigida|mvp=BOXI{{!}}Boxixixixi, BOXI{{!}}Boxixixixi
    |opponent1={{TeamOpponent|cfu gaming}}
    |opponent2={{TeamOpponent|team zone}}
    |date=January 16, 2026 - 15:00{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=6ZSXgmO6Smk
        |team1side=blue |team2side=red |length=17:10 |winner=1|comment=<b>Broken Walls</b>
        <!-- Hero picks -->
        |t1h1=lapu-lapu |t1h2=fredrinn |t1h3=zetian |t1h4=claude |t1h5=chou
        |t2h1=yu zhong |t2h2=hayabusa |t2h3=pharsa |t2h4=harith |t2h5=hylos
        <!-- Hero bans -->
        |t1b1=sora |t1b2=yve |t1b3=yi sun-shin |t1b4=leomord |t1b5=karrie
        |t2b1=grock |t2b2=zhuxin |t2b3=kalea |t2b4=baxia |t2b5=joy
    }}
    |map2={{Map|vod=https://www.youtube.com/watch?v=1PRoROz_SoE
        |team1side=blue |team2side=red |length=23:46 |winner=1|comment=<b>Dangerous Grass</b>
        <!-- Hero picks -->
        |t1h1=yu zhong |t1h2=guinevere |t1h3=pharsa |t1h4=claude |t1h5=chou
        |t2h1=lapu-lapu |t2h2=lancelot |t2h3=kadita |t2h4=karrie |t2h5=hylos
        <!-- Hero bans -->
        |t1b1=yve |t1b2=yi sun-shin |t1b3=sora |t1b4=leomord |t1b5=joy
        |t2b1=grock |t2b2=zhuxin |t2b3=kalea |t2b4=baxia |t2b5=fredrinn
    }}
    |map3={{Map|finished=skip}}
}}
|M2={{Match
    |bestof=3|caster1=Reptar|caster2=GideonQ|caster3=Brigida|mvp=Garyy, Shin, CikuGais
    |opponent1={{TeamOpponent|black sentence esports}}
    |opponent2={{TeamOpponent|cg esports}}
    |date=January 16, 2026 - 17:00{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=w0Vmj84zymk
        |team1side=red |team2side=blue |length=16:21 |winner=2|comment=<b>Flying Cloud</b>
        <!-- Hero picks -->
        |t1h1=arlott |t1h2=baxia |t1h3=pharsa |t1h4=granger |t1h5=hilda
        |t2h1=gloo |t2h2=joy |t2h3=yve |t2h4=karrie |t2h5=chou
        <!-- Hero bans -->
        |t1b1=zhuxin |t1b2=claude |t1b3=fanny |t1b4=lancelot |t1b5=leomord
        |t2b1=yu zhong |t2b2=grock |t2b3=sora |t2b4=moskov |t2b5=cici
    }}
    |map2={{Map|vod=https://www.youtube.com/watch?v=zXgjFT0XcAs
        |team1side=blue |team2side=red |length=17:07 |winner=1|comment=<b>Broken Walls</b>
        <!-- Hero picks -->
        |t1h1=esmeralda |t1h2=lancelot |t1h3=lunox |t1h4=karrie |t1h5=hylos
        |t2h1=cici |t2h2=nolan |t2h3=yve |t2h4=granger |t2h5=hilda
        <!-- Hero bans -->
        |t1b1=fanny |t1b2=claude |t1b3=sora |t1b4=baxia |t1b5=joy
        |t2b1=grock |t2b2=yu zhong |t2b3=kalea |t2b4=zhuxin |t2b5=selena
    }}
    |map3={{Map|vod=https://www.youtube.com/watch?v=MTJH6cCJQwQ
        |team1side=red |team2side=blue |length=18:32 |winner=2|comment=<b>Broken Walls</b>
        <!-- Hero picks -->
        |t1h1=uranus |t1h2=lancelot |t1h3=yve |t1h4=harith |t1h5=chip
        |t2h1=hilda |t2h2=yi sun-shin |t2h3=odette |t2h4=karrie |t2h5=chou
        <!-- Hero bans -->
        |t1b1=claude |t1b2=sora |t1b3=kalea |t1b4=lunox |t1b5=esmeralda
        |t2b1=yu zhong |t2b2=grock |t2b3=zhuxin |t2b4=hylos |t2b5=gatotkaca
    }}
}}
|M3={{Match
    |bestof=3|caster1=Reptar|caster2=GideonQ|caster3=Brigida|mvp=Lutpiii, Kairi
    |opponent1={{TeamOpponent|evil}}
    |opponent2={{TeamOpponent|onic id}}
    |date=January 16, 2026 - 19:30{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=l_oZFvkgVnc
        |team1side=red |team2side=blue |length=11:27 |winner=2|comment=<b>Dangerous Grass</b>
        <!-- Hero picks -->
        |t1h1=arlott |t1h2=baxia |t1h3=pharsa |t1h4=karrie |t1h5=kalea
        |t2h1=yu zhong |t2h2=yi sun-shin |t2h3=faramis |t2h4=cici |t2h5=gatotkaca
        <!-- Hero bans -->
        |t1b1=fanny |t1b2=claude |t1b3=zhuxin |t1b4=harith |t1b5=luo yi
        |t2b1=freya |t2b2=sora |t2b3=yve |t2b4=lapu-lapu |t2b5=uranus
    }}
    |map2={{Map|vod=https://www.youtube.com/watch?v=q_GemAaL74Q
        |team1side=blue |team2side=red |length=12:43 |winner=2|comment=<b>Dangerous Grass</b>
        <!-- Hero picks -->
        |t1h1=uranus |t1h2=leomord |t1h3=zhuxin |t1h4=karrie |t1h5=chou
        |t2h1=arlott |t2h2=yi sun-shin |t2h3=yve |t2h4=esmeralda |t2h5=chip
        <!-- Hero bans -->
        |t1b1=fanny |t1b2=claude |t1b3=yu zhong |t1b4=gatotkaca |t1b5=guinevere
        |t2b1=freya |t2b2=sora |t2b3=grock |t2b4=hylos |t2b5=hilda
    }}
    |map3={{Map|finished=skip}}
}}
}}
* {{Bgcolortext|up|Winner}} will advance to Round 5
* {{Bgcolortext|down|Loser}} will be eliminated
{{box|end|padding=2em}}

===Round 5===
{{Matchlist|width=330px|id=M7SWISSRD5|title=Round 5 Matches ({{abbr/Bo3}})|matchsection=Round 5
|M1header=January 17
|M1={{Match
    |bestof=3|caster1=Laphel|caster2=Mirko|caster3=Naisou|mvp=Kid Bomba, Hiko
    |opponent1={{TeamOpponent|team spirit}}
    |opponent2={{TeamOpponent|cfu gaming}}
    |date=January 17, 2026 - 15:00{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=7xH1EYxw2zw
        |team1side=blue |team2side=red |length=13:58 |winner=1|comment=<b>Dangerous Grass</b>
        <!-- Hero picks -->
        |t1h1=valentina |t1h2=yi sun-shin |t1h3=lunox |t1h4=cici |t1h5=kalea
        |t2h1=sora |t2h2=leomord |t2h3=faramis |t2h4=granger |t2h5=chou
        <!-- Hero bans -->
        |t1b1=yu zhong |t1b2=grock |t1b3=yve |t1b4=joy |t1b5=zetian
        |t2b1=claude |t2b2=zhuxin |t2b3=pharsa |t2b4=esmeralda |t2b5=uranus
    }}
    |map2={{Map|vod=https://www.youtube.com/watch?v=ocKY0Bny0MY
        |team1side=red |team2side=blue |length=14:02 |winner=1|comment=<b>Broken Walls</b>
        <!-- Hero picks -->
        |t1h1=lapu-lapu |t1h2=lancelot |t1h3=valentina |t1h4=granger |t1h5=chou
        |t2h1=yu zhong |t2h2=joy |t2h3=pharsa |t2h4=karrie |t2h5=grock
        <!-- Hero bans -->
        |t1b1=claude |t1b2=zhuxin |t1b3=kalea |t1b4=kadita |t1b5=freya
        |t2b1=yve |t2b2=yi sun-shin |t2b3=sora |t2b4=esmeralda |t2b5=fredrinn
    }}
    |map3={{Map|finished=skip}}
}}
|M2={{Match
    |bestof=3|caster1=Laphel|caster2=Mirko|caster3=Naisou|mvp=Ying, Stitch
    |opponent1={{TeamOpponent|yangon galacticos}}
    |opponent2={{TeamOpponent|cg esports}}
    |date=January 17, 2026 - 16:45{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=uzVtVZzG-ic
        |team1side=red |team2side=blue |length=13:21 |winner=1|comment=<b>Dangerous Grass</b>
        <!-- Hero picks -->
        |t1h1=uranus |t1h2=nolan |t1h3=zhuxin |t1h4=freya |t1h5=chou
        |t2h1=phoveus |t2h2=yi sun-shin |t2h3=pharsa |t2h4=claude |t2h5=hilda
        <!-- Hero bans -->
        |t1b1=lancelot |t1b2=kalea |t1b3=grock |t1b4=yve |t1b5=lunox
        |t2b1=baxia |t2b2=helcurt |t2b3=fanny |t2b4=yu zhong |t2b5=guinevere
    }}
    |map2={{Map|vod=https://www.youtube.com/watch?v=XgErfBThu8M
        |team1side=blue |team2side=red |length=23:36 |winner=1|comment=<b>Expanding Rivers</b>
        <!-- Hero picks -->
        |t1h1=sora |t1h2=baxia |t1h3=yve |t1h4=claude |t1h5=kalea
        |t2h1=esmeralda |t2h2=yi sun-shin |t2h3=cecilion |t2h4=harith |t2h5=chou
        <!-- Hero bans -->
        |t1b1=lancelot |t1b2=lunox |t1b3=grock |t1b4=odette |t1b5=valentina
        |t2b1=helcurt |t2b2=zhuxin |t2b3=freya |t2b4=guinevere |t2b5=hayabusa
    }}
    |map3={{Map|finished=skip}}
}}
|M3={{Match
    |bestof=3|caster1=Laphel|caster2=Mirko|caster3=Naisou|mvp=Kairi, Trolll, Skylar
    |opponent1={{TeamOpponent|team falcons}}
    |opponent2={{TeamOpponent|onic}}
    |date=January 17, 2026 - 18:45{{abbr/ICT}} |youtube=MLBB Esports|facebook=MLBB Esports
    |map1={{Map|vod=https://www.youtube.com/watch?v=y97JU_4jDwk
        |team1side=blue |team2side=red |length=11:52 |winner=2|comment=<b>Expanding Rivers</b>
        <!-- Hero picks -->
        |t1h1=esmeralda |t1h2=baxia |t1h3=kimmy |t1h4=claude |t1h5=hilda
        |t2h1=yu zhong |t2h2=hayabusa |t2h3=zhuxin |t2h4=lunox |t2h5=chou
        <!-- Hero bans -->
        |t1b1=yi sun-shin |t1b2=kalea |t1b3=karrie |t1b4=cici |t1b5=harith
        |t2b1=fredrinn |t2b2=mathilda |t2b3=yve |t2b4=minotaur |t2b5=uranus
    }}
    |map2={{Map|vod=https://www.youtube.com/watch?v=vTEFjte0xQU
        |team1side=blue |team2side=red |length=23:07 |winner=1|comment=<b>Broken Walls</b>
        <!-- Hero picks -->
        |t1h1=gloo |t1h2=hayabusa |t1h3=zhuxin |t1h4=cici |t1h5=chou
        |t2h1=yu zhong |t2h2=guinevere |t2h3=lylia |t2h4=karrie |t2h5=hylos
        <!-- Hero bans -->
        |t1b1=yi sun-shin |t1b2=kalea |t1b3=claude |t1b4=lancelot |t1b5=grock
        |t2b1=fredrinn |t2b2=mathilda |t2b3=yve |t2b4=uranus |t2b5=lapu-lapu
    }}
    |map3={{Map|vod=https://www.youtube.com/watch?v=ML43d0dZL1A
        |team1side=red |team2side=blue |length=12:08 |winner=2|comment=<b>Broken Walls</b>
        <!-- Hero picks -->
        |t1h1=phoveus |t1h2=baxia |t1h3=valentina |t1h4=moskov |t1h5=chou
        |t2h1=yu zhong |t2h2=joy |t2h3=kimmy |t2h4=granger |t2h5=kalea
        <!-- Hero bans -->
        |t1b1=yi sun-shin |t1b2=claude |t1b3=zhuxin |t1b4=karrie |t1b5=cici
        |t2b1=fredrinn |t2b2=mathilda |t2b3=yve |t2b4=gloo |t2b5=uranus
    }}
}}
}}
* {{Bgcolortext|up|Winner}} will advance to the [[M7 World Championship/Knockout Stage|Knockout Stage]]
* {{Bgcolortext|down|Loser}} will be eliminated
"""

# Parsing Logic
lines = input_text.split('\n')
parsed_rows = []

current_team1 = ""
current_team2 = ""

# Regex patterns
opp1_re = re.compile(r'\|opponent1\s*=\s*\{\{TeamOpponent\|([^}]+)\}\}')
opp2_re = re.compile(r'\|opponent2\s*=\s*\{\{TeamOpponent\|([^}]+)\}\}')
key_val_re = re.compile(r'\|([a-zA-Z0-9]+)\s*=\s*([^|}\n]+)')

i = 0
while i < len(lines):
    line = lines[i]
    
    # Check for opponents
    m1 = opp1_re.search(line)
    if m1:
        current_team1 = m1.group(1).strip().replace('_', ' ').title()
        
    m2 = opp2_re.search(line)
    if m2:
        current_team2 = m2.group(1).strip().replace('_', ' ').title()
        
    # Check for map start
    if '|map' in line and '={{Map' in line:
        # Collect lines for this map block
        # Liquipedia format usually ends the map stats with a closing brace on a new line
        # We capture content until we see a line that is effectively closing the block
        
        map_content_lines = []
        j = i
        
        # Collect lines that belong to this map
        while j < len(lines):
            curr_line = lines[j]
            map_content_lines.append(curr_line)
            
            # Check for termination of map block.
            # The map block ends when we encounter a line that closes the Map template.
            # Usually this is a line containing '}}' and ending the specific map data.
            # In Liquipedia: 
            #   |t2b5=lunox
            #   }}
            # Or inline.
            
            # If we see a line that starts with '|' (next parameter) or '}}' (end of block)
            # But key=value pairs are also on lines starting with '|'.
            # So we just look for the line that closes the braces.
            
            # Heuristic: If the line contains '}}' and doesn't contain 'Map' (start of new map) 
            # or if it is the specific closing brace for the Map object.
            # Often the map block ends with a line "    }}"
            
            if '}}' in curr_line:
                # Check if it is just a closing brace or if data is inline
                # If the line is just "    }}" or ends with " }}", we break
                if curr_line.strip() == '}}' or curr_line.strip().endswith('}}'):
                    break
            
            j += 1
            
        # Join content to parse
        map_text = " ".join(map_content_lines)
        
        # Extract all key-value pairs
        data = dict(key_val_re.findall(map_text))
        
        # Process Data
        if 'team1side' in data and 'winner' in data:
            t1_side = data['team1side'].strip()
            winner = data['winner'].strip()
            
            # Map Name
            map_name = "Unknown"
            comment = data.get('comment', '')
            nm = re.search(r'<b>(.*?)</b>', comment)
            if nm: map_name = nm.group(1)
            
            # Helper to clean hero names
            def get_hero(key):
                val = data.get(key, '').strip()
                # Replace underscores and title case
                return val.replace('_', ' ').title()
            
            t1_bans = [get_hero(f't1b{k}') for k in range(1, 6)]
            t1_picks = [get_hero(f't1h{k}') for k in range(1, 6)]
            t2_bans = [get_hero(f't2b{k}') for k in range(1, 6)]
            t2_picks = [get_hero(f't2h{k}') for k in range(1, 6)]
            
            # Logic to assign Blue/Red sides
            blue_team, red_team = "", ""
            blue_bans, blue_picks, red_bans, red_picks = [], [], [], []
            blue_res, red_res = "", ""
            
            if t1_side == 'blue':
                blue_team = current_team1
                red_team = current_team2
                blue_bans, blue_picks = t1_bans, t1_picks
                red_bans, red_picks = t2_bans, t2_picks
                
                if winner == '1':
                    blue_res, red_res = "WIN", "LOSE"
                else:
                    blue_res, red_res = "LOSE", "WIN"
            else:
                # Team 1 is Red, Team 2 is Blue
                blue_team = current_team2
                red_team = current_team1
                blue_bans, blue_picks = t2_bans, t2_picks
                red_bans, red_picks = t1_bans, t1_picks
                
                if winner == '1': # Team 1 (Red) won
                    blue_res, red_res = "LOSE", "WIN"
                else:
                    blue_res, red_res = "WIN", "LOSE"
            
            row = [
                "M7", map_name, blue_team, 
                blue_bans[0], blue_bans[1], blue_bans[2], blue_bans[3], blue_bans[4],
                blue_picks[0], blue_picks[1], blue_picks[2], blue_picks[3], blue_picks[4],
                blue_res, red_team,
                red_bans[0], red_bans[1], red_bans[2], red_bans[3], red_bans[4],
                red_picks[0], red_picks[1], red_picks[2], red_picks[3], red_picks[4],
                red_res
            ]
            parsed_rows.append(row)
            
            # Advance main loop index to skip processed lines
            i = j
            
    i += 1

# Create DataFrame
columns = [
    'Tournament', 'Selected Map', 'Team', 
    'BLUE SIDE Ban 1', 'Ban 2', 'Ban 3', 'Ban 4', 'Ban 5', 
    'Pick 1', 'Pick 2', 'Pick 3', 'Pick 4', 'Pick 5', 
    'Result', 'Team', 
    'RED SIDE Ban 1', 'Ban 2', 'Ban 3', 'Ban 4', 'Ban 5', 
    'Pick 1', 'Pick 2', 'Pick 3', 'Pick 4', 'Pick 5', 
    'Result'
]

df = pd.DataFrame(parsed_rows, columns=columns)

# Save to Excel
output_filename = "knockout_m7.xlsx"
df.to_excel(output_filename, sheet_name='MLBB Statistics', index=False)

print(f"Successfully converted {len(parsed_rows)} matches to {output_filename}")