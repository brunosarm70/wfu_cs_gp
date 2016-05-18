from celery import task

@task()
def call_run_tournament(pk, datetime):
    
    from .models import Tournament, Tournament_Status
    tournament = Tournament.objects.get(pk=pk)
    
    if tournament.datetime == datetime and (tournament.status == Tournament_Status.objects.get(name = 'Open')  or tournament.status == Tournament_Status.objects.get(name = 'Closed')):
        msg = " sí se ejecutó."
        #tournament.status = Tournament_Status.objects.get(name = 'Finished')
        # Time to call the Run Tournament function
        tournament.run_tournament()
    else:
        print(datetime)
        print(tournament.datetime)
        print(tournament.status)
        msg = " no se ejecutó, porque las horas no coinciden."
        
    tournament.save()
    
    return tournament.name + msg