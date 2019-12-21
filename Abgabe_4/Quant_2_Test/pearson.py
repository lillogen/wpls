def correlation(X, Y):
    laenge = len(X);
    
    X_average = sum(X) / float(laenge);
    Y_average = sum(Y) / float(laenge);
    
    zaehler = 0.0;
    zweiteSumme = 0.0;
    dritteSumme = 0.0;
    
    #Summe im Zaehler berechnen
    for i in range(laenge):
        zaehler += (X[i]-X_average)*(Y[i]-Y_average);
    
    #Naechste Summe im Nenner berechnen
    for i in range(laenge):
        zweiteSumme += (X[i]-X_average)**2;
    
    #Letzte Summe im Nenner berechnen
    for i in range(laenge):
        dritteSumme += (Y[i]-Y_average)**2;

    #Wurzel ziehen
    nenner = (zweiteSumme*dritteSumme)**(0.5);

#Ergebnis berechnen, falls der Nenner 0 ist, gebe nan, also not a number zurueck
    result = zaehler/nenner if (nenner !=0) else float('nan')
    
    return result
