% include('header_predicciones.tpl', title='Predicciones', ndd=noticias_del_dia)
	<h1>{{name}}</h1>
	<p>Para hoy, día <b>{{listaStrings[0]}}</b>, el nivel de alerta es: <b>{{listaPredicciones[0][listaStrings[1]]}}</b></p>
		<img src="data:image/png;base64, {{plot_url_img}}" id="municipio" alt =""/>
		<img src="data:image/png;base64, {{plot_url_img_cam}}" id="municipio-cam" alt =""/>
		
	<h1>Niveles para los próximos días:</h1>
	<p>Para mañana, día <b>{{listaStrings[2]}}</b>, el nivel de alerta es: <b>{{listaPredicciones[1][listaStrings[3]]}}</b> <img src="data:image/png;base64, {{plot_url_img_fm}}" id="peq" alt =""/></p>
	
	<p>Para pasado mañana, día <b>{{listaStrings[4]}}</b>, el nivel de alerta es: <b>{{listaPredicciones[2][listaStrings[5]]}}</b> <img src="data:image/png;base64, {{plot_url_img_fpm}}" id="peq" alt =""/></p>
	
 <a href="/predicciones">Volver</a>
% include('footer.tpl')
