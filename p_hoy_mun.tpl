% include('header_hoy.tpl', title='Niveles del día', ndd=noticias_del_dia)
    <h1>{{name}}</h1>
	<img src="data:image/png;base64, {{plot_url_img}}" id="municipio" alt =""/>
	<img src="data:image/png;base64, {{plot_url_img_cam}}" id="municipio-cam" alt =""/>
	<table>
		<tr>
		<td width="40%"  id="idblanco" valign="top"> 
		<table border="1">
			<colgroup>
				<col />
				<col />
			</colgroup>
			<thead>
			<tr>
				<th scope="col" colspan="2" align="center"><b>Datos Meteorológicos</b></th>
			</tr>
			</thead>
			% for b in busquedaAEMET:
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
					<th scope="row">Humedad relativa máxima (%)</th>
					<td>{{b['Humedad relativa maxima']}}</td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Humedad relativa mínima (%)</th>
					<td>{{b['Humedad relativa minima']}}</td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Precipitaciones (%)</th>
					<td>{{b['precipitaciones 00-24']}}</td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Velocidad del Viento (km/h)</th>
					<td>{{b['viento 00-24']}}</td>
				</tr>
			</tbody> 
	     % end
		</table>
		</td>
		<td width="60%"  id="idblanco" valign="top"> 
 		<table border="1">
			<colgroup>
				<col />
				<col />
			</colgroup>
			<thead>
			<tr>
				<th scope="col" colspan="2" align="center">Datos Calidad del Aire</th>
			</tr>
			</thead>
			<tbody>
				<tr>
					<th scope="row">Dióxido de Nitrógeno (µg/m<sup>3</sup>)</th>
					<td>{{cursor3['NO2']}}</td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Partículas en Suspensión < PM10 (µg/m<sup>3</sup>)</th>
					<td>{{cursor3['PM10']}}</td>
				</tr>
			</tbody> 	
			<tbody>
				<tr>
					<th scope="row">Partículas en Suspensión < PM2,5 (µg/m<sup>3</sup>N)</th>
					<td>{{cursor3['PM25']}}</td>
				</tr>
			</tbody>
			<tbody>
				<tr>
					<th scope="row">Monóxido de Carbono (mg/m<sup>3</sup>)</th>
					<td>{{cursor3['CO']}}</td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Concentración de Ozono (µg/m<sup>3</sup>)</th>
					<td>{{cursor3['O3']}}</td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Dióxido de Azufre (µg/m<sup>3</sup>)</th>
					<td>{{cursor3['SO2']}}</td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Monóxido de Nitrogeno (µg/m<sup>3</sup>)</th>
					<td>{{cursor3['NO']}}</td>
				</tr>
			</tbody> 
		</table>
		</td>
		</tr>
	</table>

	<a href="../hoy">Volver</a>
% include('footer.tpl')
