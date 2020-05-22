 $(document).ready(function(){
 //All functions contained in the ready function
    $('.sidenav').sidenav(//for the drop-down menu
            {
                'draggable': true,
            });
    $('.dropdown-trigger').dropdown(
        {
            'hover': true,
            'constrainWidth': false,
            'coverTrigger' : false,
            'alignment' : 'center',
            'closeOnClick' : false,
        });
       $('.collapsible').collapsible();

 });