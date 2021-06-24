class ExamException(Exception):
    pass


class CSVTimeSeriesFile:

    def __init__ (self,name):
        self.name=name

    def get_data (self):
        
        time_series=[]
        #verifico che il file esista
        try:
            time_series_file = open(self.name ,"r")
        except:
            raise ExamException ("problemi nella lettura del file")
        
        
        for line in time_series_file:
            minilista = []
            elements = line.split(',')
            #salto intestazione
            if (elements[0] == 'epoch'):
                continue
            #controllo ci siano epoch e temperature
            if len(elements) < 2:
               continue

            #converte epoch e temperature
            epoch = elements [0]
            try:
                epoch = int(epoch)
            except:
                continue
            minilista.append(epoch)           

            temperature = elements [1]
            
            try:
                temperature = float(temperature)
            except:
                continue
            
            minilista.append(temperature)

            time_series.append(minilista)
            
        #controllo possibili epoch disordinate
        for i in range (len(time_series)-1):
            if time_series[i][0] >= time_series[i+1][0]:
                raise ExamException ('time_series disordinata')


        return (time_series)
        

def compute_daily_variance(time_series):
    varianze=[]
    #valori intermedi per i calcoli
    intermedio=0

    giorno_prec=0
    daily_values=[]

    for minilista in time_series:

        epoch=minilista[0]
        temp=minilista[1]
        #individuo l'inizio giornata
        day_start_epoch = epoch - (epoch % 86400)

        if (day_start_epoch != giorno_prec):
            giorno_prec=day_start_epoch

            #se ci sono misurazione nella giornata faccio i calcoli
            if daily_values:
                somma = sum (daily_values)

                media=somma/len(daily_values)
                
                for element in daily_values:
                    intermedio += ((media - element) ** 2)
                #se c'e' solo una misurazione varianza e' nulla, altrimenti calcolo varianza
                if len(daily_values)==1:
                    var=None
                else:
                    var=intermedio/(len(daily_values)-1)
                #aggiungo la varianza alla lista dei risultati e riinizializzo il valore intermedio
                varianze.append(var)
                intermedio=0
            #svuoto daily values e aggiungo la prima misura del giorno dopo
            daily_values.clear()
            daily_values.append(temp)

        else:
            #aggiunge temp se il giorno non e' cambiato
            daily_values.append(temp)


    return varianze

