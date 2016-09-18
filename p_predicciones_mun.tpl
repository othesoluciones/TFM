% include('header_predicciones.tpl', title='Predicciones', ndd=noticias_del_dia)
	<h1>Predicción del Nivel de Gramíneas {{name}}</h1>
		<img src="data:image/png;base64, {{plot_url_img}}" id="municipio" alt =""/>
		<img src="data:image/png;base64, {{plot_url_img_cam}}" id="municipio-cam" alt =""/>
<table border="1">
		<caption><h2>TOP 5 Municipios con mayor nivel de gramíneas para el día<b>{{listaStrings[0]}}</b> </h2></caption>
			<colgroup>
				<col />
				<col />
			</colgroup>
			<tbody>
				<tr>
					<th scope="row">{{listaPredicciones[0]['Municipio']}}</th>
					<td>{{listaPredicciones[0][listaStrings[1]]}}</td>
				</tr>
			</tbody> 
 </table>
 <table border="1">
		<caption><h2>TOP 5 Municipios con mayor nivel de gramíneas para el día<b>{{listaStrings[2]}}</b> </h2></caption>
			<colgroup>
				<col />
				<col />
			</colgroup>
			<tbody>
				<tr>
					<th scope="row">{{listaPredicciones[1]['Municipio']}}</th>
					<td>{{listaPredicciones[1][listaStrings[3]]}}</td>
				</tr>
			</tbody> 
 </table>
 <table border="1">
		<caption><h2>TOP 5 Municipios con mayor nivel de gramíneas para el día<b>{{listaStrings[4]}}</b> </h2></caption>
			<colgroup>
				<col />
				<col />
			</colgroup>
			<tbody>
				<tr>
					<th scope="row">{{listaPredicciones[2]['Municipio']}}</th>
					<td>{{listaPredicciones[2][listaStrings[5]]}}</td>
				</tr>
			</tbody> 
			
 </table>
 <a href="/predicciones">Volver</a>
% include('footer.tpl')
