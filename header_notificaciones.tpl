<!--<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">-->
<!DOCTYPE html>
<html> <!--xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">-->

<head>
  <title>{{title}}</title>
  <!--<meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />-->
  <meta charset="iso-8859-1">
  <link rel="stylesheet" type="text/css" href="/static/style/style.css" />
  <link rel="stylesheet" href="/static/style/jquery-ui.css" />
  <script src="/static/style/jquery-1.9.1.js"></script>
  <script src="/static/style/jquery-ui.js"></script>
  <script type="text/javascript">
      function toggle(id) {
        var el = document.getElementById(id);
        el.style.display = (el.style.display != 'none' ? 'none' : '' );
      }
  </script>
  <script> $.datepicker.regional['es'] = {
 		closeText: 'Cerrar',
		 prevText: '<Ant',
 nextText: 'Sig>',
 currentText: 'Hoy',
 monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
 monthNamesShort: ['Ene','Feb','Mar','Abr', 'May','Jun','Jul','Ago','Sep', 'Oct','Nov','Dic'],
 dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
 dayNamesShort: ['Dom','Lun','Mar','Mié','Juv','Vie','Sáb'],
 dayNamesMin: ['Do','Lu','Ma','Mi','Ju','Vi','Sá'],
 weekHeader: 'Sem',
 dateFormat: 'dd/mm/yy',
 firstDay: 1,
 isRTL: false,
 showMonthAfterYear: false,
 yearSuffix: '',
 showWeek: true
 };
 $.datepicker.setDefaults($.datepicker.regional['es']);

	$(function () {
		$("#fechaDesde").datepicker({
		  minDate:1,
		  onClose: function (selectedDate) {
			$("#fechaHasta").datepicker("option", "minDate", selectedDate);
			$("#fechaHasta").attr("disabled", false);
		  }
		}),
		
		$("#fechaHasta").datepicker().attr("disabled",true);
	
	});
	$(function () {
		$("#fechaHasta").datepicker();
	});

 </script>
<!--<script type="text/javascript">
jQuery.validator.addMethod("isValid", function (value, element) {
    var startDate = $('#fechaDesde').val();
    var finDate = $('#fechaHasta').val();
    return Date.parse(startDate) < Date.parse(finDate);
}, "* End date must be after start date");
$(function () {
    $('#fechaDesde,#fechaHasta').datepicker()

    $('#custom').validate({
        rules: {
            'fechaL': { required: true, date: true },
            'fechaS': { required: true, date: true, isValid: true }
        }, messages: {
            'fechaL': { required: 'date required msj!',
                date: 'invalid date format msj'
            },
            'fechaS': { required: 'date required msj!',
                date: 'invalid date format msj',
                isValid: 'End date must be after start date'
            }
        }
    });

});
</script>-->
</head>

<body>
  <div id="main">
    <div id="header">
      <div id="logo">
        <h1>Alergias <span class="alternate_colour">Madrid</span></h1>
      </div>
      <div id="menubar">
        <ul id="menu">
          <!-- put class="tab_selected" in the li tag for the selected page - to highlight which page you're on -->
          <li><a href="/">Home</a></li>
          <li><a href="/hoy">Niveles del día</a></li>
		  <li><a href="/predicciones">Predicciones</a></li>
		  <li><a href="/reporte">¡Repórtanos!</a></li>
		  <li class="tab_selected"><a href="/notificaciones">Notificaciones</a></li>
        </ul>
      </div>
    </div>
    <div id="site_content">
      <div id="panel"><img src="/static/style/panel3.jpg" alt="tree tops" /></div>
      <div class="sidebar">
        <!-- insert your sidebar items here -->
        <h1>Últimas Noticias</h1>
        <h2>Nuevo sitio web</h2>
        <h3>30 de Julio de 2016</h3>
        <p>2016 nos lleva al estreno de nuestra web. Échale un vistazo y cuentános que opinas<br /><a href="#">Leer más</a></p>
        <h1>Links de interés</h1>
        <ul>
          <li><a href="http://www.polenes.com/">Sociedad Española de Alergología (SEAIC)</a></li>
          <li><a href="http://www.madrid.org/polen">Portal de Salud Comunidad de Madrid</a></li>
          <li><a href="http://www.laalergia.com/tipos-alergia/polen/">LaAlergia.com</a></li>
		  <li><a href="http://alergiaalpolen.com/niveles-de-polen/">AlergiaAlPolen.com</a></li>
        </ul>
      </div>
      <div id="content">
        <!-- insert the page content here -->
