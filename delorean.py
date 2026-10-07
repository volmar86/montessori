def spiel_schleife():
    global geschwindigkeit_mph, status, hindernis_timer, sfx_travel_gestartet, start_travel_zeit, sieg_zeit, musik_stopp_geplant, letzter_vol_wert
    
    if status == "LÄUFT":
        _, beschleunigung, spawn_faktor, trigger_speed = hole_schwierigkeits_parameter()
        
        # Normale Beschleunigung unterhalb der dynamischen Trigger-Geschwindigkeit
        if geschwindigkeit_mph < trigger_speed:
            geschwindigkeit_mph += beschleunigung
            if geschwindigkeit_mph >= trigger_speed:
                geschwindigkeit_mph = trigger_speed
                sfx_travel_gestartet = True
                start_travel_zeit = time.time()
                sfx_travel_starten()
        else:
            # Synchronisation von Trigger-Speed bis 88 MPH auf genau 6.5 Sekunden
            verstrichen = time.time() - start_travel_zeit
            geschwindigkeit_mph = trigger_speed + (verstrichen / 6.5) * (ziel_geschwindigkeit - trigger_speed)
            if geschwindigkeit_mph >= ziel_geschwindigkeit:
                geschwindigkeit_mph = ziel_geschwindigkeit
                
        # Lenkung & Grenzen
        lenkung_verarbeiten()
        neue_x = spieler.xcor() + lenkung_x
        if neue_x < -170:
            neue_x = -170
        if neue_x > 170:
            neue_x = 170
        spieler.setx(neue_x)
        
        scrolling_tempo = geschwindigkeit_mph / 3.0
        for s in streifen_liste:
            s.sety(s.ycor() - scrolling_tempo)
            if s.ycor() < -300:
                s.sety(s.ycor() + 600)
        
        # Hindernisse
        hindernis_timer += 1
        spawn_intervall = max(12, int((60 - int(geschwindigkeit_mph / 2)) * spawn_faktor))
        if hindernis_timer >= spawn_intervall:
            hindernis_erzeugen()
            hindernis_timer = 0
            
        h_tempo = (geschwindigkeit_mph / 6.0) + 3.0
        for h in hindernisse[:]:
            h.sety(h.ycor() - h_tempo)
            
            # Kollision
            dx = abs(h.xcor() - spieler.xcor())
            dy = abs(h.ycor() - spieler.ycor())
            if dx < 35 and dy < 50:
                status = "CRASH"
                musik_stoppen()
                
            if h.ycor() < -350:
                h.hideturtle()
                hindernisse.remove(h)
                
        # ⚡ GEWONNEN BEI EXAKT 88 MPH
        if geschwindigkeit_mph >= ziel_geschwindigkeit:
            status = "SIEG"
            sieg_zeit = time.time()
            
            delorean_x = spieler.xcor()
            delorean_y = spieler.ycor()
            spieler.hideturtle()
            
            # Blitz-Effekt
            fenster.bgcolor("white")
            fenster.update()
            time.sleep(0.08)
            fenster.bgcolor(FARBE_NEON_BLAU)
            fenster.update()
            time.sleep(0.08)
            fenster.bgcolor(FARBE_RASEN)
            
            feuer_spuren_zeichnen(delorean_x, delorean_y)
            
        ui_aktualisieren()

    elif status == "SIEG":
        # Stufenloses Ausblenden der Musik über 10 Sekunden (Fade-Out)
        verstrichen = time.time() - sieg_zeit
        fade_dauer = 10.0  # Fade-Out Dauer in Sekunden
        
        if verstrichen < fade_dauer:
            neuer_vol = max(0, int(350 * (1.0 - verstrichen / fade_dauer)))
            if neuer_vol != letzter_vol_wert and musik_aktiv:
                letzter_vol_wert = neuer_vol
                try:
                    ctypes.windll.winmm.mciSendStringW(f'setaudio bgm volume to {neuer_vol}', None, 0, 0)
                except Exception:
                    pass
        elif not musik_stopp_geplant:
            musik_stopp_geplant = True
            musik_stoppen()
        
    fenster.update()
    fenster.ontimer(spiel_schleife, FPS_TAKT)
