% include('header_hoy.tpl', title='Niveles del día', ndd=noticias_del_dia)
    <h1>{{name}}</h1>
		<img src="data:image/png;base64, {{plot_url_img}}" id="municipio" alt =""/>
		<img src="data:image/png;base64, {{plot_url_img_cam}}" id="municipio-cam" alt =""/>
		<table border="0" width="100%" cellpadding="5" cellspacing="5">
		<tr>
		<td width="50%"> 

		<table border="1">
		% for b in busquedaAEMET:
			<caption><h2>Datos Meteorológicos</h2></caption>
			<colgroup>
				<col />
				<col />
			</colgroup>
			<tbody>
				<tr>
					<th scope="row">Temperatura máxima (ºC)</th>
					<td>{{b['Temperatura minima']}}</td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Temperatura mínima (ºC)</th>
					<td>{{b['Temperatura maxima']}}</td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Humedad relativa máxima</th>
					<td>{{b['Humedad relativa maxima']}}</td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Humedad relativa mínima</th>
					<td>{{b['Humedad relativa minima']}}</td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">% Precipitaciones</th>
					<td>{{b['precipitaciones 00-24']}}</td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Velocidad del Viento</th>
					<td>{{b['viento 00-24']}}</td>
				</tr>
			</tbody> 
	     % end
 </table>
 </td>
<td width="50%"> 
 		<table border="1">
			<caption><h2>Datos Calidad del Aire</h2></caption>
			<colgroup>
				<col />
				<col />
			</colgroup>
			<tbody>
				<tr>
					<th scope="row">Dióxido de Nitrógeno</th>
					<td>{{cursor3['NO2']}}</td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Partículas en Suspensión < PM10</th>
					<td>{{cursor3['PM10']}}</td>
				</tr>
			</tbody> 	
			<tbody>
				<tr>
					<th scope="row">Partículas en Suspensión < PM2,5</th>
					<td>{{cursor3['PM25']}}</td>
				</tr>
			</tbody>
			<tbody>
				<tr>
					<th scope="row">Monóxido de Carbono</th>
					<td>{{cursor3['CO']}}</td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Concentración de Ozono</th>
					<td>{{cursor3['O3']}}</td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Dióxido de Azufre</th>
					<td>{{cursor3['SO2']}}</td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Monóxido de Nitrogeno</th>
					<td>{{cursor3['NO']}}</td>
				</tr>
			</tbody> 
 </table>
 </td>
</tr>
</table>

		<a href="../hoy">Volver</a>
% include('footer.tpl')
